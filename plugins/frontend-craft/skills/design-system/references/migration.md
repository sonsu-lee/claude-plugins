# Migration: Hardcoded Values to Design Tokens

## Overview

This guide covers the process of migrating a codebase from hardcoded CSS values to design tokens. The goal is to replace raw hex codes, pixel values, and other magic numbers with meaningful custom property references — without changing any visual output.

This is not a one-shot rewrite. Migration happens gradually, component by component, with verification at each step.

## Step-by-Step Migration Process

### Step 1: Audit — Find All Hardcoded Values

Before creating any tokens, understand what exists. Use grep patterns to find candidates across the codebase.

**Color values:**

```bash
# Hex colors (3, 4, 6, or 8 digit)
grep -rn --include="*.css" --include="*.scss" '#[0-9a-fA-F]\{3,8\}' src/

# RGB/RGBA
grep -rn --include="*.css" --include="*.scss" 'rgba\?\s*(' src/

# HSL/HSLA
grep -rn --include="*.css" --include="*.scss" 'hsla\?\s*(' src/

# Named colors used as values (common ones that indicate hardcoding)
grep -rn --include="*.css" ':\s*\(white\|black\|red\|blue\|green\|gray\|grey\)\s*[;,]' src/
```

**Spacing values:**

```bash
# Margin and padding with pixel values
grep -rn --include="*.css" '\(margin\|padding\|gap\|top\|right\|bottom\|left\):\s*[0-9]\+px' src/

# Margin and padding shorthand with multiple pixel values
grep -rn --include="*.css" '\(margin\|padding\):\s*[0-9]\+px\s\+[0-9]\+px' src/
```

**Typography values:**

```bash
# Font sizes
grep -rn --include="*.css" 'font-size:\s*[0-9]\+px' src/

# Line heights with raw values
grep -rn --include="*.css" 'line-height:\s*[0-9.]\+' src/

# Font weights as numbers
grep -rn --include="*.css" 'font-weight:\s*[0-9]\+' src/
```

**Border and shadow values:**

```bash
# Border radius
grep -rn --include="*.css" 'border-radius:\s*[0-9]\+px' src/

# Box shadow (often contains hardcoded colors and sizes)
grep -rn --include="*.css" 'box-shadow:' src/
```

Collect results into a spreadsheet or text file. Record the value, file, line number, and the property it belongs to.

### Step 2: Group — Categorize by Purpose

Sort every hardcoded value into one of these categories:

| Category | What to look for | Example values |
|----------|-----------------|----------------|
| Brand colors | Primary, secondary, accent hues | `#2563eb`, `#7c3aed` |
| Neutral colors | Grays, backgrounds, borders, text | `#111827`, `#f9fafb`, `#e5e7eb` |
| Feedback colors | Error, success, warning, info | `#ef4444`, `#22c55e`, `#f59e0b` |
| Spacing | Margins, paddings, gaps | `4px`, `8px`, `16px`, `24px`, `32px` |
| Typography | Font sizes, line heights, weights | `14px`, `16px`, `24px`, `1.5`, `600` |
| Borders | Radius values, border widths | `4px`, `8px`, `1px` |
| Shadows | Box shadows, drop shadows | `0 1px 3px rgba(0,0,0,0.1)` |
| Z-index | Stacking layers | `10`, `100`, `1000` |

Look for clusters. If you see `#2563eb` appear 12 times and `#2564ec` appear twice, those are probably the same intended color. Normalize to one value before tokenizing.

### Step 3: Define Primitives — Raw Value Tokens

Create primitive tokens for each unique value. These are the only place raw values should appear after migration.

