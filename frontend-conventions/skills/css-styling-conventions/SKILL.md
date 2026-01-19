---
name: CSS Styling Conventions
description: This skill should be used when the user asks to "write CSS", "style component", "review CSS", "fix styling", "add styles", or when writing/reviewing CSS in React applications with CSS Modules. Provides guidance on selector patterns, property ordering, layout patterns, and accessibility.
---

# CSS Styling Conventions

## Overview

This skill provides CSS coding conventions for React applications using CSS Modules. Focus is on maintainability, consistency, and accessibility while leveraging modern CSS features.

## Prerequisites

- CSS Modules for scoped styling
- Modern CSS features (Grid, Flexbox, custom properties)
- Mobile-first responsive design approach

## Selector Patterns

### Naming Convention: camelCase

Use camelCase for CSS class names (not kebab-case):

```css
/* Good - camelCase */
.buttonPrimary {
  background-color: blue;
}

/* Bad - kebab-case */
.button-primary {
  background-color: blue;
}
```

**Why:** Better integration with JavaScript/JSX where class names are accessed as object properties.

```tsx
// Clean access with camelCase
<button className={styles.buttonPrimary}>Click</button>

// Bracket notation needed with kebab-case
<button className={styles['button-primary']}>Click</button>
```

### Minimal Selector Specificity

Keep selectors as simple as possible:

```css
/* Bad - over-specific */
article.main p.box {
  border: 1px solid #fff;
}

/* Good - minimal specificity */
.box {
  border: 1px solid #fff;
}
```

### Avoid Deep Nesting

Don't mirror HTML structure in CSS:

```css
/* Bad - mirrors HTML hierarchy */
.card {
  .cardHeader {
    .cardTitle { ... }
  }
  .cardFooter {
    .footerNav {
      .footerLinks {
        li { ... }
      }
    }
  }
}

/* Good - flat structure */
.card { ... }
.cardTitle { ... }
.cardBody { ... }
.cardFooter { ... }
.footerNav { ... }
.footerLinks > li { ... }
```

### When Nesting is Appropriate

**Modifier states** (keep related styles together):

```css
.button {
  color: #333;

  &:hover {
    color: #000;
  }

  &:disabled {
    color: #999;
  }

  &.active {
    color: blue;
  }
}
```

**Strict HTML child relationships** (table, list):

```css
.dataTable {
  > thead > tr > th { ... }
  > tbody > tr > td { ... }
}

.navList > li { ... }
```

For detailed selector patterns, see `references/selector-patterns.md`.

## Property Ordering

### RECESS Order

Follow the RECESS property order (created by Bootstrap):

1. **Positioning** - position, top, right, bottom, left, z-index
2. **Display & Box Model** - display, flex, grid, width, height, margin, padding
3. **Typography** - font, color, text-align, line-height
4. **Visual** - background, border, opacity, shadow
5. **Animation** - animation, transition, transform

```css
.card {
  /* 1. Positioning */
  position: relative;
  z-index: 1;

  /* 2. Display & Box Model */
  display: flex;
  flex-direction: column;
  width: 100%;
  padding: 16px;

  /* 3. Typography */
  font-size: 14px;
  color: #333;

  /* 4. Visual */
  background-color: #fff;
  border: 1px solid #ddd;
  border-radius: 8px;

  /* 5. Animation */
  transition: box-shadow 0.2s;
}
```

Use Stylelint with `stylelint-config-recess-order` for automatic enforcement.

For complete property ordering details, see `references/property-ordering.md`.

## Layout Patterns

### Grid vs Flexbox

| Layout Type | Use |
|-------------|-----|
| 2D layout (rows AND columns) | Grid |
| 1D layout (row OR column) | Flexbox |
| Page layouts | Grid |
| Component internal alignment | Flexbox or Grid |

### Grid Layout

```css
/* Page layout */
.pageLayout {
  display: grid;
  grid-template-areas:
    "header header"
    "sidebar content"
    "footer footer";
  grid-template-columns: 200px 1fr;
}

.header { grid-area: header; }
.sidebar { grid-area: sidebar; }
.content { grid-area: content; }
.footer { grid-area: footer; }
```

### Flexbox Layout

```css
/* Horizontal alignment */
.toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 8px;
}

/* Vertical stack */
.cardContent {
  display: flex;
  flex-direction: column;
  gap: 16px;
}
```

### No Margin on Components

Components should not define their own outer margins:

```css
/* Bad - component defines its margin */
.card {
  margin: 16px;
}

/* Good - parent controls spacing with gap */
.cardGrid {
  display: grid;
  gap: 16px;
}
```

