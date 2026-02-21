# CSS Pitfalls When Using Design Tokens

## 1. var() Fallback Abuse

### The Problem

Adding fallback values to `var()` silently hides missing or misspelled tokens. The component renders "correctly" with the fallback, so the broken token reference is never caught during development or testing.

```css
/* BAD: hides the missing token — you will never notice --colour-text is misspelled */
color: var(--colour-text, #333333);

/* BAD: hides a renamed token — --color-text-primary was renamed to --color-text */
color: var(--color-text-primary, #111827);
```

The component looks fine. The token is broken. Nobody notices until someone audits the CSS months later.

### The Correct Approach

Omit fallback values in component CSS. A missing token should produce a visible failure that gets caught in testing.

```css
/* GOOD: if --color-text is undefined, the property becomes invalid
   and the element inherits or uses the initial value — visually obvious breakage */
color: var(--color-text);
```

### When Fallbacks ARE Appropriate

**During active migration:** When a token may not exist yet in the system but you are progressively migrating, a fallback preserves the current appearance. Remove the fallback once the token is confirmed to exist.

```css
/* Acceptable during migration — remove fallback once --shadow-sm is defined */
box-shadow: var(--shadow-sm, 0 1px 3px rgba(0, 0, 0, 0.1));
```

**Progressive enhancement with third-party consumers:** If your CSS is consumed by external projects that may not define your tokens, fallbacks prevent breakage in those environments.

```css
/* Widget CSS shipped to third parties who may not load the token stylesheet */
.widget {
  color: var(--color-text, #1f2937);
  background: var(--color-bg-surface, #ffffff);
}
```

**Composable component tokens with sensible defaults:** Component-level tokens that allow override but work standalone.

```css
.badge {
  --badge-bg: var(--color-primary);
  --badge-text: var(--color-text-inverse);
  --badge-radius: var(--radius-full);

  /* Consumer can override --badge-bg without touching the component CSS */
  background: var(--badge-bg);
  color: var(--badge-text);
  border-radius: var(--badge-radius);
}
```

## 2. calc() with Tokens

### The Problem

`calc()` requires spaces around `+` and `-` operators. Missing spaces cause the entire expression to fail silently — the property is treated as invalid and ignored.

```css
/* BAD: no spaces around operator — entire declaration is INVALID */
width: calc(var(--spacing-md)*2);
padding: calc(var(--spacing-lg)-var(--spacing-sm));

/* BAD: space on only one side — still INVALID for + and - */
margin: calc(var(--spacing-md)- 4px);
```

Note: `*` and `/` do not technically require spaces, but always add them for consistency and readability.

### The Correct Approach

```css
/* GOOD: spaces around all operators */
width: calc(var(--spacing-md) * 2);
padding: calc(var(--spacing-lg) - var(--spacing-sm));
margin: calc(100% - var(--spacing-xl));
```

### Unit Mismatch Traps

`calc()` can mix compatible units (px + rem, % + px), but you must know what your tokens resolve to. Mixing incompatible types causes silent failure.

```css
/* DANGEROUS: what unit is --spacing-md?
   If it's 1rem, this works: calc(100% - 1rem) ✓
   If it's unitless 16, this fails: calc(100% - 16) ✗ */
width: calc(100% - var(--spacing-md));
```

Rule: spacing tokens must always have units. Document whether your tokens use `rem` or `px`.

### Prefer New Tokens Over Complex calc()

If you find yourself writing complex `calc()` expressions with tokens, consider whether a new token would be clearer.

```css
/* QUESTIONABLE: complex calc for what is really a design decision */
padding: calc(var(--spacing-md) + var(--spacing-xs));

/* BETTER: if 20px padding is a deliberate choice, make it a token */
padding: var(--spacing-5); /* 1.25rem / 20px — added to the scale */

/* OR use a component token */
.sidebar {
  --sidebar-padding: var(--spacing-md);
  padding: var(--sidebar-padding);
}
```

## 3. CSS Modules :root Scope

### The Problem

CSS Modules scope class names to the component, but `:root` is global. Tokens defined in `:root` leak across all modules. This creates two failure modes:

**Failure 1: Component tokens in :root pollute the global scope.**

```css
/* Button.module.css — BAD */
:root {
  --button-bg: var(--color-primary);
  --button-text: #ffffff;
  --button-radius: var(--radius-md);
}

/* These are now global. Any element in any file can access --button-bg.
   Another component could accidentally depend on them. */
```