```css
:root {
  /* Primitive color tokens — the raw palette */
  --color-blue-50: #eff6ff;
  --color-blue-100: #dbeafe;
  --color-blue-500: #3b82f6;
  --color-blue-600: #2563eb;
  --color-blue-700: #1d4ed8;

  --color-gray-50: #f9fafb;
  --color-gray-100: #f3f4f6;
  --color-gray-200: #e5e7eb;
  --color-gray-300: #d1d5db;
  --color-gray-700: #374151;
  --color-gray-800: #1f2937;
  --color-gray-900: #111827;

  --color-red-500: #ef4444;
  --color-red-600: #dc2626;
  --color-green-500: #22c55e;
  --color-amber-500: #f59e0b;

  /* Primitive spacing tokens */
  --spacing-1: 0.25rem;  /* 4px */
  --spacing-2: 0.5rem;   /* 8px */
  --spacing-3: 0.75rem;  /* 12px */
  --spacing-4: 1rem;     /* 16px */
  --spacing-6: 1.5rem;   /* 24px */
  --spacing-8: 2rem;     /* 32px */
  --spacing-12: 3rem;    /* 48px */

  /* Primitive font sizes */
  --font-size-xs: 0.75rem;   /* 12px */
  --font-size-sm: 0.875rem;  /* 14px */
  --font-size-base: 1rem;    /* 16px */
  --font-size-lg: 1.125rem;  /* 18px */
  --font-size-xl: 1.25rem;   /* 20px */
  --font-size-2xl: 1.5rem;   /* 24px */

  /* Primitive radius */
  --radius-sm: 0.25rem;   /* 4px */
  --radius-md: 0.375rem;  /* 6px */
  --radius-lg: 0.5rem;    /* 8px */
  --radius-xl: 0.75rem;   /* 12px */
  --radius-full: 9999px;
}
```

Key rule: primitive token names describe the value itself (the color hue and shade, the spacing step number), NOT its purpose. `--color-blue-600` is correct. `--color-primary-blue` is wrong at this layer.

### Step 4: Define Semantics — Purpose-Based Names

Map primitives to semantic tokens that express design intent.

```css
:root {
  /* Semantic color tokens — what the color MEANS */
  --color-primary: var(--color-blue-600);
  --color-primary-hover: var(--color-blue-700);
  --color-danger: var(--color-red-500);
  --color-danger-hover: var(--color-red-600);
  --color-success: var(--color-green-500);
  --color-warning: var(--color-amber-500);

  --color-text: var(--color-gray-900);
  --color-text-muted: var(--color-gray-700);
  --color-text-inverse: var(--color-gray-50);

  --color-bg: var(--color-gray-50);
  --color-bg-surface: #ffffff;
  --color-bg-elevated: #ffffff;

  --color-border: var(--color-gray-200);
  --color-border-strong: var(--color-gray-300);

  /* Semantic spacing tokens — what the space IS FOR */
  --spacing-xs: var(--spacing-1);   /* tight: icon gaps, inline elements */
  --spacing-sm: var(--spacing-2);   /* compact: form elements, list items */
  --spacing-md: var(--spacing-4);   /* default: card padding, section gaps */
  --spacing-lg: var(--spacing-8);   /* roomy: section separation */
  --spacing-xl: var(--spacing-12);  /* major: page section breaks */
}
```

Not every primitive needs a semantic mapping. You may have `--color-gray-300` in your primitives that only gets used by one semantic token. That is fine. The semantic layer is where theming happens, so it needs to contain every value that could change between themes.

### Step 5: Replace — Swap Hardcoded Values for Tokens

This is the mechanical step. Go file by file, component by component, and replace raw values with token references.

**Before migration:**

```css
.card {
  background: #ffffff;
  padding: 16px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.card-title {
  font-size: 18px;
  font-weight: 600;
  color: #111827;
  margin-bottom: 8px;
}

.card-body {
  font-size: 14px;
  color: #374151;
  line-height: 1.5;
}

.card-footer {
  padding-top: 16px;
  border-top: 1px solid #e5e7eb;
  margin-top: 16px;
}
```

**After migration:**

```css
.card {
  --card-bg: var(--color-bg-surface);
  --card-padding: var(--spacing-md);
  --card-border: var(--color-border);
  --card-radius: var(--radius-lg);

  background: var(--card-bg);
  padding: var(--card-padding);
  border: 1px solid var(--card-border);
  border-radius: var(--card-radius);
  box-shadow: var(--shadow-sm, 0 1px 3px rgba(0, 0, 0, 0.1));
}

.card-title {
  font-size: var(--font-size-lg);
  font-weight: var(--font-weight-semibold, 600);
  color: var(--color-text);
  margin-bottom: var(--spacing-sm);
}

.card-body {
  font-size: var(--font-size-sm);
  color: var(--color-text-muted);
  line-height: var(--line-height-normal, 1.5);
}

.card-footer {
  padding-top: var(--spacing-md);
  border-top: 1px solid var(--card-border);
  margin-top: var(--spacing-md);
}
```

