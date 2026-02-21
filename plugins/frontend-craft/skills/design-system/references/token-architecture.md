# Token Architecture

## Token Hierarchy

Design tokens are organized into three layers. Each layer has a distinct purpose. Every token must belong to exactly one layer.

### Layer 1: Primitive Tokens (Raw Values)

Primitive tokens store raw, context-free values. These are the **only** place where hex codes, pixel values, font stacks, and literal numbers appear in the entire system. No design intent is embedded in primitive names -- they describe the value itself.

```css
/* tokens/colors.css — Primitive layer */
:root {
  /* Blues */
  --color-blue-50: #eff6ff;
  --color-blue-100: #dbeafe;
  --color-blue-200: #bfdbfe;
  --color-blue-300: #93c5fd;
  --color-blue-400: #60a5fa;
  --color-blue-500: #3b82f6;
  --color-blue-600: #2563eb;
  --color-blue-700: #1d4ed8;
  --color-blue-800: #1e40af;
  --color-blue-900: #1e3a8a;

  /* Grays */
  --color-gray-50: #f9fafb;
  --color-gray-100: #f3f4f6;
  --color-gray-200: #e5e7eb;
  --color-gray-300: #d1d5db;
  --color-gray-400: #9ca3af;
  --color-gray-500: #6b7280;
  --color-gray-600: #4b5563;
  --color-gray-700: #374151;
  --color-gray-800: #1f2937;
  --color-gray-900: #111827;

  /* Reds */
  --color-red-50: #fef2f2;
  --color-red-500: #ef4444;
  --color-red-600: #dc2626;
  --color-red-700: #b91c1c;

  /* Greens */
  --color-green-50: #f0fdf4;
  --color-green-500: #22c55e;
  --color-green-600: #16a34a;
  --color-green-700: #15803d;

  /* Yellows / Warnings */
  --color-yellow-50: #fefce8;
  --color-yellow-500: #eab308;
  --color-yellow-600: #ca8a04;
}
```

```css
/* tokens/spacing.css — Primitive layer */
:root {
  --spacing-0: 0;
  --spacing-px: 1px;
  --spacing-0-5: 0.125rem;  /* 2px */
  --spacing-1: 0.25rem;     /* 4px */
  --spacing-1-5: 0.375rem;  /* 6px */
  --spacing-2: 0.5rem;      /* 8px */
  --spacing-3: 0.75rem;     /* 12px */
  --spacing-4: 1rem;        /* 16px */
  --spacing-5: 1.25rem;     /* 20px */
  --spacing-6: 1.5rem;      /* 24px */
  --spacing-8: 2rem;        /* 32px */
  --spacing-10: 2.5rem;     /* 40px */
  --spacing-12: 3rem;       /* 48px */
  --spacing-16: 4rem;       /* 64px */
  --spacing-20: 5rem;       /* 80px */
  --spacing-24: 6rem;       /* 96px */
}
```

```css
/* tokens/typography.css — Primitive layer */
:root {
  /* Font families */
  --font-family-sans: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  --font-family-mono: 'JetBrains Mono', 'Fira Code', ui-monospace, monospace;

  /* Font sizes */
  --font-size-xs: 0.75rem;    /* 12px */
  --font-size-sm: 0.875rem;   /* 14px */
  --font-size-base: 1rem;     /* 16px */
  --font-size-lg: 1.125rem;   /* 18px */
  --font-size-xl: 1.25rem;    /* 20px */
  --font-size-2xl: 1.5rem;    /* 24px */
  --font-size-3xl: 1.875rem;  /* 30px */
  --font-size-4xl: 2.25rem;   /* 36px */
  --font-size-5xl: 3rem;      /* 48px */

  /* Font weights */
  --font-weight-normal: 400;
  --font-weight-medium: 500;
  --font-weight-semibold: 600;
  --font-weight-bold: 700;

  /* Line heights */
  --line-height-tight: 1.25;
  --line-height-normal: 1.5;
  --line-height-relaxed: 1.75;

  /* Letter spacing */
  --letter-spacing-tight: -0.025em;
  --letter-spacing-normal: 0;
  --letter-spacing-wide: 0.025em;

  /* Border radius */
  --radius-none: 0;
  --radius-sm: 0.125rem;   /* 2px */
  --radius-md: 0.375rem;   /* 6px */
  --radius-lg: 0.5rem;     /* 8px */
  --radius-xl: 0.75rem;    /* 12px */
  --radius-2xl: 1rem;      /* 16px */
  --radius-full: 9999px;
}
```