**Failure 2: Redefining global tokens inside a module creates unpredictable overrides.**

```css
/* Sidebar.module.css — BAD */
:root {
  --color-primary: var(--color-green-600);  /* "I want green buttons in the sidebar" */
}

/* This changes --color-primary for the ENTIRE page, not just the sidebar.
   Every component using --color-primary is now green. */
```

### The Correct Approach

Component tokens are scoped to the component selector. Global tokens live only in the global token stylesheet.

```css
/* tokens/global.css — the ONE place :root tokens are defined */
:root {
  --color-primary: var(--color-blue-600);
  --color-text: var(--color-gray-900);
}

/* Button.module.css — component tokens scoped to the component */
.button {
  --button-bg: var(--color-primary);
  --button-text: #ffffff;
  --button-radius: var(--radius-md);

  background: var(--button-bg);
  color: var(--button-text);
  border-radius: var(--button-radius);
}

/* Sidebar.module.css — override via component token, not global */
.sidebar .button {
  --button-bg: var(--color-green-600);
  /* Only buttons inside .sidebar are affected */
}
```

## 4. Media Query CSS Variable Limitation

### The Problem

CSS custom properties cannot be used in media query conditions. This is a specification limitation, not a browser bug. It will never work.

```css
:root {
  --breakpoint-sm: 640px;
  --breakpoint-md: 768px;
  --breakpoint-lg: 1024px;
}

/* IMPOSSIBLE — the browser ignores this entire media query */
@media (min-width: var(--breakpoint-md)) {
  .container {
    max-width: 720px;
  }
}
```

The browser parses media queries before custom properties are resolved. Custom properties are resolved at computed-value time, which happens after media query evaluation.

### The Correct Approach

**Option 1: Use fixed values with comments referencing the token name.**

```css
/* Breakpoint values — keep in sync with design tokens documentation */
/* --breakpoint-sm: 640px */
/* --breakpoint-md: 768px */
/* --breakpoint-lg: 1024px */
/* --breakpoint-xl: 1280px */

@media (min-width: 768px) { /* --breakpoint-md */
  .container {
    max-width: 720px;
  }
}

@media (min-width: 1024px) { /* --breakpoint-lg */
  .container {
    max-width: 960px;
  }
}
```

**Option 2: Use preprocessor variables if available.**

```scss
// _breakpoints.scss
$breakpoint-sm: 640px;
$breakpoint-md: 768px;
$breakpoint-lg: 1024px;

// component.scss
@media (min-width: $breakpoint-md) {
  .container {
    max-width: 720px;
  }
}
```

**Option 3: Use container queries for component-level responsiveness.** Container *size* queries evaluate against the container's dimensions. Container *style* queries (`@container style(--var: value)`) can read CSS custom properties (Chrome 111+, Safari 18+; no Firefox yet).

```css
.card-grid {
  container-type: inline-size;
}

@container (min-width: 600px) {
  .card {
    grid-template-columns: 1fr 1fr;
  }
}
```

**Option 4: Define breakpoints as JavaScript constants** and use them in JS-driven responsive logic (e.g., `matchMedia` or framework-specific hooks).

```javascript
// breakpoints.js — single source of truth
export const BREAKPOINTS = {
  sm: 640,
  md: 768,
  lg: 1024,
  xl: 1280,
};
```

## 5. Dark Mode Non-Color Properties

### The Problem

When implementing dark mode, developers often only remap colors. But several non-color properties need adjustment for dark backgrounds to maintain visual quality and readability.

### Box Shadows

Shadows on dark backgrounds behave differently. A subtle shadow that works on white is invisible on dark gray. Shadow colors may also need to change.

```css
/* Light mode: subtle shadow with semi-transparent black */
:root {
  --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 6px rgba(0, 0, 0, 0.1);
}

/* Dark mode: increase opacity and potentially add a subtle light edge */
[data-theme="dark"] {
  --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.3);
  --shadow-md: 0 4px 6px rgba(0, 0, 0, 0.4);
}
```

### Opacity

Elements with reduced opacity may become unreadable on dark backgrounds.

```css
/* Light mode: 60% opacity for muted text is readable on #ffffff */
.text-muted {
  opacity: var(--opacity-muted);
}

:root {
  --opacity-muted: 0.6;
}

/* Dark mode: 60% opacity makes light text too faint on dark backgrounds */
[data-theme="dark"] {
  --opacity-muted: 0.75;
}
```

