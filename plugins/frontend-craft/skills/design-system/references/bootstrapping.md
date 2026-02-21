# Design System Bootstrapping

## Overview

This guide covers building a design system from scratch — what tokens to create, what values to use, in what order, and how to classify them semantically. Follow this guide when starting a new design system or rebuilding one from the ground up.

## Token Creation Order

Create tokens in this order. Each layer depends on the previous one.

### Phase 1: Primitive Color Palette

Generate a full color palette first. Every other token layer references these.

**Core palette structure:**

```css
:root {
  /* Neutral scale — used for text, backgrounds, borders */
  --color-gray-50:  #f9fafb;
  --color-gray-100: #f3f4f6;
  --color-gray-200: #e5e7eb;
  --color-gray-300: #d1d5db;
  --color-gray-400: #9ca3af;
  --color-gray-500: #6b7280;
  --color-gray-600: #4b5563;
  --color-gray-700: #374151;
  --color-gray-800: #1f2937;
  --color-gray-900: #111827;
  --color-gray-950: #030712;

  /* Brand primary — 50 through 950, 10 stops minimum */
  --color-blue-50:  #eff6ff;
  --color-blue-100: #dbeafe;
  /* ... full scale ... */
  --color-blue-900: #1e3a8a;

  /* Functional colors — red (error), green (success), yellow (warning) */
  /* Same 50-900 scale per hue */

  /* Static colors */
  --color-white: #ffffff;
  --color-black: #000000;
}
```

**Scale design rules:**
- Minimum 10 stops per hue (50, 100, 200, 300, 400, 500, 600, 700, 800, 900). Add 950 for very dark shades if needed.
- 50 is the lightest tint (backgrounds), 500 is the base, 900+ is the darkest shade (text on light).
- Ensure sufficient contrast within each scale: 50 vs 900 should meet WCAG AAA (7:1).
- Neutral gray scale is the most used — invest extra time in even perceptual spacing.

**Palette generation approach:**
1. Start with the brand color as the 500 stop.
2. Generate lighter stops (50–400) by decreasing saturation and increasing lightness.
3. Generate darker stops (600–900) by shifting hue slightly toward blue/violet and decreasing lightness.
4. Test each stop against white and black backgrounds for contrast ratios.
5. Validate that adjacent stops (e.g., 300 vs 400) are visually distinguishable.

**OKLCH-based palette generation (alternative):**

Instead of hand-picking each stop, use relative color syntax to derive an entire scale from a single base:

```css
:root {
  --base-brand: oklch(55% 0.2 260);

  --brand-50:  oklch(from var(--base-brand) calc(l + 0.4) calc(c * 0.3) h);
  --brand-100: oklch(from var(--base-brand) calc(l + 0.35) calc(c * 0.5) h);
  --brand-200: oklch(from var(--base-brand) calc(l + 0.25) calc(c * 0.7) h);
  --brand-300: oklch(from var(--base-brand) calc(l + 0.15) c h);
  --brand-400: oklch(from var(--base-brand) calc(l + 0.05) c h);
  --brand-500: var(--base-brand);
  --brand-600: oklch(from var(--base-brand) calc(l - 0.05) c h);
  --brand-700: oklch(from var(--base-brand) calc(l - 0.15) c h);
  --brand-800: oklch(from var(--base-brand) calc(l - 0.25) c h);
  --brand-900: oklch(from var(--base-brand) calc(l - 0.35) calc(c * 0.8) h);
}
```

OKLCH is perceptually uniform — equal lightness steps produce visually equal brightness changes across all hues. Lighter stops reduce chroma for pastels; darker stops slightly reduce chroma to avoid oversaturation. Change one base value and the entire scale updates.

### Phase 2: Primitive Spacing Scale

Spacing tokens control all margin, padding, gap, and size values.