### Layer 2: Semantic Tokens (Purpose / Intent)

Semantic tokens assign meaning to primitive values. They describe **what the value is for**, not what it looks like. These are the tokens that change between themes.

```css
/* tokens/semantic.css */
:root {
  /* Brand */
  --color-primary: var(--color-blue-600);
  --color-primary-hover: var(--color-blue-700);
  --color-primary-active: var(--color-blue-800);
  --color-primary-subtle: var(--color-blue-50);

  /* Feedback */
  --color-danger: var(--color-red-500);
  --color-danger-hover: var(--color-red-600);
  --color-danger-subtle: var(--color-red-50);
  --color-success: var(--color-green-500);
  --color-success-hover: var(--color-green-600);
  --color-success-subtle: var(--color-green-50);
  --color-warning: var(--color-yellow-500);
  --color-warning-subtle: var(--color-yellow-50);

  /* Text */
  --color-text: var(--color-gray-900);
  --color-text-secondary: var(--color-gray-600);
  --color-text-muted: var(--color-gray-400);
  --color-text-on-primary: #ffffff;
  --color-text-on-danger: #ffffff;

  /* Surfaces */
  --color-bg: #ffffff;
  --color-bg-subtle: var(--color-gray-50);
  --color-bg-overlay: rgba(0, 0, 0, 0.5);
  --color-surface: #ffffff;
  --color-surface-raised: #ffffff;

  /* Borders */
  --color-border: var(--color-gray-200);
  --color-border-strong: var(--color-gray-300);
  --color-border-focus: var(--color-blue-500);

  /* Shadows */
  --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -2px rgba(0, 0, 0, 0.1);
  --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -4px rgba(0, 0, 0, 0.1);

  /* Semantic spacing */
  --spacing-xs: var(--spacing-1);    /* 4px — tight inner padding */
  --spacing-sm: var(--spacing-2);    /* 8px — compact elements */
  --spacing-md: var(--spacing-4);    /* 16px — standard padding */
  --spacing-lg: var(--spacing-6);    /* 24px — section separation */
  --spacing-xl: var(--spacing-8);    /* 32px — large gaps */
  --spacing-2xl: var(--spacing-12);  /* 48px — major sections */
  --spacing-3xl: var(--spacing-16);  /* 64px — page-level spacing */

  /* Semantic typography */
  --font-body: var(--font-family-sans);
  --font-code: var(--font-family-mono);
  --text-body: var(--font-size-base);
  --text-caption: var(--font-size-sm);
  --text-heading-sm: var(--font-size-lg);
  --text-heading-md: var(--font-size-xl);
  --text-heading-lg: var(--font-size-2xl);
  --text-heading-xl: var(--font-size-3xl);
  --text-display: var(--font-size-4xl);

  /* Semantic radius */
  --radius-interactive: var(--radius-md);   /* buttons, inputs */
  --radius-container: var(--radius-lg);     /* cards, panels */
  --radius-badge: var(--radius-full);       /* pills, badges */
}
```

### Layer 3: Component Tokens (Scoped)

Component tokens are declared inside the component selector. They reference semantic tokens and provide the override points that make variants and theming work.

