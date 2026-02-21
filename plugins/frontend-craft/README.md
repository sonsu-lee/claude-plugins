# Frontend Craft

Three specialized skills that make Claude Code an expert frontend partner — diagnose CSS issues with live browser inspection, enforce design system token compliance with Figma alignment, and guide component architecture decisions with UX pattern checklists.

**For:** Frontend developers building component-based UIs with design systems, CSS Modules, and Figma-to-code workflows.

## What This Does

### Without this plugin
> "Fix the sidebar overlap" → Claude guesses at CSS changes, applies trial-and-error fixes

### With this plugin
> "Fix the sidebar overlap" → Claude inspects the live DOM via Playwright, reads computed styles, identifies the root cause (`min-width: auto` on a flex child), and applies the correct fix following CSS best practices

---

## Skills

### CSS Craftsman — CSS Debugging & Best Practices

Triggers when you describe CSS problems or work on CSS/style files.

Forces a "look first, fix second" workflow: inspects the actual DOM via Playwright before attempting fixes. Includes 10 guideline areas (layout, `@layer`, accessibility, performance, design tokens, etc.).

**Agent:** `cascading-style-sheets-inspector` — Extracts computed styles, box model, parent chain, and auto-detects issues.
**Command:** `/frontend-craft:cascading-style-sheets-debug <url> <selector>` — Manual element inspection.

```
"The sidebar is overlapping the main content"
"The card grid isn't wrapping properly"
```

### Design System — Token Management & Figma Alignment

Triggers when you work with design tokens, theming, or Figma synchronization.

Guides token architecture (primitive → semantic → component), audits for hardcoded values, checks theme coverage, and verifies Figma-code alignment. Never modifies Figma directly — provides guides for additions only.

**Agent:** `design-system-auditor` — Scans code for hardcoded values, token violations, theme gaps, Figma misalignment.
**Command:** `/frontend-craft:design-system-audit [path] [--figma <url>]` — Manual compliance audit.

```
"Tokenize the hardcoded colors in this component"
"Check if our tokens match Figma variables"
```

### Component Craft — UI Component Design Guidance

Triggers when you create, modify, or review shared UI components.

Guides extension vs separation decisions, prop API design, UX pattern compliance (10 patterns including pagination, modal, select, toggle, dropdown menu), and design review. Flags non-standard UX patterns and proposes alternatives.

```
"Should I add this variant to Button or make a new component?"
"Create a new Select component for our UI kit"
```

## Prerequisites

- [Playwright plugin](https://github.com/anthropics/claude-plugins-official) required for CSS debugging (live DOM inspection)
- [Figma plugin](https://github.com/anthropics/claude-plugins-official) recommended for design system Figma cross-referencing (not required)

## Installation

```bash
# Local development
claude --plugin-dir ./frontend-craft
```

```text
# Marketplace installation (inside Claude Code)
/plugin install frontend-craft@claude-plugin-directory
```

Plugin command invocations are namespaced by plugin name:
- `/frontend-craft:cascading-style-sheets-debug`
- `/frontend-craft:design-system-audit`

## Skill Routing Precedence

Use this table when a request can match more than one skill.

| User intent | Primary skill | Use this when | Handoff to |
|-------------|---------------|---------------|------------|
| Visual bug/debugging | `css-craftsman` | Layout breakage, overflow, specificity, stacking, responsive rendering issues | `design-system` if root cause is token architecture or theme model drift |
| Token/theming system design | `design-system` | Defining token layers, DS compliance audits, theme strategy, Figma-code sync | `css-craftsman` for isolated rendering defects after token strategy is clear |
| Shared component architecture | `component-craft` | Extend-vs-split decisions, composition patterns, prop API, UX pattern compliance | `design-system` for system-level token choices; `css-craftsman` for final rendering/debug fixes |

## Components

| Component | Type | Source Skill |
|-----------|------|-------------|
| `css-craftsman` | Skill | CSS debugging workflow + 10 CSS guidelines |
| `design-system` | Skill | Token management workflow + 6 DS guidelines |
| `component-craft` | Skill | Component design workflow + 5 design guidelines |
| `cascading-style-sheets-inspector` | Agent | Live DOM/CSS inspection via Playwright |
| `design-system-auditor` | Agent | Design system compliance audit |
| `/frontend-craft:cascading-style-sheets-debug` | Command | Manual CSS element inspection |
| `/frontend-craft:design-system-audit` | Command | Manual DS compliance audit |

## Guidelines Reference

### CSS Craftsman (10 areas)

| Guideline | Key rules |
|-----------|-----------|
| Layout | Grid for 2D, Flex for 1D. `gap` on parent. Full-bleed/centering patterns. Sticky flex/grid fix. |
| DOM Structure | Wrapper divs OK for layout. Direct children for flex/grid. |
| Design Tokens | Primitive > semantic > component. No hardcoded values. |
| Typography | `rem` only. `clamp()` for responsive. `text-box` trimming. `text-wrap: balance/pretty`. Logical properties. |
| z-index | 6-tier scale. `isolation: isolate`. No raw numbers. Flex/grid items work without `position`. |
| Accessibility | DOM order = tab order. 44px team target baseline (24px AA floor with exceptions). 4.5:1 contrast. |
| Performance | `transform`/`opacity` only for animation. `contain` decision table. Respect reduced motion. |
| Defensive CSS | `min-width: 0` on flex children. `overflow: clip`. `margin-trim`. Transition safety. |
| Selectors | Max 3 nesting. No `!important`. `@layer` cascade control. Native CSS nesting. Property order convention. |
| CSS Modules | `composes` for reuse. camelCase. One file per component. |

### Design System (6 areas)

| Guideline | Key rules |
|-----------|-----------|
| Token Architecture | Three-layer hierarchy. `@property` type-safe tokens. OKLCH palette generation. Multi-brand. |
| Component Styling | Scope tokens locally. Variants via token switching. |
| Figma-Code Sync | Naming mapping. Preserve existing Figma. Drift prevention. |
| Migration | Colors → spacing → typo → borders. Per-component. No visual change. |
| CSS Pitfalls | No var() fallback abuse. IACVT behavior. `@scope` for token scoping. `@layer` for cascade. `color-mix()`. `!important` on custom props. |
| Bootstrapping | Token creation order. OKLCH palettes. Modern dark mode (`light-dark()` + `color-scheme`, system colors). Component build order. |

### Component Craft (5 areas)

| Guideline | Key rules |
|-----------|-----------|
| Composition | Same purpose → variant. Different → separate. Compound for complex UI. |
| API Design | Consistent naming. Controlled + uncontrolled. No breaking changes. |
| UX Patterns | 10 pattern checklists with framework refs and algorithm names. |
| Review Guide | 3+ usage. Single responsibility. Prop count < 10. Red flags list. |
| Implementation Patterns | 17 component CSS recipes (+ Carousel, OTP Input). Anchor positioning. Native styleable select. `@starting-style` animations. |