```css
:root {
  --spacing-0:   0;
  --spacing-0-5: 0.125rem;  /* 2px */
  --spacing-1:   0.25rem;   /* 4px */
  --spacing-1-5: 0.375rem;  /* 6px */
  --spacing-2:   0.5rem;    /* 8px */
  --spacing-3:   0.75rem;   /* 12px */
  --spacing-4:   1rem;      /* 16px */
  --spacing-5:   1.25rem;   /* 20px */
  --spacing-6:   1.5rem;    /* 24px */
  --spacing-8:   2rem;      /* 32px */
  --spacing-10:  2.5rem;    /* 40px */
  --spacing-12:  3rem;      /* 48px */
  --spacing-16:  4rem;      /* 64px */
  --spacing-20:  5rem;      /* 80px */
  --spacing-24:  6rem;      /* 96px */
}
```

**Scale design rules:**
- Use a 4px base grid. Every value should be a multiple of 4px (except 2px and 6px for fine adjustments).
- Dense at the small end (2, 4, 6, 8, 12, 16), wider gaps at the large end (32, 48, 64, 80, 96).
- Use `rem` units. Never `px` in token values — this allows user font-size scaling to propagate.
- The scale should cover the range from tight inline spacing (2px) to page-level section gaps (96px).

### Phase 3: Primitive Typography Scale

```css
:root {
  /* Font families */
  --font-sans: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, sans-serif;
  --font-mono: 'JetBrains Mono', 'Fira Code', monospace;

  /* Font sizes — modular scale or explicit steps */
  --font-size-xs:   0.75rem;   /* 12px */
  --font-size-sm:   0.875rem;  /* 14px */
  --font-size-base: 1rem;      /* 16px */
  --font-size-lg:   1.125rem;  /* 18px */
  --font-size-xl:   1.25rem;   /* 20px */
  --font-size-2xl:  1.5rem;    /* 24px */
  --font-size-3xl:  1.875rem;  /* 30px */
  --font-size-4xl:  2.25rem;   /* 36px */

  /* Line heights */
  --leading-tight:  1.25;
  --leading-snug:   1.375;
  --leading-normal: 1.5;
  --leading-relaxed: 1.625;

  /* Font weights */
  --font-weight-regular:  400;
  --font-weight-medium:   500;
  --font-weight-semibold: 600;
  --font-weight-bold:     700;

  /* Letter spacing */
  --tracking-tight:  -0.025em;
  --tracking-normal:  0;
  --tracking-wide:    0.025em;
}
```

**Scale design rules:**
- Use a limited set of sizes (8–10 stops). More than 10 font sizes usually signals inconsistency.
- Pair each font size with a recommended line height. Smaller text needs more relative line height (1.5+), headings need less (1.2–1.3).
- Define font weight tokens rather than using numeric values directly. Limit to 3–4 weights.

### Phase 4: Primitive Border and Shadow Tokens

```css
:root {
  /* Border radius */
  --radius-none: 0;
  --radius-sm:   0.25rem;   /* 4px */
  --radius-md:   0.375rem;  /* 6px */
  --radius-lg:   0.5rem;    /* 8px */
  --radius-xl:   0.75rem;   /* 12px */
  --radius-2xl:  1rem;      /* 16px */
  --radius-full: 9999px;

  /* Border widths */
  --border-width-default: 1px;
  --border-width-thick:   2px;

  /* Shadows */
  --shadow-sm:  0 1px 2px rgba(0, 0, 0, 0.05);
  --shadow-md:  0 4px 6px -1px rgba(0, 0, 0, 0.1);
  --shadow-lg:  0 10px 15px -3px rgba(0, 0, 0, 0.1);
  --shadow-xl:  0 20px 25px -5px rgba(0, 0, 0, 0.1);
}
```

### Phase 5: Semantic Tokens

Semantic tokens assign purpose to primitive values. This is the most critical layer — it determines how well the system adapts to theming.

**Semantic classification approach — classify by role, not by visual property:**

