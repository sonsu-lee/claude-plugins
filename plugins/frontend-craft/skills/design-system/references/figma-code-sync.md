# Figma-Code Synchronization

## Core Principle

**Existing Figma content is never modified or deleted. Only additions are guided.**

When the design system plugin identifies gaps or misalignments between Figma and code, it recommends additions to bring the two into alignment. It never alters what designers have already built in Figma. The code side adapts to match Figma's naming and structure, not the other way around.

## Figma Variable to CSS Variable Naming Mapping

Figma Variables use slash-separated paths organized by collections. CSS custom properties use hyphen-separated names with a `--` prefix. The conversion is mechanical.

### Conversion rules

| Figma format | CSS format | Rule |
|---|---|---|
| `color/blue/500` | `--color-blue-500` | Replace `/` with `-`, prefix with `--` |
| `color/primary` | `--color-primary` | Same rule applies to semantic names |
| `color/primary/hover` | `--color-primary-hover` | Multi-level paths flatten to hyphens |
| `spacing/md` | `--spacing-md` | Category and name joined by hyphen |
| `spacing/4` | `--spacing-4` | Numeric names preserved as-is |
| `radius/interactive` | `--radius-interactive` | Semantic radius names preserved |
| `font/size/sm` | `--font-size-sm` | Nested groups flatten to hyphens |
| `shadow/md` | `--shadow-md` | Effects follow the same convention |

### Collection-to-layer mapping

Figma organizes variables into collections. Each collection corresponds to a token layer:

| Figma collection | Token layer | Scope |
|---|---|---|
| Primitives | Primitive tokens | Raw values: hex codes, pixel/rem values, font stacks |
| Semantic (or Theme) | Semantic tokens | Purpose-based aliases that reference primitives |
| Components | Component tokens | Component-scoped variables (less common in Figma) |

If the Figma file uses different collection names, map them by their content:

- A collection containing raw hex colors and numeric spacing values is the **primitive** layer, regardless of its name.
- A collection where most values reference other variables (aliases) is the **semantic** layer.

### Figma modes to CSS themes

Figma variable modes (e.g., Light and Dark within the Semantic collection) correspond to CSS theme selectors:

```
Figma: Semantic collection → Mode: Light
  color/primary = {Primitives/color/blue/600}

Figma: Semantic collection → Mode: Dark
  color/primary = {Primitives/color/blue/400}
```

```css
/* CSS equivalent */
:root {
  --color-primary: var(--color-blue-600);
}

[data-theme="dark"] {
  --color-primary: var(--color-blue-400);
}
```

## Manual Alignment Checklist

When no automated tooling is available, use this manual process to compare Figma variables and CSS tokens.

### Step 1: Export Figma variables

Open the Figma file. Go to Local Variables. For each collection, list every variable with its name, value, and any aliases it references. Record them in a spreadsheet or plain text table:

```
Collection: Primitives
  color/blue/500    #3b82f6
  color/blue/600    #2563eb
  color/gray/200    #e5e7eb
  spacing/4         16

Collection: Semantic
  color/primary     → {color/blue/600}
  color/border      → {color/gray/200}
  spacing/md        → {spacing/4}
```

### Step 2: List all CSS custom properties

Search the codebase for every CSS custom property definition:

```bash
grep -roh -- '--[a-zA-Z][a-zA-Z0-9-]*' src/tokens/ | sort -u
```

Record each with its value and file location.

### Step 3: Compare names and values

Create a comparison table with four columns:

| Figma variable | CSS property | Name match | Value match |
|---|---|---|---|
| `color/blue/500` | `--color-blue-500` | Yes | Yes (`#3b82f6`) |
| `color/primary` | `--color-primary` | Yes | Yes (both ref blue-600) |
| `color/border/strong` | `--color-border-strong` | Yes | No (Figma: gray-400, CSS: gray-300) |
| `spacing/2xl` | _(missing)_ | N/A | N/A |
| _(missing)_ | `--color-bg-overlay` | N/A | N/A |
| `color/accent` | `--color-brand` | No (mismatch) | Yes (same hex value) |

### Step 4: Categorize discrepancies

Sort every row from Step 3 into one of five categories:

1. **Aligned** -- name and value match. No action needed.
2. **Code-only tokens** -- exists in CSS but not in Figma. Needs Figma addition.
3. **Figma-only variables** -- exists in Figma but not in CSS. Needs CSS token creation.
4. **Name mismatches** -- same value exists in both but under different names. Needs renaming.
5. **Value mismatches** -- same name exists in both but with different values. Needs investigation and resolution.

## Alignment via design-system-auditor

The design-system-auditor plugin automates the manual checklist above. Run it by providing the Figma file URL:

```
/frontend-craft:design-system-audit --figma <figma-file-url>
```

The audit does the following:
1. Reads Figma variables from the file using `get_variable_defs`.
2. Scans the project's CSS files for custom property definitions.
3. Applies the naming conversion rules to normalize both sides.
4. Produces a report categorizing every token into: aligned, code-only, Figma-only, name mismatch, or value mismatch.