Notice: the `box-shadow` and `font-weight` use fallback values because those token categories may not be defined yet. This is one of the few cases where a `var()` fallback is appropriate during migration — it keeps the component working while the full token set is being built out. Once the tokens exist, remove the fallbacks.

### Step 6: Verify — Visual Regression Check

After migrating each component:

1. Take screenshots of the component in all states (default, hover, focus, disabled, error) BEFORE the migration.
2. Apply the token changes.
3. Take the same screenshots AFTER.
4. Compare pixel-by-pixel. There should be zero visual differences for the active theme.

If using a visual regression tool (Chromatic, Percy, BackstopJS), run it against the migrated component. Any diff indicates a mapping error.

Manual spot check if no tooling is available:
- Open the component in the browser.
- Inspect each element, verify the computed value matches the original hardcoded value.
- Check the component at multiple viewport sizes.
- If dark mode exists, switch themes and verify dark mode also renders correctly.

## Migration Priority Order

Migrate in this order, from highest impact to lowest:

### 1. Colors (do first)

- Most impactful: colors affect every component visually.
- Easiest to find: hex codes and `rgb()` are unambiguous in grep results.
- Highest payoff: color tokens enable theming immediately.
- Covers: backgrounds, text colors, borders, shadows, gradients.

### 2. Spacing

- High consistency impact: inconsistent spacing is the most common design system violation.
- Easy to grep: `margin`, `padding`, `gap` with `px` values.
- Moderate risk: spacing changes can cause layout shifts if values are mapped incorrectly.
- Covers: margins, paddings, gaps, widths/heights that represent spacing.

### 3. Typography

- Medium impact: affects readability and hierarchy.
- Straightforward: font-size, font-weight, line-height, letter-spacing.
- Watch out for: `font` shorthand properties that combine multiple values.

### 4. Borders and Shadows

- Lower urgency but important for theming: border colors and shadows often need dark mode variants.
- More complex: `box-shadow` values combine size, spread, and color into one declaration.
- Consider creating composite tokens: `--shadow-sm`, `--shadow-md`, `--shadow-lg`.

### 5. Everything Else

- Z-index scales, transition durations, opacity values, breakpoints.
- Only tokenize these if they represent deliberate, reusable design decisions.
- Many of these are structural and do not benefit from tokenization.

## Gradual Migration Strategy

### Per-Component Migration (Recommended)

Migrate one component at a time, in complete isolation. A single pull request should contain:

- The token definitions (if new tokens are needed).
- The single component file with hardcoded values replaced.
- Any test updates.

```
PR #1: "Migrate Button component to design tokens"
  - tokens/primitives.css (add --color-blue-600 if missing)
  - tokens/semantic.css (add --color-primary if missing)
  - components/Button.css (replace all hardcoded values)

PR #2: "Migrate Card component to design tokens"
  - tokens/semantic.css (add --color-bg-surface if missing)
  - components/Card.css (replace all hardcoded values)
```

This approach prevents merge conflicts. If three developers are migrating different components, their PRs touch different component files and only overlap on token definition files (which are additive, so conflicts are trivial to resolve).

### Per-File Migration (Alternative)

If components span multiple files, migrate one file at a time. This is useful for large component libraries where a single component may have base styles, variant styles, and responsive styles in separate files.

### What NOT to Do

Do not attempt a full-codebase migration in a single PR. This causes:

- Massive diffs that are impossible to review meaningfully.
- Merge conflicts with every other in-flight PR.
- High risk of introducing bugs that are hard to isolate.
- Reviewer fatigue leading to rubber-stamped approvals.

## Handling Values That Don't Map to Existing Tokens

During migration you will find values that have no corresponding token. Decide case by case:

### Create a new token if:

- The value appears 3 or more times across the codebase.
- The value represents a deliberate design decision (not a one-off nudge).
- The value would need to change for theming.

```css
/* Found padding: 12px used in 5 components. Create a token. */
:root {
  --spacing-3: 0.75rem; /* 12px — add to primitive scale */
}
```

### Leave as-is with a TODO if:

- The value is used once or twice.
- The value is a structural adjustment, not a design decision.
- You are unsure whether it should be tokenized.

```css
.tooltip-arrow {
  /* TODO: evaluate whether this needs a token (only used here) */
  margin-top: 3px;
}
```

### Normalize first, then tokenize:

If you find `15px` and `16px` used for the same purpose, consult the designer. Pick one value, normalize all usages, then tokenize.

