# Modern CSS (Spec-Aligned, Progressive)

This guide lists modern CSS APIs that are strongly recommended when they reduce complexity and improve maintainability.

Always apply progressive enhancement:
- Keep a safe default path.
- Add modern behavior with `@supports` or layered overrides.
- Validate feature choice against `references/release-window.md`.

## 1) Cascade Layers (`@layer`)

Use layers to control cascade order without specificity wars.

```css
@layer reset, base, components, utilities;

@layer components {
  .button {
    border-radius: var(--radius-md);
  }
}
```

Rules:
- Declare layer order once near the top of the stylesheet.
- Prefer layer order over `!important`.

## 2) Container Queries (`@container`)

Use container queries for component-level responsiveness.

```css
.cardContainer {
  container-type: inline-size;
}

@container (min-width: 28rem) {
  .card {
    display: grid;
    grid-template-columns: 8rem minmax(0, 1fr);
  }
}
```

Rules:
- Apply to reusable components that can appear in multiple layout contexts.
- Keep viewport media queries for page-level shell changes.

## 3) Subgrid (`subgrid`)

Use subgrid when nested content must align exactly to parent tracks.

```css
.parentGrid {
  display: grid;
  grid-template-columns: 12rem minmax(0, 1fr);
}

.childGrid {
  display: grid;
  grid-template-columns: subgrid;
  grid-column: 1 / -1;
}
```

Fallback pattern:
- Default to explicit local tracks.
- Upgrade with `@supports (grid-template-columns: subgrid)`.

## 4) Parent-Aware Selectors (`:has()`)

Use `:has()` for parent-state styling to remove JavaScript-only state classes.

```css
.field:has(input:focus-visible) {
  outline: 2px solid var(--color-focus);
}
```

Rules:
- Prefer for local parent-state styling.
- Avoid broad selectors with heavy subtree matching.

## 5) Truncation with `line-clamp`

Use standard `line-clamp` first, keep prefixed fallback.

```css
.summary {
  overflow: hidden;
  line-clamp: 3;
  -webkit-line-clamp: 3;
  display: -webkit-box;
  -webkit-box-orient: vertical;
}
```

Rules:
- Ensure width constraints are present in parent layout.
- In flex contexts, add `min-width: 0` on shrinkable items.

## 6) Better Wrapping (`text-wrap`)

Use `text-wrap: balance` for headings and `pretty` for long text blocks.

```css
h1, h2, h3 {
  text-wrap: balance;
}

p {
  text-wrap: pretty;
}
```

## 7) Modern Color APIs (`oklch`, `color-mix`, `light-dark`)

Prefer perceptual color spaces and native light/dark switching.

```css
:root {
  color-scheme: light dark;
  --surface: light-dark(oklch(0.98 0.01 250), oklch(0.22 0.02 250));
  --surface-hover: color-mix(in oklab, var(--surface), black 8%);
}
```

Fallback pattern:
- Define stable fallback tokens first.
- Layer modern color functions in `@supports` blocks when needed.

## 8) Scoped Styles (`@scope`)

Use `@scope` for local cascade boundaries instead of deep selector nesting.

```css
@scope (.profileCard) {
  .title {
    margin: 0;
  }
}
```

Rules:
- Useful for large components where leakage risk is high.
- Keep CSS Modules as the first isolation layer in this repo.
- Treat as Tier B unless release-window checks confirm all target engines.

## 9) Overflow Clipping (`overflow: clip`)

Prefer `clip` over `hidden` when you only need clipping.

```css
.card {
  overflow: clip;
}
```

Rules:
- Use `hidden` only when you intentionally need BFC side-effects.

## 10) Release-Window Emerging Features

These features appeared in current-cycle browser release notes and should be treated as Tier B until compatibility is confirmed for your exact targets:
- CSS `if()` function
- `shape()` function
- `sibling-index()` and related newer selector/math helpers
- newer anchor positioning refinements

Adoption rule:
- Use only when it removes meaningful complexity.
- Include explicit fallback snippet.
- Verify behavior with text diagnostics (`css-inspector`).

## Adoption Checklist

When introducing modern APIs:
- Add fallback behavior first.
- Keep selectors and layout model simple.
- Verify in text-based DOM diagnostics (`css-inspector`) after change.
- Avoid shipping experimental features without a controlled fallback path.

## References

- MDN `@layer`: https://developer.mozilla.org/docs/Web/CSS/@layer
- MDN container queries: https://developer.mozilla.org/docs/Web/CSS/CSS_containment/Container_queries
- MDN subgrid: https://developer.mozilla.org/docs/Web/CSS/CSS_grid_layout/Subgrid
- MDN `:has()`: https://developer.mozilla.org/docs/Web/CSS/:has
- MDN `line-clamp`: https://developer.mozilla.org/docs/Web/CSS/line-clamp
- MDN `text-wrap`: https://developer.mozilla.org/docs/Web/CSS/text-wrap
- MDN `color-mix()`: https://developer.mozilla.org/docs/Web/CSS/color_value/color-mix
- MDN `light-dark()`: https://developer.mozilla.org/docs/Web/CSS/color_value/light-dark
- MDN `@scope`: https://developer.mozilla.org/docs/Web/CSS/@scope
- New in Chrome 140: https://developer.chrome.com/blog/new-in-chrome-140/
- Firefox 136 for developers: https://developer.mozilla.org/en-US/docs/Mozilla/Firefox/Releases/136
- Safari 18.4 (WebKit features): https://webkit.org/blog/16574/webkit-features-in-safari-18-4/
