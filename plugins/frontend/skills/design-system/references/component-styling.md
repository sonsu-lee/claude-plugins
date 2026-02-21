# Component Styling with Design Tokens

## Component Token Application Pattern

Every component that uses design tokens follows the same structure: declare component-scoped CSS variables that reference semantic tokens, then use those component variables in CSS properties.

```css
.button {
  /* 1. Declare component tokens referencing semantic tokens */
  --button-bg: var(--color-primary);
  --button-bg-hover: var(--color-primary-hover);
  --button-text: var(--color-text-on-primary);
  --button-padding-x: var(--spacing-md);
  --button-padding-y: var(--spacing-sm);
  --button-radius: var(--radius-interactive);
  --button-font-size: var(--text-body);
  --button-font-weight: var(--font-weight-medium);
  --button-border-width: 1px;
  --button-border-color: transparent;

  /* 2. Apply component tokens to properties */
  background: var(--button-bg);
  color: var(--button-text);
  padding: var(--button-padding-y) var(--button-padding-x);
  border-radius: var(--button-radius);
  font-size: var(--button-font-size);
  font-weight: var(--button-font-weight);
  border: var(--button-border-width) solid var(--button-border-color);
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: var(--spacing-xs);
  transition: background 150ms ease, border-color 150ms ease;
}
```

This two-step pattern is critical. It creates a stable API surface: anyone overriding the component only needs to change `--button-bg`, not hunt through property declarations.

## When to Create Component Tokens vs. Use Semantic Tokens Directly

Not every property needs a component-level token. The decision depends on whether the value is an **override point** -- something that variants, themes, or consumers might change.

### Create component tokens when:

- The component has **variants** that change the value (e.g., `--button-bg` changes for primary, danger, ghost variants).
- The component needs **external override points** (a consumer wrapping the component might need to adjust padding or color).
- The value is a **composite** of multiple semantic tokens (e.g., padding shorthand combining two spacing tokens).
- The property participates in **interaction states** (hover, active, focus) where the base and state values differ.

### Use semantic tokens directly when:

- The value is **universal and never component-specific** (e.g., `font-family: var(--font-body)` is the same everywhere).
- The component has **no variants** for that property.
- The value is **structural**, not stylistic (e.g., `gap: var(--spacing-sm)` in a simple list where no variant would change it).

```css
/* Component tokens for things that vary */
.badge {
  --badge-bg: var(--color-primary-subtle);
  --badge-text: var(--color-primary);
  --badge-radius: var(--radius-badge);
  --badge-padding-x: var(--spacing-sm);
  --badge-padding-y: var(--spacing-xs);
  --badge-font-size: var(--text-caption);

  background: var(--badge-bg);
  color: var(--badge-text);
  border-radius: var(--badge-radius);
  padding: var(--badge-padding-y) var(--badge-padding-x);
  font-size: var(--badge-font-size);

  /* Direct semantic usage for things that never vary */
  font-family: var(--font-body);
  font-weight: var(--font-weight-medium);
  line-height: var(--line-height-tight);
}
```

## Variant Styling Through Token Switching

Variants override component tokens only. They never redefine the full property set. This keeps variants minimal and predictable.

### Color variants

```css
/* Base — primary is the default */
.button {
  --button-bg: var(--color-primary);
  --button-bg-hover: var(--color-primary-hover);
  --button-text: var(--color-text-on-primary);
  --button-border-color: transparent;

  background: var(--button-bg);
  color: var(--button-text);
  border: 1px solid var(--button-border-color);
}

.button:hover {
  background: var(--button-bg-hover);
}

/* Danger variant — switch only the tokens that change */
.button--danger {
  --button-bg: var(--color-danger);
  --button-bg-hover: var(--color-danger-hover);
  --button-text: var(--color-text-on-danger);
}

/* Ghost / outline variant — no fill, border visible */
.button--ghost {
  --button-bg: transparent;
  --button-bg-hover: var(--color-primary-subtle);
  --button-text: var(--color-primary);
  --button-border-color: var(--color-border);
}

/* Secondary variant */
.button--secondary {
  --button-bg: var(--color-bg-subtle);
  --button-bg-hover: var(--color-border);
  --button-text: var(--color-text);
}
```