The report output looks like:

```
=== Figma-Code Token Alignment Report ===

Aligned (42 tokens):
  --color-blue-500, --color-blue-600, --color-gray-200, ...

Code-only (5 tokens):
  --color-bg-overlay         rgba(0,0,0,0.5)
  --shadow-sm                0 1px 2px 0 rgba(0,0,0,0.05)
  --radius-badge             9999px
  --spacing-0-5              0.125rem
  --font-weight-semibold     600

Figma-only (3 variables):
  color/success/subtle       #f0fdf4
  spacing/2xl                48
  font/weight/black          900

Name mismatches (1):
  Figma: color/accent  ↔  CSS: --color-brand  (same value: #2563eb)

Value mismatches (2):
  --color-border-strong  Figma: #9ca3af  CSS: #d1d5db
  --spacing-lg           Figma: 32       CSS: 24
```

## Handling Code-Only Tokens

When a token exists in CSS but has no corresponding Figma variable, the token is invisible to designers. They cannot use it in designs, and drift is inevitable.

### Resolution process

1. **Evaluate necessity**: Is the token used in components that designers actively work with? If yes, it needs a Figma variable. If it is purely structural or code-internal (e.g., `--scrollbar-width`), it may not need one.

2. **Document the addition needed**: Create a request for the designer specifying exactly what to add:

```
Figma variable addition request:
  Collection: Semantic
  Variable name: color/bg/overlay
  Type: Color
  Value (Light mode): rgba(0, 0, 0, 0.5)
  Value (Dark mode): rgba(0, 0, 0, 0.7)
  Used in: Modal backdrop, dropdown overlay, image lightbox
```

3. **Track**: Keep a running list of code-only tokens that need Figma additions. Review this list with the design team regularly.

### Variables that should NOT be in Figma

Not every CSS token needs a Figma counterpart. Skip Figma addition for:

- Tokens controlling animation/transition (e.g., `--transition-duration-fast`).
- Tokens for code-only concerns like z-index layers (`--z-modal`, `--z-tooltip`).
- Structural tokens that have no visual design impact (e.g., `--container-max-width`).

## Handling Figma-Only Variables

When a variable exists in Figma but not in CSS, designers are using a value that the code cannot reference. Any implementation will hardcode the value or use the wrong token.

### Resolution process

1. **Determine the token layer**: Check which Figma collection the variable belongs to. This tells you whether to create a primitive or semantic CSS token.

2. **Create the CSS token in the correct file**:

```css
/* If Figma has color/success/subtle in the Primitives collection */
/* Add to tokens/colors.css */
:root {
  --color-green-50: #f0fdf4;
}

/* If it's in the Semantic collection */
/* Add to tokens/semantic.css */
:root {
  --color-success-subtle: var(--color-green-50);
}
```

3. **Match the Figma alias structure**: If the Figma variable references another variable, replicate that reference chain in CSS.

```
Figma: color/success/subtle → references → color/green/50
CSS:   --color-success-subtle: var(--color-green-50);
```

4. **Handle multi-mode values**: If the Figma variable has different values per mode (Light vs Dark), create the corresponding theme override:

```css
:root {
  --color-success-subtle: var(--color-green-50);
}
[data-theme="dark"] {
  --color-success-subtle: var(--color-green-900);
}
```

## Handling Name Mismatches

When the same value exists in both Figma and CSS under different names, the code side should be renamed to match Figma.

### Why Figma is the source of truth for names

- Designers name variables based on how they think about the design. These names carry semantic meaning from the design perspective.
- Code can be refactored with find-and-replace. Figma variable renames propagate automatically through designs.
- Design intent flows from Figma to code, not the other way around.

### Renaming process

1. **Identify all usages** of the CSS token being renamed:

```bash
grep -r '--color-brand' src/ --include='*.css' --include='*.tsx' --include='*.jsx'
```

2. **Create the new token** with the Figma-aligned name, initially pointing to the old one for safety:

```css
/* Temporary bridge — both names work */
:root {
  --color-brand: var(--color-blue-600);   /* OLD — to be removed */
  --color-accent: var(--color-blue-600);  /* NEW — matches Figma */
}
```

3. **Update all references** from `--color-brand` to `--color-accent` across the codebase.

4. **Remove the old token** once all references are updated.

### Exception: when Figma naming is clearly wrong

If a Figma variable name violates the naming conventions (e.g., `color/myBrandBlue` instead of `color/primary`), flag it as a naming improvement to discuss with the designer. Do not silently adopt a bad name. Propose a rename that both sides agree on.

## Handling Value Mismatches

When the same name exists in Figma and CSS but with different values, investigation is needed. One side is outdated.

### Resolution process

1. **Check change history**: Which side was updated more recently? If the designer adjusted the Figma value, update the CSS. If a developer changed the CSS token, check whether the design team was consulted.

2. **Check visual intent**: If Figma says `--color-border-strong` is `#9ca3af` (gray-400) and CSS has `#d1d5db` (gray-300), ask: does the design intend a stronger or lighter border? Align to the intended visual.

