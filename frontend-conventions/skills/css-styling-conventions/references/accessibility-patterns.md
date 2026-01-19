# CSS Accessibility Patterns

## Focus Management

### Never Remove Focus Outline

Focus indicators are essential for keyboard navigation:

```css
/* Bad - removes accessibility */
button:focus {
  outline: none;
}

input:focus {
  outline: 0;
}

/* Bad - hides focus */
*:focus {
  outline: none;
}
```

### Custom Focus Styles

Replace default outline with visible custom style:

```css
/* Good - visible custom focus */
button:focus {
  outline: 2px solid #0066cc;
  outline-offset: 2px;
}

/* Good - focus ring with shadow */
input:focus {
  outline: none;
  box-shadow: 0 0 0 3px rgba(0, 102, 204, 0.4);
}
```

### focus-visible for Keyboard Only

Show focus only for keyboard navigation:

```css
/* Mouse clicks: no focus ring */
button:focus {
  outline: none;
}

/* Keyboard navigation: show focus ring */
button:focus-visible {
  outline: 2px solid #0066cc;
  outline-offset: 2px;
}
```

### Focus Within

Style parent when child has focus:

```css
.searchBox {
  border: 1px solid #dddddd;
}

.searchBox:focus-within {
  border-color: #0066cc;
  box-shadow: 0 0 0 3px rgba(0, 102, 204, 0.2);
}
```

## ARIA State Styling

### Disabled State

Style based on `:disabled` pseudo-class:

```css
button:disabled {
  background-color: #cccccc;
  color: #666666;
  cursor: not-allowed;
  opacity: 0.6;
}

input:disabled {
  background-color: #f5f5f5;
  color: #999999;
  cursor: not-allowed;
}
```

### Invalid State

Style based on `aria-invalid` attribute:

```css
/* Using ARIA attribute */
input[aria-invalid="true"] {
  border-color: #cc0000;
  background-color: #fff5f5;
}

input[aria-invalid="true"]:focus {
  box-shadow: 0 0 0 3px rgba(204, 0, 0, 0.2);
}

/* With error icon */
.inputWrapper:has(input[aria-invalid="true"])::after {
  content: '⚠';
  position: absolute;
  right: 12px;
  color: #cc0000;
}
```

### Expanded State

Style based on `aria-expanded` attribute:

```css
.accordion {
  border: 1px solid #dddddd;
}

.accordionButton[aria-expanded="true"] {
  background-color: #f5f5f5;
}

.accordionIcon {
  transition: transform 0.2s ease-in-out;
}

.accordionButton[aria-expanded="true"] .accordionIcon {
  transform: rotate(180deg);
}

.accordionPanel {
  display: none;
}

.accordionButton[aria-expanded="true"] + .accordionPanel {
  display: block;
}
```

### Selected State

Style based on `aria-selected` attribute:

```css
.tab {
  padding: 12px 24px;
  border-bottom: 2px solid transparent;
  color: #666666;
}

.tab[aria-selected="true"] {
  border-bottom-color: #0066cc;
  color: #0066cc;
  font-weight: 500;
}
```

### Pressed State

Style toggle buttons based on `aria-pressed`:

```css
.toggleButton {
  background-color: #eeeeee;
  color: #333333;
}

.toggleButton[aria-pressed="true"] {
  background-color: #0066cc;
  color: #ffffff;
}
```

### Hidden State

Style based on `aria-hidden`:

```css
[aria-hidden="true"] {
  display: none;
}

/* Or use visibility for animation */
.menu {
  visibility: hidden;
  opacity: 0;
  transition: opacity 0.2s, visibility 0.2s;
}

.menu[aria-hidden="false"] {
  visibility: visible;
  opacity: 1;
}
```

### Busy State

Style loading states based on `aria-busy`:

```css
button[aria-busy="true"] {
  position: relative;
  color: transparent;
  pointer-events: none;
}

button[aria-busy="true"]::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 16px;
  height: 16px;
  margin: -8px 0 0 -8px;
  border: 2px solid currentColor;
  border-right-color: transparent;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
```

