---
name: design-system
description: Design system workflow and best-practice guidance for token architecture, theme modeling, compliance audits, and Figma-code synchronization. Use when defining or evolving primitives/semantics/component tokens, auditing token usage, resolving Figma drift, or planning DS migrations. Prefer this skill for system-level token decisions; use css-craftsman for isolated rendering bugs and component-craft for shared component API/composition decisions.
---

# Design System

## Workflow

This workflow has two modes. Choose based on the task.

### Mode A: New Work / Modification

Use when writing or modifying design-system-related code.

#### Step 1: Survey

Discover the project's token files, theme setup, and existing design system structure. Use Glob to find token/variable files (e.g., `**/*token*`, `**/*variable*`, `**/*theme*`). Read them to understand what currently exists: token layers, naming conventions, theme implementation, and which components already use tokens.

#### Step 2: Figma Check

If the Figma plugin is available, use `get_variable_defs` to read the current Figma variable state. Compare the variable collections, modes, and naming structure against the code tokens discovered in Step 1.

If the Figma plugin is not available, skip this step and note that Figma state was not verified.

#### Step 3: Gap Analysis

Compare code tokens against Figma variables. Note:

- **Missing tokens**: Values in Figma that have no code counterpart, or code values with no Figma variable.
- **Naming inconsistencies**: Tokens that represent the same concept but use different names in code vs Figma.
- **Structural mismatches**: Different grouping, different layer hierarchy, or missing semantic mappings.

#### Step 4: Execute

Apply changes following the guidelines below. Key rules during execution:

- All styling must go through tokens. Never hardcode color, spacing, typography, or shadow values in component CSS.
- Follow the three-layer token hierarchy (primitive, semantic, component).
- Ensure dark mode and theming work through token overrides, not conditional logic.

#### Step 5: Figma Guide

If changes introduced new tokens or renamed existing ones, provide a clear guide of what should be updated in Figma. The guide must specify:

- New variables to add (with collection, group, and suggested values).
- Variables to rename (old name and new name).
- New modes to add if applicable.

**Never modify Figma directly. Existing Figma content must be preserved — additions only.**

### Mode B: Audit

Use when assessing design system health or compliance.

#### Step 1: Spawn Audit

Spawn the `design-system-auditor` agent with the target path (and Figma URL if available).

#### Step 2: Review Report

Review the audit report returned by the agent. Understand the findings: hardcoded values, missing tokens, naming violations, Figma drift, theme coverage gaps.

#### Step 3: Prioritize

Prioritize fixes based on severity:

1. **Critical** — Broken theming, tokens pointing to nonexistent values, hardcoded colors that break dark mode.
2. **Warning** — Naming inconsistencies, skipped token layers, Figma-code drift.
3. **Info** — Minor naming suggestions, unused tokens, optimization opportunities.

#### Step 4: Execute Fixes

Execute fixes following the Mode A workflow (Steps 1-5) for each issue, starting from the highest severity.

---

**KEY RULE: Never modify Figma content directly. Only provide guides for what should be added. Existing Figma designs and variables must be preserved.**

---

## Guidelines

Apply these rules whenever you work with design system tokens, theming, or component styling. Each rule is summarized below. For detailed guidance, examples, and edge cases, read the corresponding reference file.

### Token Architecture — `references/token-architecture.md`

- Three-layer hierarchy: primitive, semantic, component. Never skip layers. Raw values only in primitives.
- `@property` registration for type-safe tokens. Relative color syntax (OKLCH) for palette generation. Multi-brand token architecture. `contrast-color()` for auto text contrast.

### Component Styling — `references/component-styling.md`

- Scope component tokens locally. Variants through token switching. All interaction states (hover, disabled) via tokens.

### Figma-Code Sync — `references/figma-code-sync.md`

- Figma variable names map to CSS variable names. Check alignment both directions. Preserve existing Figma content.

### Migration — `references/migration.md`

- Priority: colors, then spacing, then typography, then borders/shadows. Migrate per-component. Verify no visual change.

### CSS Pitfalls — `references/css-pitfalls.md`

- No `var()` fallbacks that hide missing tokens. CSS variables cannot be used in media queries. Watch dark mode non-color properties.
- IACVT behavior and `@property` fix. `!important` on custom properties. `@scope` for proximity-based token scoping. `@layer` for token cascade control. `color-mix()` for runtime color derivation. Modern color space `@supports` fallbacks.

### Bootstrapping — `references/bootstrapping.md`

- Token creation order: colors, spacing, typography, borders/shadows, semantic tokens, dark theme. Semantic classification by role (bg, fg, border, interactive). Component build order from atoms to composites.
- OKLCH-based palette generation. Modern dark mode: `color-scheme`, `light-dark()`, system colors, `currentColor` for icons (with fallbacks/progressive enhancement for older browser matrices). Checklist includes `@property`, `interpolate-size`, `text-wrap`.
