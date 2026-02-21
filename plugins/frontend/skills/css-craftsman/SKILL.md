---
name: css-craftsman
description: CSS debugging workflow and best-practice guidelines focused on visual/rendering defects and root-cause diagnosis. Use when layout/styling behavior is wrong (overflow, alignment, responsive breakage, specificity issues, stacking issues) or when CSS files need implementation-level fixes. Prefer this skill for debugging existing UI behavior; use design-system for token architecture/Figma sync and component-craft for shared component API/architecture decisions.
---

# CSS Craftsman

## Debugging Workflow

When you encounter a CSS problem, follow these five steps in order. Do NOT skip steps.

### Step 1: Identify

Parse the user's description. Determine:

- **Expected behavior**: What should the element look like or how should it be laid out?
- **Actual behavior**: What is happening instead?
- **Scope**: Is it one element, a group, or the whole page? Is it viewport-dependent?

If the description is vague, ask clarifying questions before proceeding.

### Step 2: Read Source

Read the relevant source files to understand what the code intends:

- The component file (`.tsx`, `.jsx`, `.vue`, etc.) to understand the DOM structure and any conditional classes or inline styles.
- The style file (`.module.css`, `.css`, `.scss`) to understand the authored CSS rules.
- Any parent components that control the layout context.

Note what the code is trying to do before you look at what the browser is actually doing.

### Step 3: Inspect DOM

**This step is NON-OPTIONAL. Never skip it.**

Spawn the `css-inspector` agent to get the actual browser DOM state. Provide it with:

- **URL**: The page where the problem appears (e.g., `http://localhost:3000/some-page`).
- **Selector**: The CSS selector for the target element.
- **Problem description**: What the user reported.

Rules for this step:

- If the dev server is not running, ask the user to start it. Do not proceed without a running page.
- If the selector is unknown, infer it from the component source code read in Step 2, or ask the user.
- Wait for the full diagnostic report before moving to Step 4.

The css-inspector agent will return computed styles, box model data, the parent chain, layout context, auto-detected issues, and a screenshot. This data is what you base your diagnosis on.

### Step 4: Diagnose

Compare the source code intent (Step 2) against the actual DOM report (Step 3). Identify the root cause.

Common root-cause patterns:

- **Parent layout mismatch**: The parent is `display: block` but you expected `flex` or `grid`.
- **Missing `min-width: 0`**: A flex child with `flex: 1` overflows because default `min-width: auto` prevents shrinking.
- **Overflow ancestor clipping**: An ancestor has `overflow: hidden` and the element extends beyond its bounds.
- **Specificity conflicts**: Another rule wins due to higher specificity, or a global style overrides a CSS Module class.
- **CSS Module scoping**: Class not applied due to incorrect import, wrong file, or `:global()` conflict.
- **Wrong DOM nesting**: A library component wraps content in unexpected elements, breaking flex/grid parent-child relationship.
- **Stacking context**: `z-index` not working because the element is in a different stacking context.
- **Zero-size element**: No width or height because no content, no explicit size, and parent does not stretch it.

State the root cause clearly before proposing a fix.

### Step 5: Fix and Verify

Apply the fix following the CSS Guidelines below. Then verify:

1. Take a Playwright screenshot after the fix to confirm the visual result.
2. If the fix does not resolve the issue, return to Step 4 with the new diagnostic data.

---

**KEY RULE: Never attempt CSS fixes without first completing Step 3 (DOM inspection).** Guessing at CSS fixes without seeing actual computed styles is the single most common cause of wasted effort.

---

## CSS Guidelines

Apply these rules whenever you write or modify CSS. Each rule is summarized below. For detailed guidance, examples, and edge cases, read the corresponding reference file.

### Layout — `references/layout.md`

- Grid for 2D layout, Flex for 1D. Choose based on current need.
- Sizing: content-based > ratio > range > fixed px.
- `flex: 1` always with `min-width: 0`. Grid: `minmax(0, 1fr)` to prevent content blowout.
- `gap` on parent, not margin between siblings.
- Responsive: mobile-first, container queries for components, `clamp()` for fluid values.
- Full-bleed/centering one-liners. Intrinsic sizing with `min()`/`max()`/`clamp()`. Sticky positioning flex/grid fix.

### DOM Structure — `references/dom-structure.md`

- Wrapper divs OK for layout if semantics preserved.
- Flex/grid items must be direct children.
- Library components: check className props first, inspect rendered DOM, wrap externally.

### Design Tokens & Theming — `references/design-tokens.md`

- Token hierarchy: primitive → semantic → component. Never skip layers.
- All colors, spacing, typography through tokens. No hardcoded values in components.
- Theme switching via CSS variable overrides on `[data-theme]` or `prefers-color-scheme`.
- Create a token when: used 3+ times, represents a design decision, or varies per theme.

### Typography — `references/typography.md`

- Font sizes in `rem` only. Define a type scale with tokens.
- Responsive type with `clamp()`. Never viewport units alone.
- Line height: unitless, 1.5 for body, 1.1-1.3 for headings.
- Max line length: `max-width: 65ch` for prose.
- `text-box: trim-both cap alphabetic` for optical centering. `text-wrap: balance`/`pretty`. Logical properties.

### z-index — `references/z-index.md`

- Use project-wide scale: base(0), dropdown(100), sticky(200), overlay(300), modal(400), toast(500).
- Always use scale variables, never raw numbers. `z-index: 9999` is a bug.
- Use `isolation: isolate` to contain stacking scope.

### Accessibility — `references/accessibility.md`

- DOM order = tab order = screen reader order.
- Touch targets: 44x44px team baseline (AA floor is 24x24 with exceptions). Font sizes in rem. Body line-height around 1.5.
- `:focus-visible` for keyboard focus. Never bare `outline: none`.
- Color contrast: 4.5:1 text, 3:1 UI components. Never color-only information.
- Respect `prefers-reduced-motion`.

### Performance & Animation — `references/performance.md`

- `will-change` only on animated elements. `contain` with decision table (layout paint, content, strict, inline-size).
- Animate only `transform` and `opacity`. Use `translate()` not `top`/`left`.
- `prefers-reduced-motion`: MUST respect. Wrap all animations.
- Avoid: nested calc(), `*` selector, `@import`.

### Defensive CSS — `references/defensive-css.md`

- `min-width: 0` on flex children. `img { max-width: 100%; height: auto }`.
- `overflow-wrap: break-word` for long strings. `min-height` over `height`.
- `scrollbar-gutter: stable`. `overscroll-behavior: contain`.
- Never `transition: all`. `overflow: clip` over `hidden`. `margin-trim` with padding. Sticky flex/grid fix.
- Test with long/short/empty/many content variations.

### Selectors & Specificity — `references/selectors.md`

- Max 3 levels of nesting. No `!important` (except documented utility classes).
- `@layer` for cascade control: `reset → base → components → utilities`. Native CSS nesting rules.
- No tag selectors for styling. CSS Module scoping handles specificity.
- Property order: layout → box model → typography → visual → misc.

### CSS Modules — `references/css-modules.md`

- `composes` for reuse. Minimize `:global()`.
- File: `ComponentName.module.css`. Classes: camelCase. No BEM.
- One module file per component. Don't mix styling approaches.
