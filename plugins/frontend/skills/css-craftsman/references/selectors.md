# Selector & Specificity Management

## Max Nesting Depth: 3 Levels

Never nest selectors deeper than 3 levels. If you reach 4+, restructure by extracting inner elements into their own class.

```css
/* Acceptable — 2 levels */
.card .title { ... }

/* Acceptable — 3 levels */
.card .header .title { ... }

/* Too deep — restructure */
.page .section .card .header .title { ... }

/* Fix: give .title its own class */
.card-title { ... }
```

## No `!important`

Never use `!important` except for utility classes that must override all other styles.

```css
/* Allowed — utility override */
.hidden { display: none !important; }
.sr-only { position: absolute !important; /* ... */ }

/* Not allowed — specificity hack */
.header .nav .link { color: blue !important; } /* Fix specificity instead */
```

Every `!important` in the codebase must have a comment explaining why it exists. If you cannot justify it, remove it and fix the specificity chain.

## No Tag Selectors for Styling

Do not style bare HTML tags. Use class selectors.

```css
/* Wrong */
div { padding: 1rem; }
p { margin-bottom: 1rem; }
header { background: white; }

/* Correct */
.container { padding: 1rem; }
.paragraph { margin-bottom: 1rem; }
.site-header { background: white; }
```

Exception: CSS resets and normalizers may target tags directly. Prose/markdown content rendered from a CMS may use tag selectors scoped to a wrapper:

```css
.prose p { margin-bottom: 1em; }
.prose h2 { font-size: var(--font-size-2xl); }
```

## CSS Module Scoping

When using CSS Modules (or other scoping mechanisms like Scoped CSS in Vue), selectors are automatically scoped. This eliminates the need for BEM or complex naming.

Keep selectors flat and simple:

```css
/* In Button.module.css */
.root { ... }
.icon { ... }
.label { ... }

/* In Card.module.css */
.root { ... }
.header { ... }
.title { ... }
.content { ... }
```

No risk of collision. No need for `.card__header--active`. Just `.header` scoped to the component.

## Attribute Selectors

Use `data-*` attributes for JavaScript hooks. Use classes for CSS styling. Keep the concerns separated.

```css
/* Styling — use class */
.button-primary { background: var(--color-primary); }

/* JS hook — use data attribute */
/* <button data-action="submit"> — selected in JS, not styled in CSS */
```

Exception: Styling based on state communicated through attributes is acceptable:

```css
[aria-expanded="true"] .dropdown-panel { display: block; }
[data-state="active"] { outline: 2px solid var(--color-primary); }
```

## Pseudo-Selectors

### `:is()` and `:where()` for grouping

`:is()` takes the highest specificity of its arguments. `:where()` always has 0 specificity.

```css
/* :where() — good for defaults that are easy to override */
:where(h1, h2, h3, h4) {
  line-height: var(--leading-tight);
}

/* :is() — takes specificity of most specific argument */
:is(.card, .panel) .title {
  font-weight: var(--font-weight-semibold);
}
```

Use `:where()` for base/reset styles. Use `:is()` when you want the specificity.

### `:has()` for parent selection

Powerful but use sparingly. Every `:has()` selector forces the browser to evaluate children, which can be expensive at scale.

```css
/* Style card differently when it has an image */
.card:has(> img) {
  grid-template-rows: auto 1fr;
}

/* Form field with error */
.field:has(.input:invalid) .label {
  color: var(--color-danger);
}
```

### `:not()` — prefer positive selectors

Write what something IS, not what it ISN'T.

```css
/* Prefer */
.item.active { ... }

/* Avoid when possible */
.item:not(.active) { ... }
```

`:not()` is appropriate for structural patterns:

```css
/* Gap between siblings — acceptable use of :not() */
.stack > :not(:first-child) {
  margin-top: var(--spacing-md);
}
```

## Property Declaration Order

Within a rule, order properties consistently. Follow this grouping:

