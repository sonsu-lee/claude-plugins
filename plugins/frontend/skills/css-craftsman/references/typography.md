# Typography

## Font Stacks

Use system fonts as the default. Only load web fonts when the design explicitly requires a specific typeface.

```css
:root {
  --font-sans: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto,
    'Helvetica Neue', Arial, sans-serif, 'Apple Color Emoji', 'Segoe UI Emoji';
  --font-mono: ui-monospace, 'Cascadia Code', 'Source Code Pro',
    'Fira Code', Menlo, Consolas, monospace;
  --font-serif: Georgia, Cambria, 'Times New Roman', Times, serif;
}
```

When loading web fonts:
- Use `font-display: swap` to prevent invisible text during load.
- Subset fonts to only the character sets needed.
- Preload critical font files: `<link rel="preload" href="font.woff2" as="font" type="font/woff2" crossorigin>`.
- Prefer `woff2` format. It has the best compression and broadest support.

## Type Scale

Define all font sizes as tokens using `rem`. Never use `px` for font sizes.

```css
:root {
  --font-size-xs: 0.75rem;    /* 12px */
  --font-size-sm: 0.875rem;   /* 14px */
  --font-size-base: 1rem;     /* 16px */
  --font-size-lg: 1.125rem;   /* 18px */
  --font-size-xl: 1.25rem;    /* 20px */
  --font-size-2xl: 1.5rem;    /* 24px */
  --font-size-3xl: 1.875rem;  /* 30px */
  --font-size-4xl: 2.25rem;   /* 36px */
  --font-size-5xl: 3rem;      /* 48px */
}
```

Always reference the scale: `font-size: var(--font-size-lg)`. Never use arbitrary sizes like `font-size: 1.1rem`.

## Responsive Typography

Use `clamp()` for fluid sizing. This scales smoothly between breakpoints without media queries.

```css
.heading {
  /* Minimum 1.5rem, preferred 1.5rem + 1.5vw, maximum 3rem */
  font-size: clamp(1.5rem, 1.2rem + 1.5vw, 3rem);
}

.body {
  font-size: clamp(1rem, 0.95rem + 0.25vw, 1.125rem);
}
```

Rules:
- Never use viewport units alone (`font-size: 3vw`). Text will be unreadably small on mobile and oversized on large screens.
- The minimum value in `clamp()` must be readable (at least `0.875rem` / 14px for body text).
- Test at 320px and 1920px viewport widths to verify bounds.

## Line Height

Use unitless values. Never use `px`, `rem`, or `%` for line-height.

```css
:root {
  --leading-tight: 1.15;
  --leading-snug: 1.3;
  --leading-normal: 1.5;
  --leading-relaxed: 1.65;
}
```

Scale inversely with font size:
- **Body text** (14–18px): `line-height: 1.5` to `1.6` for readability.
- **Headings** (24px+): `line-height: 1.1` to `1.3` — tighter for visual weight.
- **Small text** (12px): `line-height: 1.5` to `1.65` — looser for legibility.

## Font Weight

Define weight tokens and use them consistently.

```css
:root {
  --font-weight-normal: 400;
  --font-weight-medium: 500;
  --font-weight-semibold: 600;
  --font-weight-bold: 700;
}
```

Verify that loaded web fonts include the weights you reference. Missing weights cause the browser to synthesize bold/italic, which looks poor.

## Text Truncation

### Single-line truncation

```css
.truncate {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  max-width: 100%; /* Must have a width constraint */
}
```

### Multi-line truncation

```css
.line-clamp-3 {
  overflow: hidden;
  line-clamp: 3;
  -webkit-line-clamp: 3; /* fallback for engines still using prefixed behavior */
  display: -webkit-box;
  -webkit-box-orient: vertical;
  max-width: 100%;
}
```

Rules:
- Always set `max-width` or an equivalent width constraint on truncated elements. Truncation without width constraints does nothing.
- In flex containers, add `min-width: 0` on the flex child for truncation to work.
- For modern engines, prefer standard `line-clamp` and keep prefixed declarations for compatibility.

## Line Length

Constrain reading width for prose content. Optimal line length is 45-75 characters.

```css
.prose {
  max-width: 65ch;
}
```

Use `ch` units for line length. They scale with font size automatically.

## Vertical Rhythm

Maintain consistent spacing between text blocks. Base spacing on line-height.

```css
.prose > * + * {
  margin-top: 1.5em; /* Matches body line-height */
}

.prose > h2 + * {
  margin-top: 0.75em; /* Tighter after headings */
}

.prose > * + h2 {
  margin-top: 2em; /* More space before headings */
}
```

Use `em` for text-adjacent spacing so it scales with the element's font size.

## Letter Spacing

- Headings in all-caps: add `letter-spacing: 0.05em` for readability.
- Large headings (36px+): slight negative tracking `letter-spacing: -0.02em` can improve visual density.
- Body text: leave at default. Do not adjust letter-spacing on paragraph text.

## Text Box Trimming

Font metrics add extra space above and below glyphs. `text-box` trims this space for precise optical alignment:

```css
@supports (text-box: trim-both cap alphabetic) {
  h1, h2, h3, button {
    text-box: trim-both cap alphabetic;
  }
}
```

- `trim-both` — trims top and bottom.
- `cap` — top edge aligns to capital letter height.
- `alphabetic` — bottom edge aligns to alphabetic baseline.

This solves the "button text centering" problem — true optical vertical centering without magic-number padding. Progressive enhancement — no visual change in unsupported browsers.

## Text Wrap

```css
h1, h2, h3, h4, h5, h6 {
  text-wrap: balance;     /* Distributes text evenly across lines */
}

p, li, dd, blockquote, figcaption {
  text-wrap: pretty;      /* Avoids orphans on the last line */
  max-inline-size: 88ch;  /* Readable line length with logical property */
}
```

Both are progressive enhancements with no visual degradation in unsupported browsers. Use feature queries when you need strict support gating.

## Logical Properties

Default to logical properties for internationalization support:

```css
/* Physical (avoid by default) */
margin-right → margin-inline-end
padding-left → padding-inline-start
width → inline-size
height → block-size
top → inset-block-start
bottom → inset-block-end

/* Logical properties work correctly in RTL and vertical writing modes */
.element {
  margin-inline: auto;        /* replaces margin-left: auto; margin-right: auto */
  padding-block: var(--spacing-4);  /* replaces padding-top + padding-bottom */
  inline-size: 100%;          /* replaces width: 100% */
  max-inline-size: 65ch;      /* replaces max-width: 65ch */
}
```

**When physical properties ARE necessary:**
- Transform functions: `translateX()`, `scaleX()` (no logical equivalents)
- Media queries: `@media (width < 30rem)` (no `inline-size` version)
- Gradient directions: `linear-gradient(to top, ...)`
- Physically-anchored UI: chat widget pinned to bottom-right of viewport

## Anti-aliasing

Set globally for consistency:

```css
body {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
```

This produces thinner, crisper text on macOS. Apply it once on the body, not per-element.

## References

- MDN `text-box`: https://developer.mozilla.org/docs/Web/CSS/text-box
- MDN `text-wrap`: https://developer.mozilla.org/docs/Web/CSS/text-wrap
- MDN `line-height`: https://developer.mozilla.org/docs/Web/CSS/line-height
- MDN CSS logical properties: https://developer.mozilla.org/docs/Web/CSS/CSS_logical_properties_and_values