```css
/* tokens/semantic.css */
:root {
  /* ── Background ── */
  --bg-primary:     var(--color-white);
  --bg-secondary:   var(--color-gray-50);
  --bg-tertiary:    var(--color-gray-100);
  --bg-inverse:     var(--color-gray-900);
  --bg-brand:       var(--color-blue-500);
  --bg-success:     var(--color-green-50);
  --bg-warning:     var(--color-yellow-50);
  --bg-danger:      var(--color-red-50);
  --bg-overlay:     rgba(0, 0, 0, 0.5);

  /* ── Foreground (text/icons) ── */
  --fg-primary:     var(--color-gray-900);
  --fg-secondary:   var(--color-gray-600);
  --fg-tertiary:    var(--color-gray-400);
  --fg-inverse:     var(--color-white);
  --fg-brand:       var(--color-blue-600);
  --fg-success:     var(--color-green-600);
  --fg-warning:     var(--color-yellow-600);
  --fg-danger:      var(--color-red-600);
  --fg-disabled:    var(--color-gray-300);
  --fg-link:        var(--color-blue-600);

  /* ── Border ── */
  --border-default:    var(--color-gray-200);
  --border-strong:     var(--color-gray-400);
  --border-brand:      var(--color-blue-500);
  --border-danger:     var(--color-red-500);
  --border-focus:      var(--color-blue-500);

  /* ── Interactive (buttons, links, controls) ── */
  --interactive-primary:       var(--color-blue-600);
  --interactive-primary-hover: var(--color-blue-700);
  --interactive-primary-active: var(--color-blue-800);
  --interactive-secondary:       var(--color-gray-100);
  --interactive-secondary-hover: var(--color-gray-200);
  --interactive-danger:          var(--color-red-600);
  --interactive-danger-hover:    var(--color-red-700);
  --interactive-disabled:        var(--color-gray-100);

  /* ── Spacing (semantic aliases) ── */
  --space-component-gap:  var(--spacing-2);   /* gap inside components */
  --space-element-gap:    var(--spacing-4);   /* gap between elements */
  --space-section-gap:    var(--spacing-8);   /* gap between sections */
  --space-page-gap:       var(--spacing-16);  /* gap between page sections */
  --space-inset-sm:       var(--spacing-2);   /* small padding */
  --space-inset-md:       var(--spacing-4);   /* medium padding */
  --space-inset-lg:       var(--spacing-6);   /* large padding */

  /* ── Typography (semantic compositions) ── */
  --text-heading-size:    var(--font-size-2xl);
  --text-heading-weight:  var(--font-weight-bold);
  --text-heading-leading: var(--leading-tight);

  --text-body-size:       var(--font-size-base);
  --text-body-weight:     var(--font-weight-regular);
  --text-body-leading:    var(--leading-normal);

  --text-caption-size:    var(--font-size-sm);
  --text-caption-weight:  var(--font-weight-regular);
  --text-caption-leading: var(--leading-normal);

  /* ── Elevation ── */
  --elevation-low:    var(--shadow-sm);
  --elevation-mid:    var(--shadow-md);
  --elevation-high:   var(--shadow-lg);
  --elevation-overlay: var(--shadow-xl);
}
```

**Semantic naming principles:**

| Category | Pattern | Examples |
|----------|---------|----------|
| Background | `--bg-{role}` | `--bg-primary`, `--bg-danger`, `--bg-overlay` |
| Foreground | `--fg-{role}` | `--fg-primary`, `--fg-link`, `--fg-disabled` |
| Border | `--border-{role}` | `--border-default`, `--border-focus` |
| Interactive | `--interactive-{variant}-{state}` | `--interactive-primary-hover` |
| Spacing | `--space-{context}` | `--space-section-gap`, `--space-inset-md` |
| Typography | `--text-{role}-{property}` | `--text-heading-size`, `--text-body-weight` |
| Elevation | `--elevation-{level}` | `--elevation-low`, `--elevation-overlay` |

**Choosing the right semantic category:**