### Border Width

Fine 1px borders that are visible on light backgrounds can disappear on dark backgrounds, especially on lower-contrast displays.

```css
:root {
  --border-width-subtle: 1px;
}

/* Dark mode: bump subtle borders to 1.5px or use a lighter border color */
[data-theme="dark"] {
  --border-width-subtle: 1.5px;
}
```

### Background Images and Gradients

Gradients using color tokens update automatically only if they reference tokens. Hardcoded gradient colors will not adapt.

```css
/* BAD: hardcoded gradient colors — broken in dark mode */
.hero {
  background: linear-gradient(135deg, #667eea, #764ba2);
}

/* GOOD: gradient uses tokens that remap per theme */
.hero {
  background: linear-gradient(135deg, var(--color-gradient-start), var(--color-gradient-end));
}

:root {
  --color-gradient-start: #667eea;
  --color-gradient-end: #764ba2;
}

[data-theme="dark"] {
  --color-gradient-start: #4c5ecc;
  --color-gradient-end: #5e3a87;
}
```

### Filter: drop-shadow

`filter: drop-shadow()` with hardcoded colors does not respond to theme changes.

```css
/* BAD */
.icon {
  filter: drop-shadow(0 1px 2px rgba(0, 0, 0, 0.2));
}

/* GOOD: use a token for the shadow color */
.icon {
  filter: drop-shadow(0 1px 2px var(--color-shadow));
}
```

## 6. Token Chain Performance

### The Problem

Design tokens are structured in layers: component references semantic, semantic references primitive. Each level adds one `var()` resolution step.

```css
/* 3 levels of indirection */
.button {
  --button-bg: var(--color-primary);       /* component → semantic */
}
:root {
  --color-primary: var(--color-blue-600);  /* semantic → primitive */
  --color-blue-600: #2563eb;              /* primitive → raw value */
}
/* Resolution chain: --button-bg → --color-primary → --color-blue-600 → #2563eb */
```

### Guidelines

**3 levels of indirection is fine.** This is the standard component-semantic-primitive architecture. All modern browsers resolve these chains efficiently at computed-value time. There is no measurable performance impact.

**More than 3 levels should be avoided.** Deep chains make debugging difficult — inspecting a value in DevTools requires tracing through multiple definitions. They also create fragile dependency chains where a change in one intermediate token has hard-to-predict cascading effects.

```css
/* BAD: 5 levels deep — hard to debug, hard to trace */
--button-primary-bg: var(--button-bg);
--button-bg: var(--interactive-primary);
--interactive-primary: var(--color-primary);
--color-primary: var(--color-blue-600);
--color-blue-600: #2563eb;
```

**If you find yourself exceeding 3 levels,** it usually means one of:
- An unnecessary alias layer exists. Remove it.
- Two semantic layers were created (e.g., "semantic" and "contextual"). Flatten to one.
- Component tokens are referencing other component tokens. Components should reference semantic tokens, not each other.

### Debugging Tip

In browser DevTools, computed styles show the final resolved value. To trace the chain, inspect the element's styles panel — it shows each `var()` reference. If the chain is longer than component-semantic-primitive, refactor.

## 7. Specificity Conflicts with Theme Overrides

### The Problem

Theme selectors like `[data-theme="dark"]` have relatively low specificity (0-1-0 for a single attribute selector). Component selectors with nesting, combinators, or pseudo-classes can easily outweigh them.

```css
/* Theme override: specificity 0-1-0 (one attribute selector) */
[data-theme="dark"] {
  --color-text: var(--color-gray-50);
}

/* Component rule: specificity 0-2-0 (two class selectors) */
.sidebar .nav-item {
  color: var(--color-gray-900);  /* Uses primitive, not semantic token */
}

/* Result: in dark mode, .sidebar .nav-item is still using --color-gray-900 (dark text).
   The theme override changed --color-text, but the component never used --color-text. */
```

This is not a specificity war between the component selector and the theme selector competing for the same property. The actual problem is that the component used a primitive token (`--color-gray-900`) instead of the semantic token (`--color-text`). Primitives do not change between themes. Only semantics do.

### The Correct Approach

**Rule: components must ALWAYS use semantic tokens, never primitives.**

```css
/* GOOD: component uses semantic token that changes per theme */
.sidebar .nav-item {
  color: var(--color-text);
}

/* Theme override works because it redefines --color-text */
[data-theme="dark"] {
  --color-text: var(--color-gray-50);
}
```

