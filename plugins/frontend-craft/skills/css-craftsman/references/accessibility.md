# CSS Accessibility

## DOM Order = Tab Order = Screen Reader Order

CSS `order`, `flex-direction: row-reverse`, `flex-direction: column-reverse`, and grid placement (`grid-row`, `grid-column`) only change **visual** order. Tab order and screen reader order always follow the DOM source order.

Rules:
- Never use CSS `order` to rearrange content that has a meaningful reading sequence
- If visual order differs from logical order, restructure the HTML
- `row-reverse` and `column-reverse` are acceptable only for purely decorative reordering (e.g., swapping icon position) where tab order is irrelevant

## Touch Targets

WCAG distinguishes minimum and enhanced target sizes:
- **WCAG 2.5.8 (AA)**: minimum target size is **24x24 CSS pixels** (with exceptions).
- **WCAG 2.5.5 (AAA)**: target size is **44x44 CSS pixels**.

This guide uses **44x44** as the default product baseline because it is safer for touch ergonomics.

Expand small interactive elements with padding, not by inflating the visible design:

```css
/* Small visible button, accessible touch target */
.iconButton {
  padding: 12px; /* expands touch target */
  margin: -12px; /* compensates layout impact if needed */
  min-width: 44px;
  min-height: 44px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}
```

For links within text, ensure the line height provides enough vertical target space. Keep interactive targets at 44x44px where possible; do not go below 24x24px unless a WCAG exception clearly applies.

## Font Sizes

Always use `rem` for font sizes. Never use `px`. This ensures user browser font-size preferences are respected.

```css
/* CORRECT */
.body { font-size: 1rem; }
.heading { font-size: 1.5rem; }
.small { font-size: 0.875rem; }

/* WRONG: ignores user preferences */
.body { font-size: 16px; }
```

Exception: borders, shadows, and outlines may use `px` because they are decorative and should not scale with font size.

## Line Height

Set body text line height to around **1.5** for readability. WCAG 1.4.12 focuses on supporting user-applied text spacing overrides (for example, line-height up to 1.5), not forcing a single default value.

```css
body { line-height: 1.5; }
```

Headings may use tighter line height (1.2-1.3) because large text is more readable at tighter spacing. Never go below 1.2.

## Focus Indicators

Never remove focus outlines without providing a visible replacement:

```css
/* WRONG: removes all focus indication */
:focus { outline: none; }

/* CORRECT: custom focus for keyboard users only */
:focus-visible {
  outline: 2px solid var(--color-focus);
  outline-offset: 2px;
}

/* Optional: remove default for mouse users */
:focus:not(:focus-visible) {
  outline: none;
}
```

Focus indicator requirements:
- Must have at least **3:1 contrast ratio** against the surrounding background
- Must be visible on all interactive elements (links, buttons, inputs, selects)
- Use `outline` over `box-shadow` for focus rings — outlines follow border-radius in modern browsers and are not clipped by `overflow: hidden`

## Hiding Elements

Choose the correct hiding technique based on who should perceive the element:

| Technique | Visible | In tab order | Screen reader |
|---|---|---|---|
| `display: none` | No | No | No |
| `visibility: hidden` | No | No | No |
| `sr-only` class | No | Yes (if focusable) | Yes |
| `aria-hidden="true"` | Yes | No (remove from tab) | No |
| `opacity: 0` | No | Yes | Yes |

The `sr-only` (screen-reader only) pattern:

```css
.srOnly {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border-width: 0;
}
```

Never use `display: none` to hide content that screen readers need. Never use `opacity: 0` as a general hiding mechanism — the element remains interactive.

## Color Contrast

### WCAG AA requirements

- **Normal text** (below 18px / below 14px bold): **4.5:1** contrast ratio minimum
- **Large text** (18px+ regular / 14px+ bold): **3:1** contrast ratio minimum
- **UI components and graphical objects**: **3:1** contrast ratio minimum (borders, icons, form controls)

### Rules

- Never rely on color alone to convey information. Always pair color with a secondary indicator: icon, text label, pattern, or underline
- Use CSS custom properties for all colors so they can be systematically audited:

```css
:root {
  --color-text: #1a1a1a;
  --color-text-secondary: #555555;
  --color-error: #d32f2f;
  --color-bg: #ffffff;
}
```

- Test contrast in browser DevTools (Elements panel > color swatch > contrast ratio)
- When creating hover/active states, verify the new color still meets contrast requirements
- Disabled elements are exempt from contrast requirements, but should still be distinguishable

## Reduced Motion

Always respect `prefers-reduced-motion`. See the performance reference for implementation patterns. In short: either disable all motion globally or only add motion when the user has not opted out.

## Scrolling and Overflow

- Never use `overflow: hidden` on `<body>` or `<html>` as a permanent style — it prevents scrolling
- When creating scroll containers, ensure they are keyboard-scrollable (add `tabindex="0"` and a label, or use a naturally focusable element)
- Use `scroll-behavior: smooth` only inside a `prefers-reduced-motion: no-preference` query

## References

- W3C WCAG 2.2 Understanding 2.5.8 Target Size (Minimum): https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html
- W3C WCAG 2.2 Understanding 2.5.5 Target Size (Enhanced): https://www.w3.org/WAI/WCAG22/Understanding/target-size-enhanced.html
- W3C WCAG 2.2 Understanding 1.4.12 Text Spacing: https://www.w3.org/WAI/WCAG22/Understanding/text-spacing.html
- W3C WCAG 2.2 Understanding 1.4.3 Contrast (Minimum): https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html
- MDN `:focus-visible`: https://developer.mozilla.org/docs/Web/CSS/:focus-visible
- MDN `prefers-reduced-motion`: https://developer.mozilla.org/docs/Web/CSS/@media/prefers-reduced-motion