### Size variants

```css
.button--sm {
  --button-padding-x: var(--spacing-sm);
  --button-padding-y: var(--spacing-xs);
  --button-font-size: var(--text-caption);
}

.button--lg {
  --button-padding-x: var(--spacing-lg);
  --button-padding-y: var(--spacing-md);
  --button-font-size: var(--text-heading-sm);
}
```

### Combining variants

Because each variant only touches its own tokens, combinations work automatically with no extra CSS:

```html
<!-- These all work without any compound selectors -->
<button class="button button--danger button--lg">Delete Account</button>
<button class="button button--ghost button--sm">Cancel</button>
```

No `.button--danger.button--lg` selector is needed. The token overrides compose naturally because they target different variables.

## Interaction States via Tokens

Define state-specific tokens at the component level. Never hardcode color adjustments like `filter: brightness(0.9)` or shift to an arbitrary hex inside a `:hover` rule.

### Core state pattern

```css
.input {
  --input-bg: var(--color-surface);
  --input-border: var(--color-border);
  --input-border-hover: var(--color-border-strong);
  --input-border-focus: var(--color-border-focus);
  --input-text: var(--color-text);
  --input-placeholder: var(--color-text-muted);
  --input-radius: var(--radius-interactive);
  --input-ring-color: var(--color-primary);
  --input-ring-width: 2px;
  --input-ring-offset: 1px;

  background: var(--input-bg);
  border: 1px solid var(--input-border);
  border-radius: var(--input-radius);
  color: var(--input-text);
  padding: var(--spacing-sm) var(--spacing-md);
  outline: none;
  transition: border-color 150ms ease, box-shadow 150ms ease;
}

.input::placeholder {
  color: var(--input-placeholder);
}

.input:hover {
  border-color: var(--input-border-hover);
}

.input:focus {
  border-color: var(--input-border-focus);
  box-shadow: 0 0 0 var(--input-ring-width) var(--input-ring-color);
}
```

### Disabled state

Disabled styling should use tokens to ensure consistency across all disabled elements in the system.

```css
.button:disabled,
.button[aria-disabled="true"] {
  --button-bg: var(--color-bg-subtle);
  --button-text: var(--color-text-muted);
  --button-border-color: var(--color-border);

  cursor: not-allowed;
  pointer-events: none;
  opacity: 0.6;
}

.input:disabled,
.input[aria-disabled="true"] {
  --input-bg: var(--color-bg-subtle);
  --input-border: var(--color-border);
  --input-text: var(--color-text-muted);

  cursor: not-allowed;
}
```

### Error state

```css
.input--error {
  --input-border: var(--color-danger);
  --input-border-hover: var(--color-danger-hover);
  --input-border-focus: var(--color-danger);
  --input-ring-color: var(--color-danger);
}
```

All state changes happen through token reassignment. The property declarations in the base component never change. This makes states composable and predictable.

## Theme Override Pattern

When component tokens reference semantic tokens, dark mode and other themes work automatically. The component never needs to know which theme is active.

### How it works

```css
/* Semantic tokens — light (default) */
:root {
  --color-primary: var(--color-blue-600);
  --color-text: var(--color-gray-900);
  --color-surface: #ffffff;
  --color-border: var(--color-gray-200);
}

/* Semantic tokens — dark override */
[data-theme="dark"] {
  --color-primary: var(--color-blue-400);
  --color-text: var(--color-gray-50);
  --color-surface: var(--color-gray-800);
  --color-border: var(--color-gray-600);
}

/* Component — same CSS in both themes */
.card {
  --card-bg: var(--color-surface);
  --card-text: var(--color-text);
  --card-border: var(--color-border);
  --card-radius: var(--radius-container);
  --card-padding: var(--spacing-md);

  background: var(--card-bg);
  color: var(--card-text);
  border: 1px solid var(--card-border);
  border-radius: var(--card-radius);
  padding: var(--card-padding);
}
```

The `.card` CSS is written once. When `[data-theme="dark"]` is applied to the document, `--color-surface` resolves to `var(--color-gray-800)` instead of `#ffffff`, and the card automatically adapts.

### Component-specific theme overrides

Occasionally a component needs different behavior in dark mode beyond what automatic token resolution provides (e.g., a shadow should be heavier in dark mode, or a particular surface needs different opacity):