```css
.button {
  --button-bg: var(--color-primary);
  --button-bg-hover: var(--color-primary-hover);
  --button-text: var(--color-text-on-primary);
  --button-padding-x: var(--spacing-md);
  --button-padding-y: var(--spacing-sm);
  --button-radius: var(--radius-interactive);
  --button-font-size: var(--text-body);
  --button-font-weight: var(--font-weight-medium);

  background: var(--button-bg);
  color: var(--button-text);
  padding: var(--button-padding-y) var(--button-padding-x);
  border-radius: var(--button-radius);
  font-size: var(--button-font-size);
  font-weight: var(--button-font-weight);
  border: none;
  cursor: pointer;
}

.button:hover {
  background: var(--button-bg-hover);
}
```

## Token File Structure

Organize tokens into separate files by category. Import them in dependency order through a single index file.

```
tokens/
  colors.css         ← primitive color values
  spacing.css        ← primitive spacing scale
  typography.css     ← primitive fonts, sizes, weights, radii
  semantic.css       ← semantic tokens referencing primitives
  themes/
    dark.css         ← dark theme overrides (semantic layer only)
    high-contrast.css
  index.css          ← single import point
```

The index file imports in dependency order -- primitives first, then semantics, then themes:

```css
/* tokens/index.css */
@import './colors.css';
@import './spacing.css';
@import './typography.css';
@import './semantic.css';
```

Theme files are loaded conditionally or appended after the base imports:

```css
/* In main entry point */
@import './tokens/index.css';
@import './tokens/themes/dark.css';  /* scoped to [data-theme="dark"] internally */
```

## When to Create a Token

Create a new token when **all** of the following apply:

1. **Used 3+ times** across the codebase (or expected to be, in a new system).
2. **Represents a design decision** -- a deliberate choice, not an incidental value.
3. **Would change per theme** or context -- if dark mode or a brand variant would need a different value, it belongs in a token.

Examples that warrant tokens:
- A brand blue used on buttons, links, and active states.
- A standard `16px` padding used inside cards, modals, and form groups.
- A `600` font weight used for all headings.

## When NOT to Create a Token

Do **not** create a token when:

- **One-off value**: A `margin-top: 2px` nudge to align an icon is not a design decision. It is a layout fix. Use the raw value with a comment.
- **Structural necessity**: A `flex-shrink: 0` or `position: absolute` is structural CSS, not a design value.
- **Derived calculation**: A `calc(var(--spacing-md) + var(--spacing-xs))` expression using existing tokens does not need its own token unless it becomes a reused pattern.
- **Single-use component quirk**: If only one component ever uses `border-width: 3px`, do not create `--border-width-thick` for it.

```css
/* WRONG — token for a one-off nudge */
:root {
  --icon-alignment-fix: 2px;
}
.icon { margin-top: var(--icon-alignment-fix); }

/* RIGHT — inline value with a comment */
.icon { margin-top: 2px; /* optical alignment with adjacent text */ }
```

## Naming Conventions

Follow these patterns. Names must be self-describing. Never use generic names like `--color-1` or `--big-spacing`.

| Layer | Pattern | Examples |
|-------|---------|----------|
| Primitive color | `--color-{hue}-{shade}` | `--color-blue-500`, `--color-gray-100` |
| Primitive spacing | `--spacing-{step}` | `--spacing-4`, `--spacing-8` |
| Primitive font size | `--font-size-{name}` | `--font-size-sm`, `--font-size-xl` |
| Primitive font weight | `--font-weight-{name}` | `--font-weight-bold`, `--font-weight-medium` |
| Primitive radius | `--radius-{size}` | `--radius-sm`, `--radius-lg` |
| Semantic color | `--color-{purpose}` | `--color-primary`, `--color-danger`, `--color-text` |
| Semantic color variant | `--color-{purpose}-{state}` | `--color-primary-hover`, `--color-danger-subtle` |
| Semantic spacing | `--spacing-{size-name}` | `--spacing-xs`, `--spacing-md`, `--spacing-2xl` |
| Semantic typography | `--text-{purpose}` | `--text-body`, `--text-heading-lg`, `--text-caption` |
| Semantic radius | `--radius-{context}` | `--radius-interactive`, `--radius-container` |
| Component token | `--{component}-{property}` | `--button-bg`, `--card-radius`, `--input-border` |
| Component state token | `--{component}-{property}-{state}` | `--button-bg-hover`, `--input-border-focus` |

