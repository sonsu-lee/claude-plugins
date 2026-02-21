# Design Tokens & Theming

> **Note:** This is a concise reference for CSS authors. For comprehensive token architecture, multi-brand strategies, OKLCH palette generation, and migration guidance, see the **design-system** skill's reference files.

## Token Hierarchy

Structure all design values into three layers. Never skip a layer.

### Primitive Tokens (Raw Values)

Define raw, context-free values. These are the only place hex codes, pixel values, and raw numbers appear.

```css
:root {
  /* Colors */
  --color-blue-50: #eff6ff;
  --color-blue-500: #3b82f6;
  --color-blue-600: #2563eb;
  --color-blue-700: #1d4ed8;
  --color-gray-50: #f9fafb;
  --color-gray-100: #f3f4f6;
  --color-gray-200: #e5e7eb;
  --color-gray-700: #374151;
  --color-gray-800: #1f2937;
  --color-gray-900: #111827;
  --color-red-500: #ef4444;
  --color-green-500: #22c55e;

  /* Spacing */
  --spacing-1: 0.25rem;  /* 4px */
  --spacing-2: 0.5rem;   /* 8px */
  --spacing-3: 0.75rem;  /* 12px */
  --spacing-4: 1rem;     /* 16px */
  --spacing-6: 1.5rem;   /* 24px */
  --spacing-8: 2rem;     /* 32px */
  --spacing-12: 3rem;    /* 48px */
  --spacing-16: 4rem;    /* 64px */

  /* Font sizes */
  --font-size-xs: 0.75rem;
  --font-size-sm: 0.875rem;
  --font-size-base: 1rem;
  --font-size-lg: 1.125rem;
  --font-size-xl: 1.25rem;
  --font-size-2xl: 1.5rem;
  --font-size-3xl: 1.875rem;
  --font-size-4xl: 2.25rem;

  /* Border radius */
  --radius-sm: 0.125rem;
  --radius-md: 0.375rem;
  --radius-lg: 0.5rem;
  --radius-xl: 0.75rem;
  --radius-full: 9999px;
}
```

### Semantic Tokens (Purpose)

Define in `:root`, referencing primitives. These express design intent.

```css
:root {
  --color-primary: var(--color-blue-600);
  --color-primary-hover: var(--color-blue-700);
  --color-danger: var(--color-red-500);
  --color-success: var(--color-green-500);
  --color-text: var(--color-gray-900);
  --color-text-muted: var(--color-gray-700);
  --color-bg: var(--color-gray-50);
  --color-bg-surface: #ffffff;
  --color-border: var(--color-gray-200);

  --spacing-xs: var(--spacing-1);   /* 4px */
  --spacing-sm: var(--spacing-2);   /* 8px */
  --spacing-md: var(--spacing-4);   /* 16px */
  --spacing-lg: var(--spacing-6);   /* 24px */
  --spacing-xl: var(--spacing-8);   /* 32px */
}
```

### Component Tokens (Specific)

Scope to the component. Always reference semantic tokens.

```css
.button {
  --button-bg: var(--color-primary);
  --button-bg-hover: var(--color-primary-hover);
  --button-text: #ffffff;
  --button-padding-x: var(--spacing-md);
  --button-padding-y: var(--spacing-sm);
  --button-radius: var(--radius-md);

  background: var(--button-bg);
  color: var(--button-text);
  padding: var(--button-padding-y) var(--button-padding-x);
  border-radius: var(--button-radius);
}

.card {
  --card-padding: var(--spacing-md);
  --card-radius: var(--radius-lg);
  --card-bg: var(--color-bg-surface);
  --card-border: var(--color-border);

  background: var(--card-bg);
  padding: var(--card-padding);
  border-radius: var(--card-radius);
  border: 1px solid var(--card-border);
}
```

### Chain Rule

Always reference the next layer up: component -> semantic -> primitive. Never use raw hex/pixel values in component CSS. Never skip a layer (component directly referencing a primitive is wrong unless no semantic equivalent exists).

## When to Create a Token

Create a token when:
- A value is used 3 or more times across the codebase.
- A value represents a deliberate design decision (brand color, standard spacing).
- A value must change per theme or breakpoint.

Do NOT create a token when:
- A value is used once and is arbitrary (e.g., a one-off `margin-top: 3px` nudge).
- The value is a structural necessity, not a design choice.

## Naming Conventions

Follow these patterns strictly:

| Layer | Pattern | Examples |
|-------|---------|----------|
| Primitive color | `--color-{hue}-{shade}` | `--color-blue-500`, `--color-gray-100` |
| Primitive spacing | `--spacing-{step}` | `--spacing-4`, `--spacing-8` |
| Primitive font | `--font-size-{name}` | `--font-size-sm`, `--font-size-xl` |
| Semantic color | `--color-{purpose}` | `--color-primary`, `--color-danger`, `--color-text`, `--color-bg` |
| Semantic spacing | `--spacing-{context}` | `--spacing-xs`, `--spacing-sm`, `--spacing-md` |
| Component | `--{component}-{property}` | `--button-bg`, `--card-radius`, `--input-border` |

Never use generic names like `--color-1` or `--big-spacing`. Names must be self-describing.

## Theming & Dark Mode

### Attribute-based theming (preferred)

Override semantic tokens on a data attribute. Primitives never change per theme.

```css
[data-theme="dark"] {
  --color-bg: var(--color-gray-900);
  --color-bg-surface: var(--color-gray-800);
  --color-text: var(--color-gray-50);
  --color-text-muted: var(--color-gray-200);
  --color-border: var(--color-gray-700);
  --color-primary: var(--color-blue-500);
}
```

### System preference detection

Use `prefers-color-scheme` as the automatic default, with data attribute as the manual override.

```css
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --color-bg: var(--color-gray-900);
    --color-text: var(--color-gray-50);
    --color-primary: var(--color-blue-500);
  }
}
```

### Theme switching rules

- Only override semantic tokens in theme selectors. Never redefine primitives.
- Every semantic color token must have both light and dark values defined.
- Test both themes with every UI change. Do not assume dark mode works from light mode alone.

## Color Accessibility

Follow WCAG AA at minimum:
- **4.5:1** contrast ratio for normal text (under 18px / 14px bold).
- **3:1** contrast ratio for large text (18px+ / 14px+ bold).
- **3:1** contrast ratio for UI components and graphical objects.

Rules:
- Never rely on color alone to convey information. Add icons, text labels, or patterns.
- Use semantic color names: `--color-danger` not `--color-red`. The meaning matters, not the hue.
- Never hardcode hex values in component CSS. Always go through tokens.
- When creating a dark theme, re-check all contrast ratios. Light-mode-passing colors often fail on dark backgrounds.

## Spacing System

Use a consistent base unit. Choose one and stick to it:
- **4px base** (0.25rem increments): more granular, good for dense UIs.
- **8px base** (0.5rem increments): simpler, good for most apps.

Rules:
- All spacing in component CSS must reference tokens: `padding: var(--spacing-md)`.
- Never use magic numbers like `padding: 13px`.
- Maintain a limited set of spacing values. If the scale has gaps, add to the scale rather than using arbitrary values.

## Figma Integration

When a Figma design system exists:
- Token names in CSS must match Figma variable names. If Figma calls it `color/primary`, use `--color-primary`.
- Primitive tokens map to Figma's raw color/spacing variables.
- Semantic tokens map to Figma's aliased/referencing variables.
- If Figma uses Token Studio or Variables, the JSON output can be converted directly to CSS custom properties.
- When Figma and code diverge, update whichever is behind. Do not tolerate drift.