Ask these questions in order:
1. **What role does this value serve?** Background, foreground, border, interactive surface, spacing, or elevation?
2. **What priority level?** Primary, secondary, tertiary — or a specific intent like brand, danger, success?
3. **Does it have states?** If it's interactive, add hover/active/disabled/focus variants.

Do NOT name by visual appearance (`--color-light-blue`, `--big-padding`). Name by function (`--bg-brand`, `--space-section-gap`).

### Phase 6: Dark Theme

After semantic tokens are defined, dark theme is a single override layer:

```css
[data-theme="dark"] {
  --bg-primary:     var(--color-gray-950);
  --bg-secondary:   var(--color-gray-900);
  --bg-tertiary:    var(--color-gray-800);
  --bg-inverse:     var(--color-white);

  --fg-primary:     var(--color-gray-50);
  --fg-secondary:   var(--color-gray-400);
  --fg-tertiary:    var(--color-gray-500);
  --fg-inverse:     var(--color-gray-900);
  --fg-disabled:    var(--color-gray-600);

  --border-default: var(--color-gray-700);
  --border-strong:  var(--color-gray-500);

  --interactive-secondary:       var(--color-gray-800);
  --interactive-secondary-hover: var(--color-gray-700);
  --interactive-disabled:        var(--color-gray-800);

  --bg-success:     rgba(34, 197, 94, 0.1);
  --bg-warning:     rgba(234, 179, 8, 0.1);
  --bg-danger:      rgba(239, 68, 68, 0.1);

  --elevation-low:  0 1px 2px rgba(0, 0, 0, 0.3);
  --elevation-mid:  0 4px 6px rgba(0, 0, 0, 0.4);
  --elevation-high: 0 10px 15px rgba(0, 0, 0, 0.5);
}
```

**Dark theme rules:**
- Override ONLY semantic tokens. Never override primitives in dark mode.
- Every semantic color token should have a dark override. Missing overrides = theme gaps.
- Shadows need separate dark overrides (stronger opacity, since dark backgrounds absorb shadows).
- Don't just invert colors. Dark mode backgrounds use gray-800/900/950 — not pure black.

**Modern dark mode techniques:**

Support is uneven across older browsers, so treat the following as progressive enhancement and keep semantic-token fallbacks in place.

**`color-scheme` declaration** — honors OS preference automatically, enabling dark scrollbars and form controls:

```css
html { color-scheme: light dark; }
```

**`light-dark()` function** — inline mode-aware values without media queries. Set `color-scheme: light dark` (typically on `:root` or `html`) so `light-dark()` resolves against an explicit light/dark preference. Keep a fallback declaration before `light-dark()` when supporting browsers that do not implement it:

```css
html { color-scheme: light dark; }  /* Needed for reliable light-dark() behavior */

.card {
  background: var(--gray-1); /* Fallback */
  color: var(--gray-9);      /* Fallback */
  background: light-dark(var(--gray-1), var(--gray-9));
  color: light-dark(var(--gray-9), var(--gray-1));
}
```

**System colors** — auto-adapt to light/dark modes:

```css
button {
  background: CanvasText;   /* Text color = dark in light mode, light in dark mode */
  color: Canvas;            /* Background color = light in light mode, dark in dark mode */
}
```

**Single-variable color adjustment** — instead of maintaining two entire palettes, use a single OKLCH lightness adjuster:

```css
html {
  color-scheme: light dark;
  --color-adjust: -0.1;
  @media (prefers-color-scheme: light) {
    --color-adjust: 0.133;
  }
}

.accent {
  color: oklch(calc(0.75 - var(--color-adjust)) 0.2 328);
}
```

**`currentColor` for icon theming:**

```css
svg.icon { fill: currentColor; }
/* Icons automatically match parent text color across themes */
```

Combine with relative color syntax for derived shadows:

```css
.icon {
  filter: drop-shadow(0 1px 0 oklch(from currentColor calc(l - 0.25) c h));
}
```