### Naming rules

- Use lowercase and hyphens only. No camelCase, no underscores.
- Hue names for primitives: `red`, `blue`, `green`, `gray`, `yellow`, `purple`, `orange`. Use a single word.
- Shade scale for colors: `50` through `900` in increments matching Tailwind/Material convention (50, 100, 200, ..., 900).
- Spacing scale: numeric steps matching the rem multiplier (`--spacing-4` = `1rem` = 4 x 0.25rem).
- Never encode the raw value in the name: `--color-blue-hex-2563eb` is wrong.

## Chain Rule

Always reference the next layer up. Never skip layers.

```css
/* CORRECT — component → semantic → primitive */
.button {
  --button-bg: var(--color-primary);          /* references semantic */
  background: var(--button-bg);               /* references component */
}
:root {
  --color-primary: var(--color-blue-600);     /* references primitive */
}

/* WRONG — component skips semantic, references primitive directly */
.button {
  --button-bg: var(--color-blue-600);         /* skips semantic layer */
  background: var(--button-bg);
}

/* WRONG — component uses raw value */
.button {
  background: #2563eb;                        /* no tokens at all */
}
```

The one exception: if there is genuinely no semantic meaning for a primitive (e.g., a decorative gradient stop that is purely aesthetic), a component may reference a primitive directly. This should be rare and documented with a comment.

## Cross-Format Mapping: CSS, JSON, and Figma Variables

Tokens exist in three formats that must stay in sync. The naming convention adapts to each format's syntax, but the structure is identical.

| Figma Variables path | CSS custom property | JSON token path |
|---------------------|--------------------|--------------------|
| `color/blue/500` | `--color-blue-500` | `color.blue.500` |
| `color/primary` | `--color-primary` | `color.primary` |
| `color/primary/hover` | `--color-primary-hover` | `color.primary.hover` |
| `spacing/4` | `--spacing-4` | `spacing.4` |
| `spacing/md` | `--spacing-md` | `spacing.md` |
| `radius/interactive` | `--radius-interactive` | `radius.interactive` |
| `font/size/sm` | `--font-size-sm` | `font.size.sm` |

### Conversion rules

- **Figma to CSS**: Replace `/` (slash) with `-` (hyphen). Prefix with `--`.
- **Figma to JSON**: Replace `/` (slash) with `.` (dot) for nested object paths.
- **CSS to Figma**: Remove `--` prefix. Replace `-` (hyphen) with `/` (slash) at group boundaries.
- **Figma collection groups map to token layers**: A Figma "Primitives" collection holds primitive tokens. A "Semantic" or "Theme" collection holds semantic tokens.

```
Figma Variables                    CSS Custom Properties
─────────────────────             ─────────────────────
Primitives (collection)
  └─ color/blue/500         →     --color-blue-500
  └─ color/blue/600         →     --color-blue-600
  └─ spacing/4              →     --spacing-4

Semantic (collection)
  └─ color/primary          →     --color-primary
       value: {color/blue/600}     value: var(--color-blue-600)
  └─ spacing/md             →     --spacing-md
       value: {spacing/4}          value: var(--spacing-4)
```

### JSON token format (W3C DTCG compatible)

```json
{
  "color": {
    "blue": {
      "500": { "$value": "#3b82f6", "$type": "color" },
      "600": { "$value": "#2563eb", "$type": "color" }
    },
    "primary": { "$value": "{color.blue.600}", "$type": "color" },
    "primary-hover": { "$value": "{color.blue.700}", "$type": "color" }
  },
  "spacing": {
    "4": { "$value": "1rem", "$type": "dimension" },
    "md": { "$value": "{spacing.4}", "$type": "dimension" }
  }
}
```