**Why:** Margin is external spacing that depends on context. Components shouldn't know their surrounding layout.

## Responsive Design

### Mobile-First

Always write base styles for mobile, then add breakpoints for larger screens:

```css
/* Bad - desktop-first */
@media (width <= 600px) {
  /* Mobile styles */
}

/* Good - mobile-first */
.container {
  /* Base mobile styles */
  padding: 16px;
}

@media (width >= 600px) {
  .container {
    /* Tablet and up */
    padding: 24px;
  }
}

@media (width >= 1024px) {
  .container {
    /* Desktop and up */
    padding: 32px;
  }
}
```

### Use `min-width` Consistently

Mobile-first means building up from small screens.

## Values and Variables

### Custom Properties for Design Tokens

```css
:root {
  /* Colors */
  --color-primary: #0066cc;
  --color-error: #cc0000;
  --color-text: #333333;

  /* Spacing */
  --spacing-sm: 8px;
  --spacing-md: 16px;
  --spacing-lg: 24px;

  /* Typography */
  --font-family-base: 'Inter', sans-serif;
  --font-size-base: 16px;
}

.button {
  background-color: var(--color-primary);
  padding: var(--spacing-sm) var(--spacing-md);
  font-family: var(--font-family-base);
}
```

### No Color Names

Use hex, rgb, or hsl values, not named colors:

```css
/* Bad - color names */
.error { color: red; }
.success { color: green; }

/* Good - hex values */
.error { color: #cc0000; }
.success { color: #00cc00; }
```

### Shorthand Properties

Use shorthand for box model properties:

```css
/* Good - shorthand */
.box {
  margin: 4px 8px 12px;
  padding: 16px 24px;
  inset: 0 0 auto auto;
}

/* Bad - longhand when shorthand works */
.box {
  margin-top: 4px;
  margin-right: 8px;
  margin-bottom: 12px;
  margin-left: 8px;
}
```

Avoid shorthand for complex properties like `font` or `background`:

```css
/* Bad - complex shorthand hides values */
.text {
  font: italic 1.2em "Fira Sans", serif;
  background: #cfcfcf;
}

/* Good - explicit properties */
.text {
  font-style: italic;
  font-size: 1.2em;
  font-family: "Fira Sans", serif;
  background-color: #cfcfcf;
}
```

## Transitions and Animations

### Explicit Transition Properties

Always specify which properties transition:

```css
/* Bad - transitions everything */
.card {
  transition: 0.2s;
}

/* Good - explicit property */
.card {
  transition: box-shadow 0.2s;
}
```

## Accessibility

### Preserve Outline

Never remove focus outlines without replacement:

```css
/* Bad - removes focus indicator */
button:focus {
  outline: none;
}

/* Good - custom focus style */
button:focus {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
}

/* Or use focus-visible for keyboard only */
button:focus-visible {
  outline: 2px solid var(--color-primary);
}
```

### Use ARIA Attributes for State Styling

```css
/* Good - style based on ARIA state */
.button:disabled {
  opacity: 0.5;
}

.input[aria-invalid="true"] {
  border-color: var(--color-error);
}

.accordion[aria-expanded="true"] .icon {
  transform: rotate(180deg);
}
```

### Parent-Child State Dependencies

Use `:is()` or `:where()` for parent-dependent styles:

```css
/* Child controls its own style based on parent state */
.child {
  color: #333;

  &:is(.parent:hover *) {
    color: #000;
  }
}
```

For comprehensive accessibility patterns, see `references/accessibility-patterns.md`.

## Things to Avoid

### Avoid !important

Rarely needed if CSS architecture is correct. If needed, indicates design problem.

### Avoid Base64 Images

Large file sizes, always downloaded, slow parsing.

### Avoid Over-Specific Selectors

Keep specificity low for maintainability.

## Quick Reference

**Selectors:**
- camelCase class names
- Minimal specificity
- Flat structure (avoid deep nesting)
- Nest modifiers and strict child relationships

**Properties:**
- RECESS order (positioning → display → typography → visual → animation)
- Shorthand for box model
- Explicit for complex properties
- Custom properties for design tokens

**Layout:**
- Grid for 2D layouts
- Flexbox for 1D layouts
- No margin on components (use parent gap)

**Responsive:**
- Mobile-first (min-width breakpoints)
- Base styles for mobile

**Accessibility:**
- Preserve focus outlines
- Use ARIA attributes for state styling

## Additional Resources

### Reference Files

For detailed patterns and examples, consult:
- **`references/selector-patterns.md`** - Complete selector patterns
- **`references/property-ordering.md`** - Full RECESS property order
- **`references/accessibility-patterns.md`** - Accessibility best practices