```css
[data-theme="dark"] .card--elevated {
  --card-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
}
```

This should be rare. If many components need dark-specific overrides, the semantic token layer has gaps that should be filled.

## Composing Multiple Token Layers for Complex Components

Complex components have multiple zones, each with their own spacing, color, or typography needs. Use a flat component token namespace with descriptive names for each zone.

### Card with header, body, and footer

```css
.card {
  /* Surface tokens */
  --card-bg: var(--color-surface);
  --card-border: var(--color-border);
  --card-radius: var(--radius-container);
  --card-shadow: var(--shadow-sm);

  /* Header zone tokens */
  --card-header-bg: var(--color-bg-subtle);
  --card-header-padding: var(--spacing-md);
  --card-header-font-size: var(--text-heading-sm);
  --card-header-font-weight: var(--font-weight-semibold);
  --card-header-text: var(--color-text);
  --card-header-border: var(--color-border);

  /* Body zone tokens */
  --card-body-padding: var(--spacing-md);
  --card-body-text: var(--color-text);
  --card-body-font-size: var(--text-body);

  /* Footer zone tokens */
  --card-footer-bg: var(--color-bg-subtle);
  --card-footer-padding: var(--spacing-sm) var(--spacing-md);
  --card-footer-border: var(--color-border);

  background: var(--card-bg);
  border: 1px solid var(--card-border);
  border-radius: var(--card-radius);
  box-shadow: var(--card-shadow);
  overflow: hidden;
}

.card__header {
  background: var(--card-header-bg);
  padding: var(--card-header-padding);
  font-size: var(--card-header-font-size);
  font-weight: var(--card-header-font-weight);
  color: var(--card-header-text);
  border-bottom: 1px solid var(--card-header-border);
}

.card__body {
  padding: var(--card-body-padding);
  color: var(--card-body-text);
  font-size: var(--card-body-font-size);
}

.card__footer {
  background: var(--card-footer-bg);
  padding: var(--card-footer-padding);
  border-top: 1px solid var(--card-footer-border);
  display: flex;
  justify-content: flex-end;
  gap: var(--spacing-sm);
}
```

### Multi-zone variant example

A `card--compact` variant can override specific zone tokens without rewriting any property declarations:

```css
.card--compact {
  --card-header-padding: var(--spacing-sm);
  --card-body-padding: var(--spacing-sm);
  --card-footer-padding: var(--spacing-xs) var(--spacing-sm);
  --card-header-font-size: var(--text-caption);
}
```

### Navigation component with multiple sections

```css
.nav {
  /* Container tokens */
  --nav-bg: var(--color-surface);
  --nav-padding: var(--spacing-sm) var(--spacing-md);
  --nav-border: var(--color-border);
  --nav-height: 3.5rem;

  /* Nav item tokens */
  --nav-item-padding: var(--spacing-sm) var(--spacing-md);
  --nav-item-text: var(--color-text-secondary);
  --nav-item-text-hover: var(--color-text);
  --nav-item-text-active: var(--color-primary);
  --nav-item-bg-hover: var(--color-bg-subtle);
  --nav-item-bg-active: var(--color-primary-subtle);
  --nav-item-radius: var(--radius-interactive);
  --nav-item-font-size: var(--text-caption);
  --nav-item-font-weight: var(--font-weight-medium);

  background: var(--nav-bg);
  padding: var(--nav-padding);
  border-bottom: 1px solid var(--nav-border);
  height: var(--nav-height);
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
}

.nav__item {
  padding: var(--nav-item-padding);
  color: var(--nav-item-text);
  font-size: var(--nav-item-font-size);
  font-weight: var(--nav-item-font-weight);
  border-radius: var(--nav-item-radius);
  text-decoration: none;
  transition: background 150ms ease, color 150ms ease;
}

.nav__item:hover {
  color: var(--nav-item-text-hover);
  background: var(--nav-item-bg-hover);
}

.nav__item--active {
  color: var(--nav-item-text-active);
  background: var(--nav-item-bg-active);
  font-weight: var(--font-weight-semibold);
}
```

## Anti-Patterns

### 1. Using primitive tokens directly in components