```css
.element {
  /* 1. Layout */
  display: flex;
  position: relative;
  flex-direction: column;
  align-items: center;
  grid-template-columns: 1fr 2fr;
  gap: var(--spacing-md);

  /* 2. Box model */
  width: 100%;
  max-width: 40rem;
  min-height: 10rem;
  padding: var(--spacing-md);
  margin: 0 auto;

  /* 3. Typography */
  font-family: var(--font-sans);
  font-size: var(--font-size-base);
  font-weight: var(--font-weight-normal);
  line-height: var(--leading-normal);
  text-align: left;

  /* 4. Visual */
  color: var(--color-text);
  background: var(--color-bg-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  box-shadow: 0 1px 3px rgb(0 0 0 / 0.1);

  /* 5. Misc */
  cursor: pointer;
  opacity: 1;
  transition: opacity 150ms ease;
  pointer-events: auto;
}
```

Maintain this order across the entire codebase. It makes scanning declarations predictable.

## Cascade Layers (`@layer`)

Cascade layers provide explicit control over which styles win, independent of selector specificity. Define layer order once, then any rule in a higher-priority layer wins regardless of specificity.

```css
/* Define layer order — last layer has highest priority */
@layer reset, base, components, utilities;

/* Rules in each layer */
@layer reset {
  *, *::before, *::after { box-sizing: border-box; margin: 0; }
}

@layer base {
  body { font-family: var(--font-sans); color: var(--fg-primary); }
  h1, h2, h3 { line-height: var(--leading-tight); }
}

@layer components {
  .button { background: var(--button-bg); }
  .card { border-radius: var(--radius-lg); }
}

@layer utilities {
  .hidden { display: none !important; }
  .sr-only { position: absolute !important; }
}
```

### Rules

- **Unlayered styles beat all layers.** Styles outside any `@layer` always win. This is intentional — third-party styles you cannot control remain overridable.
- **Layer order = priority.** Later layers in the `@layer` declaration beat earlier ones.
- **Specificity only matters within the same layer.** A `.card .title` in `components` layer always loses to `.hidden` in `utilities` layer.
- **`@import` with layers**: `@import url('reset.css') layer(reset);`
- **Nested layers**: `@layer components.buttons { ... }` for fine-grained control.

### When to Use

- Eliminating `!important` hacks — move utility classes to a high-priority layer instead.
- Third-party CSS integration — import libraries into a lower layer so your styles always win.
- Design system architecture — resets → tokens → components → utilities as a clear cascade.

## Native CSS Nesting

CSS nesting is supported in all major browsers. It reduces repetition and co-locates related rules.

```css
.card {
  padding: var(--spacing-4);
  border-radius: var(--radius-lg);

  .title {
    font-weight: var(--font-weight-semibold);
  }

  .content {
    color: var(--fg-secondary);
  }

  &:hover {
    box-shadow: var(--shadow-md);
  }

  @media (min-width: 768px) {
    padding: var(--spacing-6);
  }
}
```

### Rules

- **`&` is required for pseudo-classes/elements and compound selectors**: `&:hover`, `&::before`, `&.active`.
- **`&` is optional for descendant selectors**: `.title` inside `.card` nests as `.card .title` automatically.
- **Max 3 levels of nesting** — same as the general nesting depth rule. Native nesting makes deep nesting tempting; resist it.
- **Specificity**: nested selectors have the specificity of the full expanded selector (`.card .title` = 0-2-0).
- **`@media` and `@container` can be nested** directly inside rule blocks.

## Selector Performance

Selectors are read right to left by the browser. Rightmost selector (key selector) matters most.

```css
/* Slow — key selector is *, matches everything then filters */
.container * { ... }

/* Fast — key selector is a class */
.card-title { ... }
```

Rules:
- Avoid universal selector (`*`) except in resets.
- Avoid deep descendant selectors: `.a .b .c .d` forces 4 ancestor checks per match.
- Class selectors are the fastest practical choice. Use them.