If a component needs a color that differs from the standard `--color-text`, create a semantic token for that purpose:

```css
:root {
  --color-nav-text: var(--color-gray-800);
}

[data-theme="dark"] {
  --color-nav-text: var(--color-gray-100);
}

.sidebar .nav-item {
  color: var(--color-nav-text);
}
```

### Specificity Tip for Theme Selectors

If you must increase theme selector specificity (e.g., to override legacy styles), double the attribute selector:

```css
/* Higher specificity: 0-2-0 */
[data-theme="dark"][data-theme="dark"] {
  --color-text: var(--color-gray-50);
}
```

This is a temporary workaround. The real fix is to refactor components to use semantic tokens.

## 8. Transitions with Token Values

### The Problem

CSS transitions and animations work with CSS custom property values. When a theme switch changes the value of a token, any component with a `transition` on that property will animate the change.

```css
.card {
  background: var(--color-bg-surface);
  color: var(--color-text);
  transition: background 0.2s ease, color 0.2s ease;
}

/* When theme switches from light to dark:
   - background animates from #ffffff to #1f2937 over 200ms
   - color animates from #111827 to #f9fafb over 200ms */
```

This may or may not be desired. Animated theme transitions can look polished, but they can also look buggy — elements animate at different speeds depending on their transition durations, creating a chaotic "ripple" effect across the page.

### Decide: Animated or Instant Theme Switch?

**If animated theme switching is desired:**

Only animate when the user has **not** enabled reduced motion.

Ensure all themed properties have matching transition durations so the switch feels coordinated.

```css
/* All themed elements use the same transition duration */
:root {
  --theme-transition-duration: 0.3s;
}

@media (prefers-reduced-motion: no-preference) {
  .card {
    transition: background var(--theme-transition-duration) ease,
                color var(--theme-transition-duration) ease,
                border-color var(--theme-transition-duration) ease;
  }

  .button {
    transition: background var(--theme-transition-duration) ease,
                color var(--theme-transition-duration) ease;
  }
}
```

**If instant theme switching is desired (more common):**

Temporarily disable transitions during the theme switch using a class.

```css
/* Applied to <html> during theme switch, removed after a frame */
.theme-switching,
.theme-switching *,
.theme-switching *::before,
.theme-switching *::after {
  transition-duration: 0s !important;
  animation-duration: 0s !important;
}
```

```javascript
// Theme switch logic
function switchTheme(newTheme) {
  document.documentElement.classList.add('theme-switching');
  document.documentElement.setAttribute('data-theme', newTheme);

  // Remove the class after one frame to re-enable transitions
  requestAnimationFrame(() => {
    requestAnimationFrame(() => {
      document.documentElement.classList.remove('theme-switching');
    });
  });
}
```

The double `requestAnimationFrame` ensures the browser has painted the new theme before transitions are re-enabled.

### Respecting User Preferences

Users who have enabled `prefers-reduced-motion` should not see animated theme transitions.

```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    transition-duration: 0.01ms !important;
    animation-duration: 0.01ms !important;
  }
}
```

This applies globally, not just to theme switches. It ensures motion-heavy transitions are minimized for users who need it.

### Watch Out: Interaction Transitions Conflicting with Theme Transitions

Components often have hover/focus transitions that should remain even during an instant theme switch. The `.theme-switching` class disables ALL transitions, including interactive ones. If a user is hovering a button during a theme switch, the hover transition will be skipped.

In practice this is rarely noticed because theme switches happen on a deliberate user action (clicking a toggle). But if theme switches happen automatically (e.g., system preference change at sunset), consider a more targeted approach:

```css
/* Only disable transitions on theme-dependent properties */
.theme-switching * {
  transition-property: none !important;
}

/* But this also disables hover transitions. A more surgical approach: */
.theme-switching * {
  transition-duration: 0s !important;
}
/* Interaction transitions will resume immediately after .theme-switching is removed */
```

## 9. Custom Property Invalid Value Behavior (IACVT)

### The Problem

When a custom property resolves to an invalid value, the property becomes "Invalid At Computed-Value Time" (IACVT). The fallback behavior is *inheritance*, not the previous valid declaration:

```css
html { --color: notacolor; }
body { color: blue; }
p {
  color: green;
  color: var(--color);
}
/* Result: p is BLUE (inherited from body), NOT green */
```