3. **Update the trailing side**:

```css
/* If Figma is correct (gray-400 for strong border) */
:root {
  --color-border-strong: var(--color-gray-400);  /* was gray-300, aligned to Figma */
}
```

4. **Verify the update**: Check all components using the changed token to confirm nothing breaks visually.

## Drift Prevention

Alignment is not a one-time activity. Without ongoing practices, Figma and code will diverge within weeks.

### Regular audit cadence

- Run the alignment audit (`/frontend-craft:design-system-audit --figma <url>`) at least once per sprint.
- Add it to your CI or pre-release checklist.
- Track the number of discrepancies over time. The trend should decrease.

### When adding a token to code

Every time a new CSS token is created:

1. Check whether a corresponding Figma variable exists.
2. If not, immediately document the Figma addition needed (see Code-Only Tokens above).
3. Include the Figma addition request in the same pull request or task that introduces the CSS token.

```
/* In the PR description or commit message */
New token: --color-info (semantic, references --color-blue-500)
Figma addition needed:
  Collection: Semantic
  Name: color/info
  Light: {Primitives/color/blue/500}
  Dark: {Primitives/color/blue/400}
```

### When a Figma variable is added by designers

When designers add new variables in Figma, the corresponding CSS tokens should be created promptly:

1. Designer notifies the team (via a handoff document, Slack message, or design review).
2. Developer creates the CSS tokens in the appropriate token files.
3. The new tokens go through the normal code review process.

### Preventing silent drift

- **Code reviews**: Reviewers should flag any new hardcoded color, spacing, or font value that should be a token.
- **Linting**: Use stylelint rules to disallow raw hex colors or pixel values in component CSS files (allow them only in `tokens/` files).
- **Design reviews**: When reviewing new Figma designs, check that new variables follow the naming convention and exist at the correct layer.

## Interpreting `get_variable_defs` Output

The `get_variable_defs` tool returns the complete set of Figma variables from a file. Understanding its output structure is essential for automated and manual comparison.

### Output structure

The tool returns data organized by collections and modes. Each variable has a name, type, and per-mode values:

```json
{
  "collections": [
    {
      "name": "Primitives",
      "modes": ["Value"],
      "variables": [
        {
          "name": "color/blue/500",
          "type": "COLOR",
          "valuesByMode": {
            "Value": { "r": 0.231, "g": 0.510, "b": 0.965, "a": 1 }
          }
        },
        {
          "name": "spacing/4",
          "type": "FLOAT",
          "valuesByMode": {
            "Value": 16
          }
        }
      ]
    },
    {
      "name": "Semantic",
      "modes": ["Light", "Dark"],
      "variables": [
        {
          "name": "color/primary",
          "type": "COLOR",
          "valuesByMode": {
            "Light": { "type": "VARIABLE_ALIAS", "name": "color/blue/600" },
            "Dark": { "type": "VARIABLE_ALIAS", "name": "color/blue/400" }
          }
        },
        {
          "name": "spacing/md",
          "type": "FLOAT",
          "valuesByMode": {
            "Light": { "type": "VARIABLE_ALIAS", "name": "spacing/4" },
            "Dark": { "type": "VARIABLE_ALIAS", "name": "spacing/4" }
          }
        }
      ]
    }
  ]
}
```

### How to interpret the data

**Collections** represent token layers:
- Look at the collection `name` to determine the layer (Primitives, Semantic, Components).
- If collection names are nonstandard, look at the values: raw values indicate primitives, aliases indicate semantic tokens.

**Modes** represent theme variants:
- A single-mode collection (e.g., `["Value"]`) holds values that do not change per theme (primitives).
- A multi-mode collection (e.g., `["Light", "Dark"]`) holds values that change per theme (semantic tokens).

**Variable values**:
- A raw value (hex object or number) is a primitive. Convert it to the CSS equivalent directly.
- A `VARIABLE_ALIAS` value references another variable. This corresponds to `var(--...)` in CSS.

**Color values**:
- Figma returns colors as RGBA objects with values from 0 to 1. Convert to CSS:
  - `{ r: 0.231, g: 0.510, b: 0.965, a: 1 }` becomes `#3b82f6` (multiply each channel by 255, round, convert to hex).
  - If `a` is less than 1, use `rgba()` format.

**Float values**:
- Figma stores spacing as unitless numbers (pixels). Convert to rem in CSS:
  - `16` becomes `1rem` (assuming 16px base).
  - `8` becomes `0.5rem`.

### Comparison workflow using `get_variable_defs`

1. **Parse the output** into a flat list of `{ name, layer, lightValue, darkValue }` entries.
2. **Convert names** from Figma format to CSS format (`color/primary` to `--color-primary`).
3. **Convert values** from Figma format to CSS format (RGBA objects to hex, floats to rem, aliases to `var()` references).
4. **Compare** against the CSS token files using the categorization from the Manual Alignment Checklist.
5. **Generate the report** listing aligned, code-only, Figma-only, name mismatches, and value mismatches.