Primitive tokens carry no design intent. Using them in components bypasses the semantic layer and breaks theming.

```css
/* WRONG — primitive token in a component */
.alert {
  background: var(--color-red-50);
  border: 1px solid var(--color-red-500);
  color: var(--color-red-700);
}

/* RIGHT — semantic tokens in a component */
.alert {
  --alert-bg: var(--color-danger-subtle);
  --alert-border: var(--color-danger);
  --alert-text: var(--color-text);

  background: var(--alert-bg);
  border: 1px solid var(--alert-border);
  color: var(--alert-text);
}
```

When the theme changes, `--color-red-50` stays `#fef2f2` regardless of dark or light mode. But `--color-danger-subtle` resolves correctly in both themes.

### 2. Mixing hardcoded values with tokens

A component that is half-tokenized is worse than a fully hardcoded one. It creates a false sense of consistency -- some values respond to theme changes, others do not.

```css
/* WRONG — mixed approach */
.card {
  background: var(--color-surface);     /* tokenized */
  padding: 20px;                        /* hardcoded */
  border: 1px solid #e5e7eb;            /* hardcoded */
  border-radius: var(--radius-container); /* tokenized */
}

/* RIGHT — fully tokenized */
.card {
  --card-bg: var(--color-surface);
  --card-padding: var(--spacing-md);
  --card-border: var(--color-border);
  --card-radius: var(--radius-container);

  background: var(--card-bg);
  padding: var(--card-padding);
  border: 1px solid var(--card-border);
  border-radius: var(--card-radius);
}
```

### 3. Creating tokens for every single property

Not every CSS property should have a token. Structural properties, layout logic, and one-off positioning values are not design decisions.

```css
/* WRONG — over-tokenized */
.modal {
  --modal-display: flex;
  --modal-position: fixed;
  --modal-z-index: 1000;
  --modal-inset: 0;
  --modal-align-items: center;
  --modal-justify-content: center;
  --modal-overflow: auto;

  display: var(--modal-display);
  position: var(--modal-position);
  z-index: var(--modal-z-index);
  inset: var(--modal-inset);
  align-items: var(--modal-align-items);
  justify-content: var(--modal-justify-content);
  overflow: var(--modal-overflow);
}

/* RIGHT — only tokenize design values */
.modal {
  --modal-bg-overlay: var(--color-bg-overlay);
  --modal-content-bg: var(--color-surface);
  --modal-content-radius: var(--radius-container);
  --modal-content-shadow: var(--shadow-lg);
  --modal-content-padding: var(--spacing-lg);
  --modal-content-max-width: 32rem;

  display: flex;
  position: fixed;
  z-index: 1000;
  inset: 0;
  align-items: center;
  justify-content: center;
  overflow: auto;
  background: var(--modal-bg-overlay);
}

.modal__content {
  background: var(--modal-content-bg);
  border-radius: var(--modal-content-radius);
  box-shadow: var(--modal-content-shadow);
  padding: var(--modal-content-padding);
  max-width: var(--modal-content-max-width);
  width: 100%;
}
```

### 4. Defining state styles through property manipulation instead of tokens

```css
/* WRONG — computed hover color, not a token */
.button:hover {
  background: color-mix(in srgb, var(--button-bg) 85%, black);
}

/* WRONG — arbitrary shade shift */
.button:hover {
  filter: brightness(0.9);
}

/* RIGHT — explicit hover token */
.button {
  --button-bg: var(--color-primary);
  --button-bg-hover: var(--color-primary-hover);
}
.button:hover {
  background: var(--button-bg-hover);
}
```

Using explicit hover tokens ensures designers have approved the exact hover color, and it works predictably across themes.

### 5. Nesting component tokens from unrelated components

```css
/* WRONG — card reaching into button's internals */
.card .button {
  --button-bg: var(--card-accent);
}

/* RIGHT — use established variant patterns */
.card .button {
  /* Use button's own variant API */
}
/* Or define a card-specific button variant */
.button--card-action {
  --button-bg: var(--color-surface);
  --button-text: var(--color-primary);
  --button-border-color: var(--color-border);
}
```

Components should not reach into other components' token namespaces. If a button needs different styling inside a card, create a variant of the button or use a shared semantic token that both can reference.
