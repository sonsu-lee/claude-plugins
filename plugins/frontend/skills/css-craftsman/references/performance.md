# CSS Performance

## will-change

Only apply `will-change` to elements that are about to animate. It promotes the element to its own compositor layer, which consumes GPU memory.

```css
/* CORRECT: apply on interaction, not permanently */
.card:hover { will-change: transform; }
.card.animating { will-change: transform, opacity; }

/* WRONG: permanent will-change on many elements */
.card { will-change: transform; }
```

Rules:
- Never apply `will-change` to more than a handful of elements at once
- Remove it after the animation completes when possible (via JS class toggle)
- Never use `will-change: auto` — it does nothing

## contain

Use CSS containment on isolated visual components to limit the browser's recalculation scope:

```css
/* Cards, modals, popovers — self-contained UI blocks */
.card { contain: layout paint; }
.modal { contain: layout paint style; }
```

Containment types:
- `layout` — element's internals don't affect outside layout. Creates a formatting context. **Important:** `position: fixed` children become positioned relative to the contained element, not the viewport.
- `paint` — element's contents don't paint outside its bounds. Creates a stacking context (affects z-index behavior). Safe if no visible overflow needed.
- `style` — counters and quotes scoped to this subtree.
- `inline-size` — required by container queries. `container-type: inline-size` implicitly applies this.
- `content` — shorthand for `layout paint style` (use on fully isolated blocks).
- `strict` — shorthand for `size layout paint style` (use on data-heavy widgets where performance matters most).

Do not use `contain: size` unless you explicitly set the element's dimensions — it makes the element report 0x0 intrinsic size.

**When to use which:**

| Containment | Safe for | Watch out for |
|-------------|----------|---------------|
| `layout paint` | Cards, list items, widgets | Fixed-position children change behavior |
| `content` | Fully isolated blocks | Same as above + counter scoping |
| `strict` | Dashboard widgets, live feeds | Requires explicit dimensions |
| `inline-size` | Container query hosts | Implicit with `container-type` |

## Selectors to Avoid

- **Universal selector in complex selectors**: `*` is acceptable only for box-sizing reset. Never use `.parent *` or `.parent > *` for styling.
- **Deeply nested selectors**: Keep selectors to 2-3 levels maximum. CSS Modules already scope styles — deep nesting is unnecessary.
- **`@import` in CSS files**: It blocks parallel downloading. Use the bundler's import system instead (JS imports of CSS modules).
- **Deeply nested `calc()`**: More than 2 levels of nested `calc()` hurts readability and can slow calculation. Simplify with custom properties.

```css
/* WRONG */
.element { width: calc(100% - calc(var(--sidebar) + calc(var(--gap) * 2))); }

/* CORRECT: flatten with a custom property */
.element {
  --offset: calc(var(--sidebar) + var(--gap) * 2);
  width: calc(100% - var(--offset));
}
```

## CSS Custom Properties

Use custom properties for values that are repeated or need to change dynamically (theming, responsive adjustments, component variants).

Do not create a custom property for a value used only once — it adds indirection without benefit.

```css
/* CORRECT: repeated or themed values */
:root {
  --space-sm: 8px;
  --space-md: 16px;
  --radius: 8px;
}

/* WRONG: single-use custom property */
.header {
  --header-left-pad: 24px;
  padding-left: var(--header-left-pad);
}
```

## Animation and Transition

### Only animate composited properties

These properties can be animated without triggering layout or paint — use them exclusively:

- `transform` (translate, scale, rotate)
- `opacity`

```css
/* CORRECT: composited properties */
.fadeSlide {
  transition: transform 200ms ease, opacity 200ms ease;
}
.fadeSlide.enter {
  transform: translateY(8px);
  opacity: 0;
}

/* WRONG: triggers layout on every frame */
.slide { transition: top 200ms ease, height 200ms ease; }
```

### Use translate() instead of top/left

For position-based animations, always use `transform: translate()` instead of animating `top`, `left`, `right`, or `bottom`:

```css
/* CORRECT */
.tooltip { transform: translateY(-4px); transition: transform 150ms ease; }
.tooltip.visible { transform: translateY(0); }

/* WRONG */
.tooltip { top: -4px; transition: top 150ms ease; }
.tooltip.visible { top: 0; }
```

### transition vs animation

- `transition` — for simple state changes (hover, focus, enter/exit). Two states.
- `animation` with `@keyframes` — for multi-step sequences, looping, or complex choreography.

Do not use `@keyframes` for a simple A-to-B state change. Do not use `transition` for multi-step effects.

### prefers-reduced-motion

You MUST respect the user's motion preference. Use one of these two approaches:

**Approach 1: Global blanket disable**

```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

**Approach 2: Opt-in motion (preferred for new projects)**

Only add motion when the user has not requested reduced motion:

```css
/* Base: no motion */
.element { transform: translateY(0); }

/* Motion only for users who accept it */
@media (prefers-reduced-motion: no-preference) {
  .element { transition: transform 200ms ease; }
}
```

Approach 2 is safer — motion is off by default and explicitly enabled. Use this for new work. Use Approach 1 when retrofitting an existing codebase.

## Image and Media

- Use `aspect-ratio` to reserve space and prevent layout shift:

```css
.thumbnail {
  aspect-ratio: 16 / 9;
  width: 100%;
  object-fit: cover;
}
```

- Set `content-visibility: auto` on below-the-fold sections for rendering performance:

```css
.section {
  content-visibility: auto;
  contain-intrinsic-size: auto 500px; /* estimated height */
}
```