## Advanced Token Techniques

### @property Registration for Type-Safe Tokens

Register critical tokens with `@property` for type checking, animation support, and guaranteed fallbacks:

```css
@property --color-primary {
  syntax: '<color>';
  inherits: true;
  initial-value: #2563eb;
}
```

Benefits:
- **Type checking**: Browser validates the value matches the declared syntax. Invalid values fall back to `initial-value` instead of producing IACVT (Invalid At Computed-Value Time).
- **Animation**: Registered properties can be interpolated in transitions/animations. Unregistered custom properties cannot.
- **Guaranteed fallback**: `initial-value` provides a reliable fallback when the token value is invalid, unlike `var(--token, fallback)` which only activates when the token is *undefined*.

### Relative Color Syntax for Palette Generation

Generate entire color scales from a single base token using OKLCH relative color syntax:

```css
:root {
  --base-brand: oklch(55% 0.2 260);

  /* Generate scale by adjusting lightness and chroma */
  /* Lighter stops reduce chroma for natural pastels; darker stops slightly reduce for saturation control */
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

**Derive interaction states algorithmically:**

```css
.button {
  --btn-bg: var(--brand-500);
  --btn-bg-hover: oklch(from var(--btn-bg) calc(l - 0.05) c h);
  --btn-bg-active: oklch(from var(--btn-bg) calc(l - 0.1) c h);
  --btn-bg-disabled: oklch(from var(--btn-bg) calc(l + 0.2) calc(c * 0.3) h);
  border-color: oklch(from var(--btn-bg) calc(l - 0.1) c h / 50%);
}
```

**Why OKLCH:** Perceptually uniform lightness — `calc(l + 0.1)` looks the same amount "lighter" regardless of hue. HSL does not have this property.

### Multi-Brand Token Architecture

For systems serving multiple brands, use token variables for brand switching:

```css
/* Namespaced component tokens */
:root {
  --system-card-bg: #ffffff;
  --system-card-accent-bg: #a3533c;
  --system-card-border-radius: 8px;
}

/* Brand override via class */
.theme--brand-b {
  --system-card-accent-bg: #328198;
  --system-card-border-radius: 0;
}
```

Key principles:
- **Namespace tokens by component** (`--system-card-*`) to prevent collision.
- **Tokens control visual decisions**, slots control content structure, props control behavior.
- **Partial components** (sanctioned sub-components) provide guardrails against arbitrary customization that breaks consistency.

### contrast-color() (Emerging)

Auto-selects black or white text for optimal contrast on any background:

```css
.badge {
  background: var(--badge-color);
  color: contrast-color(var(--badge-color));
}
```

Currently Safari Technology Preview only. Uses WCAG 2 contrast algorithm (limited to black/white output). For production, continue using manually curated contrast pairs.

## Building a Token System From Scratch

When a project has no tokens -- only hardcoded values scattered across CSS files -- follow this process to create a token system incrementally.

### Step 1: Audit Existing Hardcoded Values

Search the entire codebase for raw values. Group what you find.

```bash
# Find all hex colors
grep -roh '#[0-9a-fA-F]\{3,8\}' src/ | sort | uniq -c | sort -rn

# Find all pixel/rem values in padding and margin
grep -roE '(padding|margin)[^;]*:[^;]+;' src/ | grep -oE '[0-9.]+(px|rem|em)' | sort | uniq -c | sort -rn