### Current Page

Style current navigation item:

```css
.navLink {
  color: #666666;
  text-decoration: none;
}

.navLink[aria-current="page"] {
  color: #0066cc;
  font-weight: 500;
  border-bottom: 2px solid #0066cc;
}
```

## Visually Hidden Content

### Screen Reader Only Text

Hide visually but keep accessible:

```css
.visuallyHidden {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}

/* Make visible on focus (skip links) */
.visuallyHidden:focus {
  position: static;
  width: auto;
  height: auto;
  padding: 8px 16px;
  margin: 0;
  overflow: visible;
  clip: auto;
  white-space: normal;
}
```

### Usage Example

```html
<button>
  <span class="visuallyHidden">Close dialog</span>
  <svg aria-hidden="true"><!-- X icon --></svg>
</button>
```

## Skip Links

Enable keyboard users to skip navigation:

```css
.skipLink {
  position: absolute;
  top: -100px;
  left: 0;
  z-index: 9999;
  padding: 16px 24px;
  background-color: #0066cc;
  color: #ffffff;
  text-decoration: none;
}

.skipLink:focus {
  top: 0;
}
```

```html
<a href="#main-content" class="skipLink">
  Skip to main content
</a>
```

## Color Contrast

### Minimum Contrast Ratios

- **Normal text**: 4.5:1 minimum
- **Large text** (18px+ or 14px bold): 3:1 minimum
- **UI components**: 3:1 minimum

### Accessible Color Combinations

```css
/* Good contrast - meets WCAG AA */
.textPrimary {
  color: #333333; /* on white: 12.6:1 */
  background-color: #ffffff;
}

.textSecondary {
  color: #666666; /* on white: 5.7:1 */
  background-color: #ffffff;
}

.linkText {
  color: #0066cc; /* on white: 5.9:1 */
  background-color: #ffffff;
}

/* Error text needs sufficient contrast */
.errorText {
  color: #cc0000; /* on white: 5.9:1 */
  background-color: #ffffff;
}
```

### Don't Rely on Color Alone

```css
/* Bad - color is only indicator */
.required {
  color: red;
}

/* Good - additional indicator */
.required::after {
  content: ' *';
  color: #cc0000;
}

/* Good - icon + color */
.errorMessage::before {
  content: '⚠ ';
}
```

## Motion and Animation

### Respect User Preferences

```css
/* Reduced motion preference */
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}

/* Or more targeted */
@media (prefers-reduced-motion: reduce) {
  .animatedElement {
    animation: none;
    transition: none;
  }
}
```

### Safe Animation Defaults

```css
/* Enable animations only when not reduced */
@media (prefers-reduced-motion: no-preference) {
  .fadeIn {
    animation: fadeIn 0.3s ease-in-out;
  }

  .slideIn {
    animation: slideIn 0.4s ease-out;
  }
}
```

## Touch Target Size

Ensure interactive elements are large enough:

```css
/* Minimum 44x44px touch targets */
button,
a,
input[type="checkbox"],
input[type="radio"] {
  min-width: 44px;
  min-height: 44px;
}

/* Small buttons need padding */
.iconButton {
  min-width: 44px;
  min-height: 44px;
  padding: 10px; /* Centers 24px icon */
}

/* Increase checkbox/radio hit area */
.checkboxLabel {
  display: inline-flex;
  align-items: center;
  min-height: 44px;
  padding: 10px 0;
  cursor: pointer;
}
```

## High Contrast Mode

Support Windows High Contrast Mode:

```css
/* Forced colors mode support */
@media (forced-colors: active) {
  .button {
    border: 2px solid currentColor;
  }

  .focusRing:focus {
    outline: 3px solid CanvasText;
  }

  /* Use system colors */
  .link {
    color: LinkText;
  }

  .selectedItem {
    background-color: Highlight;
    color: HighlightText;
  }
}
```

## Text Resize

Ensure content works at 200% zoom:

```css
/* Use relative units for text */
body {
  font-size: 100%; /* or 16px base */
}

.heading {
  font-size: 1.5rem; /* scales with user preference */
}

/* Avoid fixed heights on text containers */
.textBox {
  min-height: 100px; /* not height: 100px */
  padding: 16px;
}

/* Use flexible layouts */
.contentArea {
  max-width: 65ch; /* readable line length */
  width: 100%;
}
```

## Form Accessibility

### Label Association

```css
/* Visual label styling */
.formLabel {
  display: block;
  margin-bottom: 4px;
  font-weight: 500;
}

/* Required indicator */
.formLabel.required::after {
  content: ' *';
  color: #cc0000;
}

/* Error message styling */
.errorMessage {
  margin-top: 4px;
  font-size: 14px;
  color: #cc0000;
}

/* Associate with aria-describedby */
.formField[aria-invalid="true"] {
  border-color: #cc0000;
}
```

### Input States

```css
/* Clear state indication */
.formField {
  border: 2px solid #dddddd;
  transition: border-color 0.15s;
}

.formField:hover {
  border-color: #999999;
}

.formField:focus {
  border-color: #0066cc;
  outline: none;
  box-shadow: 0 0 0 3px rgba(0, 102, 204, 0.2);
}

.formField:disabled {
  background-color: #f5f5f5;
  cursor: not-allowed;
}

.formField[aria-invalid="true"] {
  border-color: #cc0000;
}

.formField[aria-invalid="true"]:focus {
  box-shadow: 0 0 0 3px rgba(204, 0, 0, 0.2);
}
```

## Loading States

### Accessible Loading Indicators

```css
/* Spinner with aria-label */
.spinner {
  width: 24px;
  height: 24px;
  border: 3px solid #eeeeee;
  border-top-color: #0066cc;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@media (prefers-reduced-motion: reduce) {
  .spinner {
    animation: none;
    border-style: dotted;
  }
}

/* Skeleton loading */
.skeleton {
  background: linear-gradient(
    90deg,
    #f0f0f0 25%,
    #e0e0e0 50%,
    #f0f0f0 75%
  );
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
}

@media (prefers-reduced-motion: reduce) {
  .skeleton {
    animation: none;
    background: #f0f0f0;
  }
}

@keyframes shimmer {
  0% {
    background-position: 200% 0;
  }
  100% {
    background-position: -200% 0;
  }
}
```

## Print Styles

```css
@media print {
  /* Hide non-essential elements */
  .navigation,
  .sidebar,
  .footer,
  .noprint {
    display: none;
  }

  /* Ensure text is readable */
  body {
    font-size: 12pt;
    line-height: 1.5;
    color: #000000;
    background: #ffffff;
  }

  /* Show link URLs */
  a[href]::after {
    content: ' (' attr(href) ')';
    font-size: 10pt;
  }

  /* Avoid page breaks in content */
  h1, h2, h3 {
    page-break-after: avoid;
  }

  p, li {
    orphans: 3;
    widows: 3;
  }
}
```

## Quick Reference

| State | CSS Selector |
|-------|-------------|
| Disabled | `:disabled`, `[aria-disabled="true"]` |
| Invalid | `[aria-invalid="true"]` |
| Expanded | `[aria-expanded="true"]` |
| Selected | `[aria-selected="true"]` |
| Pressed | `[aria-pressed="true"]` |
| Current | `[aria-current="page"]` |
| Busy | `[aria-busy="true"]` |
| Hidden | `[aria-hidden="true"]` |
| Keyboard focus | `:focus-visible` |
| Any focus | `:focus-within` |

## Checklist

- [ ] Focus indicators visible on all interactive elements
- [ ] Custom focus styles meet contrast requirements
- [ ] ARIA states styled appropriately
- [ ] Color not used as only indicator
- [ ] Motion respects prefers-reduced-motion
- [ ] Touch targets at least 44x44px
- [ ] Text resizes properly to 200%
- [ ] Form states clearly indicated
- [ ] Skip links available
- [ ] High contrast mode supported
