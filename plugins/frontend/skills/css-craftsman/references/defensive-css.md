# Defensive CSS

Write CSS that handles unexpected content, edge cases, and variable conditions gracefully. Every rule here prevents a real-world layout bug.

## Flex Item Overflow

Flex children with long content will overflow their container unless constrained. Always add `min-width: 0` on flex children that contain text or dynamic content.

```css
.flex-container {
  display: flex;
  gap: var(--spacing-md);
}

.flex-child {
  min-width: 0; /* Allows text truncation and prevents overflow */
}
```

Without `min-width: 0`, the flex child's minimum size defaults to its content size, which can blow out the layout.

## Images

Set this baseline for all images:

```css
img {
  max-width: 100%;
  height: auto;
  display: block; /* Removes bottom gap from inline image baseline */
}
```

In flex or grid containers where the image must fill a specific area:

```css
.image-fill {
  width: 100%;
  height: 100%;
  object-fit: cover; /* Crops to fill — maintains aspect ratio */
}
```

Always include `width` and `height` attributes in HTML `<img>` tags to prevent layout shift during load (CLS).

## Text Overflow Protection

Prevent long unbroken strings (URLs, email addresses, hashes) from breaking layouts:

```css
.content {
  overflow-wrap: break-word; /* Breaks long words/URLs to prevent overflow */
}
```

For cleaner word breaks in supported languages:

```css
.prose {
  hyphens: auto;
  -webkit-hyphens: auto;
}
```

Apply `overflow-wrap: break-word` broadly (on body or content wrappers). It has no visual effect on normal text — it only activates when content would otherwise overflow.

## Heights

Use `min-height` instead of `height` for any container that holds dynamic content.

```css
/* Wrong — content taller than 500px overflows */
.hero { height: 500px; }

/* Correct — at least 500px, grows with content */
.hero { min-height: 500px; }
```

Rules:
- `height: 100%` only works when every ancestor up to the viewport has an explicit height. Prefer `min-height: 100vh` or `min-height: 100dvh` instead.
- Use `dvh` (dynamic viewport height) on mobile to account for browser chrome: `min-height: 100dvh`.

## Scroll Containers

Prevent scroll chaining (where scrolling past the end of a modal scrolls the page behind it):

```css
.scroll-container {
  overflow-y: auto;
  overscroll-behavior: contain;
}
```

Reserve space for the scrollbar to prevent layout shift when content changes from non-scrollable to scrollable:

```css
.scroll-container {
  scrollbar-gutter: stable;
}
```

## Empty States

Never let empty containers collapse and break layout:

```css
/* Hide element when empty */
.card-list:empty {
  display: none;
}

/* Or show a message */
.card-list:empty::before {
  content: "No items found";
  display: block;
  padding: var(--spacing-lg);
  text-align: center;
  color: var(--color-text-muted);
}
```

For elements with whitespace-only children, use `:has()`:

```css
.container:not(:has(*)) {
  display: none;
}
```

## Long Content Testing

Before considering any component done, test with:
- Very long text (single word, full paragraph).
- Very short text (1-2 characters).
- No text at all (empty state).
- Many items (50+ in a list).
- Single item.
- Content in different languages (German words are long, CJK characters have different line-breaking rules).

## Variable Content Constraints

Use `min-width` / `max-width` instead of fixed `width` for elements with dynamic content:

```css
/* Wrong — too rigid */
.tag { width: 120px; }

/* Correct — adapts to content within bounds */
.tag {
  min-width: 4rem;
  max-width: 12rem;
}
```

Same for height:

```css
.card {
  min-height: 8rem;  /* Doesn't collapse when empty */
  /* No max-height unless scrolling is intended */
}
```

## Safe Area (Notched Devices)

Account for device notches and home indicators on iOS:

```css
.fixed-bottom-bar {
  padding-bottom: env(safe-area-inset-bottom, 0px);
}

.full-width-section {
  padding-left: env(safe-area-inset-left, 0px);
  padding-right: env(safe-area-inset-right, 0px);
}
```

Must include `viewport-fit=cover` in the HTML meta tag for `env()` values to be nonzero:

```html
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
```

## Sticky Positioning Pitfalls

`position: sticky` silently fails when:
- Any ancestor has `overflow: hidden`, `overflow: auto`, or `overflow: scroll` (the sticky element sticks within that overflow container, not the viewport).
- The sticky element has no room to scroll (parent is same height as the sticky element).
- In flex/grid layouts, the element stretches to match sibling height (default `align-items: stretch`). Fix with `align-self: flex-start` on the sticky element.

Debug by checking every ancestor for `overflow` values. For full sticky positioning patterns including scroll-state detection, see `references/layout.md`.

## Transition Safety

Never use `transition: all`. It transitions every property change including layout-triggering ones, causing jank.

```css
/* WRONG — transitions everything including width, height, padding */
.element { transition: all 0.3s ease; }

/* CORRECT — only transition intended properties */
.element { transition: background-color 0.2s ease, color 0.2s ease, box-shadow 0.2s ease; }
```

Safe to transition: `opacity`, `transform`, `filter`. Use with caution: `background-color`, `box-shadow`, `border-color`. Avoid transitioning: `width`, `height`, `margin`, `padding`, `top`, `left`.

## overflow: clip vs overflow: hidden

Prefer `overflow: clip` over `overflow: hidden` when possible:

```css
.card { overflow: clip; }   /* Clips without creating formatting context */
.card { overflow: hidden; } /* Clips AND creates new block formatting context */
```

`overflow: hidden` creates a **block formatting context** (BFC), not a stacking context. However, `overflow: clip` clips content identically without creating a BFC. Use `clip` by default; use `hidden` only when you need the formatting context (e.g., to contain floats or prevent margin collapse).

## Scroll Margin for Fixed Headers

When using sticky/fixed headers, anchored content hides behind the header. Add scroll margin:

```css
:target {
  scroll-margin-top: calc(var(--header-height, 4rem) + var(--spacing-md));
}
```

## margin-trim

When a container has `padding`, child margins touching the padding edges create extra space. The classic fix is verbose:

```css
/* OLD */
.card > *:first-child { margin-top: 0; }
.card > *:last-child { margin-bottom: 0; }

/* NEW */
.card {
  padding: 1rem;
  margin-trim: block;
}
```

**Rule:** When you add `padding` to a container, add `margin-trim` in the same axis. Values: `block`, `inline`, `block-start`, `block-end`, `inline-start`, `inline-end`. Progressive enhancement — no effect in unsupported browsers.

## Background Image Fallbacks

Always set a background color fallback when using background images:

```css
.hero {
  background-color: var(--color-gray-800); /* Fallback */
  background-image: url('hero.webp');
  background-size: cover;
  background-position: center;
}
```

## Pointer Interaction Safety

Prevent text selection on interactive elements, enable it on content:

```css
button, [role="button"] {
  user-select: none;
}

.content {
  user-select: text;
}
```

For touch targets, enforce minimum 44x44px hit areas:

```css
.icon-button {
  min-width: 44px;
  min-height: 44px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}
```