Compare with a direct invalid value:

```css
p {
  color: green;
  color: notacolor;
}
/* Result: p is GREEN (previous valid declaration applies) */
```

### Why This Matters for Token Systems

If a consumer sets a token to a nonsensical value, the fallback is inheritance from a potentially distant ancestor — not the previous declaration. This produces unpredictable results that are hard to debug.

### The Fix

Use `@property` registration to define valid syntax and a guaranteed fallback:

```css
@property --color-primary {
  syntax: '<color>';
  inherits: true;
  initial-value: #2563eb;
}

:root {
  --color-primary: notacolor;
}

.button {
  background: var(--color-primary);
  /* Falls back to #2563eb (initial-value), NOT inheritance */
}
```

### Modern Color Space Fallbacks

When using modern color spaces (oklch, lab), wrap in `@supports` for older browsers:

```css
:root {
  --color-primary: #2563eb; /* Safe fallback */
}
@supports (color: oklch(55% 0.2 260)) {
  :root {
    --color-primary: oklch(55% 0.2 260);
  }
}
```

## 10. !important and Custom Properties

`!important` on a custom property declaration elevates the *declaration* in the cascade — it is NOT part of the stored value:

```css
div { --color: red !important; }
.child { --color: blue; color: var(--color); }
/* Result: red wins — !important on div's declaration beats higher specificity */
```

The value stored in `--color` is `red`, not `red !important`. Use `!important` on design system tokens only when you explicitly intend to prevent all downstream overrides.

## 11. @scope for Token Scoping

`@scope` provides proximity-based cascade resolution — closer ancestor wins regardless of source order:

```css
@scope (.theme-dark) { a { color: cyan; } }
@scope (.theme-light) { a { color: navy; } }

/* With nested themes, the closest ancestor scope wins */
```

This eliminates the classic "nested theme override" specificity bug. Use `@scope` with donut scoping (`@scope (root) to (limit)`) for component shells that style themselves but not their content slots.

**Browser support note:** Evaluate before production use. Does not progressively enhance — unsupported browsers apply no scoped styles.

## 12. @layer for Token Cascade Control

Cascade layers (`@layer`) provide explicit control over which token overrides win, independent of specificity or source order.

```css
@layer tokens, themes, components, overrides;

@layer tokens {
  :root {
    --color-primary: var(--color-blue-600);
    --spacing-md: var(--spacing-4);
  }
}

@layer themes {
  [data-theme="dark"] {
    --color-primary: var(--color-blue-400);
  }
}

@layer components {
  .button { --button-bg: var(--color-primary); }
}
```

**Key rule:** Theme overrides belong in a layer above base tokens but below component-level overrides. This prevents specificity wars between `[data-theme]` selectors and component classes.

**Pitfall:** Unlayered styles always beat layered styles. If any token definitions are outside `@layer`, they will override everything in layers regardless of order.

## 13. color-mix() for Runtime Color Manipulation

`color-mix()` creates derived colors at runtime without defining new tokens for every variation:

```css
.button:hover {
  background: color-mix(in oklch, var(--button-bg) 85%, black);
}

.button:disabled {
  background: color-mix(in oklch, var(--button-bg) 40%, transparent);
}

.card {
  border-color: color-mix(in srgb, var(--color-primary) 20%, transparent);
}
```

**When to use vs when to tokenize:**
- Use `color-mix()` for predictable derivations (hover = darken 15%, disabled = 40% opacity).
- Create explicit tokens when the derived value is a design decision that may change independently.

**Pitfall:** `color-mix()` requires both inputs to be valid computed colors. `var()` with a fallback that is not a valid color will produce IACVT. Always ensure token values resolve to valid colors.

## References

- MDN CSS custom properties (cascading variables): https://developer.mozilla.org/docs/Web/CSS/CSS_cascading_variables
- MDN `var()`: https://developer.mozilla.org/docs/Web/CSS/var
- MDN `@property`: https://developer.mozilla.org/docs/Web/CSS/@property
- MDN `@scope`: https://developer.mozilla.org/docs/Web/CSS/@scope
- MDN cascade layers (`@layer`): https://developer.mozilla.org/docs/Web/CSS/@layer
- MDN `color-mix()`: https://developer.mozilla.org/docs/Web/CSS/color_value/color-mix
- MDN `prefers-reduced-motion`: https://developer.mozilla.org/docs/Web/CSS/@media/prefers-reduced-motion