## Component Build Order

Build foundational components before composite ones. Each phase builds on the previous.

### Phase 1: Foundation Components

These are the atomic building blocks that almost every other component depends on.

1. **Button** — The most used interactive element. Establishes size scale, variant pattern, disabled/loading states.
2. **Input / TextField** — Establishes form control sizing, focus ring, error/disabled states.
3. **Icon** — SVG icon wrapper. Establishes icon sizing relative to text.
4. **Typography** (Text, Heading) — Optional as a component but useful for enforcing text styles.

### Phase 2: Form Components

Build after Phase 1 because these compose Button, Input, and Icon.

5. **Checkbox** — Single toggle. Establishes toggle pattern.
6. **Radio** — Group selection. Similar to Checkbox but mutually exclusive.
7. **Select / Dropdown** — Combines Input trigger + dropdown listbox.
8. **Switch / Toggle** — On/off control.
9. **Textarea** — Multi-line input.

### Phase 3: Layout & Feedback Components

10. **Badge / Tag** — Small status or label indicator.
11. **Divider** — Horizontal/vertical separator.
12. **Tooltip** — Floating text hint. Establishes positioning logic (reused by Dropdown, Popover).
13. **Toast / Notification** — Feedback messages. Establishes stacking and animation.
14. **Modal / Dialog** — Overlay with focus trap. Establishes overlay pattern.

### Phase 4: Composite Components

15. **Tabs** — Panel switching. Composes with other components.
16. **Accordion** — Collapsible sections.
17. **Table** — Data display with sorting, pagination.
18. **Card** — Content container with flexible slots.
19. **Pagination** — Page navigation.
20. **Navigation** — Header, sidebar, breadcrumb.

## File Structure

Recommended file organization for a new design system:

```
tokens/
  primitive/
    colors.css
    spacing.css
    typography.css
    borders.css
    shadows.css
  semantic/
    colors.css        (bg, fg, border, interactive)
    spacing.css       (gap, inset aliases)
    typography.css    (heading, body, caption)
    elevation.css     (shadow aliases)
  themes/
    dark.css          (semantic overrides for dark mode)
  index.css           (imports all token files in correct order)
```

**Import order matters.** Primitives first, then semantics (which reference primitives), then themes (which override semantics).

## Checklist

Before considering the design system bootstrapped:

- [ ] Primitive color palette: neutral + brand + functional hues, each with 10+ stops
- [ ] Primitive spacing scale: 4px grid, 2px to 96px coverage
- [ ] Primitive typography: families, 8–10 sizes, 3–4 weights, line heights, letter spacing
- [ ] Primitive borders and shadows: radius scale, border widths, shadow scale
- [ ] Semantic tokens: bg, fg, border, interactive, spacing, typography, elevation
- [ ] Dark theme overrides for all semantic color tokens
- [ ] Token files organized by layer with correct import order
- [ ] At least Button and Input components built using tokens to validate the system works end-to-end
- [ ] `color-scheme: light dark` in base styles for automatic scrollbar/form adaptation
- [ ] `@property` registration for critical color tokens (type safety + animation support)
- [ ] `interpolate-size: allow-keywords` in base styles (progressive enhancement; unsupported browsers simply skip intrinsic-size animation)
- [ ] `text-wrap: balance` on headings, `text-wrap: pretty` on body text (progressive enhancement)

## References

- MDN `color-scheme`: https://developer.mozilla.org/docs/Web/CSS/color-scheme
- MDN `light-dark()`: https://developer.mozilla.org/docs/Web/CSS/color_value/light-dark
- MDN CSS system colors: https://developer.mozilla.org/docs/Web/CSS/system-color
- MDN `@property`: https://developer.mozilla.org/docs/Web/CSS/@property
- MDN `interpolate-size`: https://developer.mozilla.org/docs/Web/CSS/interpolate-size
- MDN `text-wrap`: https://developer.mozilla.org/docs/Web/CSS/text-wrap