# Find all font-size declarations
grep -roE 'font-size:\s*[^;]+' src/ | sort | uniq -c | sort -rn
```

Record the results. You will see clusters: the same blue hex used 14 times, `16px` padding used 23 times, etc.

### Step 2: Group by Purpose

Categorize every frequently-used raw value:

| Raw value | Usage count | Proposed category | Proposed primitive name |
|-----------|-------------|-------------------|------------------------|
| `#2563eb` | 14 | Color — blue | `--color-blue-600` |
| `#ef4444` | 8 | Color — red | `--color-red-500` |
| `1rem` | 23 | Spacing | `--spacing-4` |
| `0.5rem` | 18 | Spacing | `--spacing-2` |
| `0.875rem` | 9 | Font size | `--font-size-sm` |

### Step 3: Define the Primitive Layer

Create token files with only the clustered raw values. Do not try to be exhaustive -- start with the values that actually exist in the codebase.

```css
/* tokens/colors.css — start with what you actually use */
:root {
  --color-blue-500: #3b82f6;
  --color-blue-600: #2563eb;
  --color-blue-700: #1d4ed8;
  --color-gray-50: #f9fafb;
  --color-gray-200: #e5e7eb;
  --color-gray-900: #111827;
  --color-red-500: #ef4444;
  --color-green-500: #22c55e;
}
```

You do not need the full 50-900 range for every hue on day one. Add shades as the design requires them.

### Step 4: Define the Semantic Layer

Look at how each primitive is used. Assign purpose-based names.

```css
/* tokens/semantic.css — based on actual usage patterns */
:root {
  --color-primary: var(--color-blue-600);       /* buttons, links, active indicators */
  --color-danger: var(--color-red-500);          /* error states, destructive actions */
  --color-success: var(--color-green-500);       /* success messages, positive indicators */
  --color-text: var(--color-gray-900);           /* main body text */
  --color-border: var(--color-gray-200);         /* default borders */
  --color-bg: var(--color-gray-50);              /* page background */

  --spacing-sm: var(--spacing-2);                /* compact padding in small elements */
  --spacing-md: var(--spacing-4);                /* standard padding */
  --spacing-lg: var(--spacing-6);                /* section gaps */
}
```

### Step 5: Replace Hardcoded Values Incrementally

Do not attempt a full codebase replacement in a single pass. Work component by component:

1. Pick one component (e.g., `.button`).
2. Replace every hardcoded value with the appropriate semantic or component token.
3. Verify the component looks identical after the change.
4. Move to the next component.

```css
/* Before */
.button {
  background: #2563eb;
  color: #ffffff;
  padding: 8px 16px;
  border-radius: 6px;
}

/* After — with tokens */
.button {
  --button-bg: var(--color-primary);
  --button-text: var(--color-text-on-primary);
  --button-padding-x: var(--spacing-md);
  --button-padding-y: var(--spacing-sm);
  --button-radius: var(--radius-interactive);

  background: var(--button-bg);
  color: var(--button-text);
  padding: var(--button-padding-y) var(--button-padding-x);
  border-radius: var(--button-radius);
}
```

### Step 6: Fill Gaps as Needed

As you tokenize more components, you will discover missing primitives or semantic tokens. Add them when the need arises -- not before. A token system grows with the product. Do not pre-generate hundreds of tokens that nobody uses.

### Step 7: Introduce Theming Once the Semantic Layer is Stable

Dark mode and theme variants only work reliably when the semantic layer is complete. Do not attempt theming until most components reference semantic tokens rather than primitives or raw values. For comprehensive dark mode techniques (`color-scheme`, `light-dark()`, system colors), see `references/bootstrapping.md`.

```css
/* tokens/themes/dark.css — only override semantic tokens */
[data-theme="dark"] {
  --color-primary: var(--color-blue-500);
  --color-text: var(--color-gray-50);
  --color-text-secondary: var(--color-gray-300);
  --color-bg: var(--color-gray-900);
  --color-surface: var(--color-gray-800);
  --color-border: var(--color-gray-700);

  --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.3);
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.4), 0 2px 4px -2px rgba(0, 0, 0, 0.3);
}
```