## Common Pitfalls

### 1. Breaking `calc()` Expressions

When a hardcoded value is inside a `calc()`, ensure the replacement token has compatible units.

```css
/* BEFORE: works fine */
width: calc(100% - 32px);

/* WRONG: if --spacing-lg resolves to 2rem, this still works,
   but if you later change the token to a unitless value, it breaks */
width: calc(100% - var(--spacing-lg));

/* SAFE: verify the token's resolved unit is compatible with the expression */
/* --spacing-lg: 2rem works in calc(100% - 2rem) ✓ */
/* --spacing-lg: 32 (unitless) would break calc(100% - 32) ✗ */
```

Rule: spacing tokens should always include units (rem or px). Unitless tokens are only for line-height, opacity, and z-index.

### 2. Replacing Values in Token Definition Files

Token definition files (where primitives are declared) contain raw values by design. Do not recursively replace those.

```css
/* tokens/primitives.css — these ARE the raw values. Leave them alone. */
:root {
  --color-blue-600: #2563eb;  /* ← This hex code stays. It is the source of truth. */
  --spacing-4: 1rem;          /* ← This rem value stays. */
}

/* components/Button.css — THESE are what you migrate. */
.button {
  background: #2563eb;  /* ← Replace with var(--color-primary) */
}
```

### 3. Creating Too Many Tokens

Not every unique value in the codebase deserves a token. Tokens have a maintenance cost: they must be named, documented, and kept in sync with Figma.

Signs you are over-tokenizing:
- Tokens used exactly once.
- Token names that describe the value instead of the purpose: `--margin-top-3px`.
- The token set has more than 200 entries and growing uncontrolled.

### 4. Forgetting to Test Both Themes

After migrating a component, test it in every supported theme. A common failure mode:

```css
/* Light mode: ✓ looks correct */
.alert {
  background: var(--color-bg-surface);
  color: var(--color-text);
  border: 1px solid var(--color-border);
}

/* Dark mode: ✗ --color-bg-surface is not overridden in the dark theme!
   Falls back to #ffffff on a dark page — broken. */
```

Every semantic token used in a component must have a defined value in every theme. If you add a new semantic token during migration, add its dark mode override immediately.

### 5. Migrating vendor/third-party CSS

Do not migrate CSS from third-party libraries (`node_modules`, vendor prefixed files, CSS resets). You do not control those files and they will be overwritten on update. Only migrate CSS you own.

### 6. Changing Values During Migration

Migration is a refactor, not a redesign. Do not "fix" spacing or colors during migration. If `padding: 14px` looks wrong, file a separate issue. The migration PR should produce zero visual changes.

```css
/* WRONG: "fixing" the spacing during migration */
/* Was: padding: 14px → should be 16px → use --spacing-md */
padding: var(--spacing-md);  /* Changed from 14px to 16px — this is not a migration */

/* RIGHT: preserve the original value */
padding: 14px;  /* TODO: non-standard spacing, should be reviewed separately */
```

## Verification Checklist

Run through this checklist for every migration PR:

- [ ] No visual differences in light theme (screenshot comparison).
- [ ] No visual differences in dark theme if applicable.
- [ ] No new tokens created without 3+ usages or a design justification.
- [ ] Token definition files contain only raw values (no `var()` in primitives).
- [ ] Semantic tokens reference primitives (not raw values, unless no primitive exists).
- [ ] Component CSS contains zero hex codes, zero raw `px` spacing, zero raw font sizes.
- [ ] All `calc()` expressions still compute correctly with token values.
- [ ] No vendor/third-party CSS was modified.
- [ ] The PR only touches one component (or a small, related set).

## Tracking Migration Progress

Maintain a simple tracking list. For each component, record its migration status:

```
| Component   | Colors | Spacing | Typography | Borders | Status    |
|-------------|--------|---------|------------|---------|-----------|
| Button      | ✓      | ✓       | ✓          | ✓       | Complete  |
| Card        | ✓      | ✓       | ✓          | ✓       | Complete  |
| Input       | ✓      | ✗       | ✗          | ✗       | Partial   |
| Modal       | ✗      | ✗       | ✗          | ✗       | Not started |
| Sidebar     | ✗      | ✗       | ✗          | ✗       | Not started |
```

This makes it clear what work remains, and prevents duplicate effort if multiple people are contributing to the migration.
