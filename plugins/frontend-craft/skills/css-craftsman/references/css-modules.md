# CSS Module Conventions

## File Naming

Name CSS module files to match their component:

```
Button.tsx        -> Button.module.css
CardHeader.tsx    -> CardHeader.module.css
NavItem.tsx       -> NavItem.module.css
```

One CSS module file per component. Do not create shared CSS module files that serve multiple components — use `composes` to share instead.

## Class Naming

Use camelCase for all class names. Do not use BEM, kebab-case, or any other convention — CSS Modules handle scoping.

```css
/* CORRECT */
.card { }
.cardHeader { }
.cardBody { }
.navItem { }
.navItemActive { }

/* WRONG: BEM is redundant with CSS Modules */
.card__header { }
.card__header--active { }

/* WRONG: kebab-case requires bracket access in JS */
.card-header { }
```

camelCase allows clean dot-notation access in JS:

```jsx
// Clean
<div className={styles.cardHeader}>

// Awkward (required for kebab-case)
<div className={styles['card-header']}>
```

## Import Pattern

Always use the default import pattern:

```jsx
import styles from './Component.module.css';
```

Apply classes directly:

```jsx
<div className={styles.container}>
  <h2 className={styles.title}>{title}</h2>
</div>
```

For conditional classes, use string concatenation or a utility like `clsx`:

```jsx
<div className={`${styles.tab} ${isActive ? styles.tabActive : ''}`}>

// Or with clsx
<div className={clsx(styles.tab, isActive && styles.tabActive)}>
```

## composes

Use `composes` to share styles between classes within the same file or across files:

```css
/* Within the same file */
.base {
  padding: 8px 16px;
  border-radius: 4px;
  font-size: 1rem;
}

.primary {
  composes: base;
  background: var(--color-primary);
  color: white;
}

.secondary {
  composes: base;
  background: var(--color-secondary);
  color: white;
}
```

```css
/* From another file */
.heading {
  composes: textLarge from './typography.module.css';
  margin-bottom: 16px;
}
```

Rules for `composes`:
- `composes` must be the first declaration in a rule block
- Do not compose from more than 2-3 sources — it becomes hard to trace
- Prefer composing from a shared module (e.g., `typography.module.css`, `spacing.module.css`) over duplicating values

## Minimize :global()

`:global()` breaks CSS Module scoping. Use it only when you must target elements outside your control:

```css
/* Acceptable: targeting a third-party library class */
:global(.tippy-content) {
  padding: 0;
}

/* Acceptable: targeting a state class added by JS/framework */
.menu :global(.is-open) {
  display: block;
}
```

Never use `:global()` for your own component styles. If you feel you need it, the component structure needs fixing.

## Do Not Mix Styling Approaches

Within a single component, use one styling method. Do not combine CSS Modules with:

- Inline `style` props for layout/theming (conditional dynamic values are acceptable)
- CSS-in-JS (styled-components, Emotion)
- Tailwind utility classes
- Global stylesheets

If the project uses CSS Modules, all component styles go in the module file. Inline `style` is acceptable only for truly dynamic values that change per-render (e.g., `style={{ left: position.x }}`).

## Typed CSS Modules

If the project generates `.module.css.d.ts` type declaration files (via `typed-css-modules`, `typescript-plugin-css-modules`, or similar), respect the types:

- Do not reference class names that don't exist in the module
- If you add a new class in CSS, the type file may need regeneration
- Do not manually edit `.d.ts` files — they are auto-generated

Check for an existing type generation script:

```json
// package.json
{ "scripts": { "css-types": "typed-css-modules src" } }
```

## Selector Scope

Keep selectors simple. CSS Modules already scope everything to the component — deep nesting is unnecessary:

```css
/* CORRECT: flat selectors */
.list { }
.listItem { }
.listItemActive { }

/* WRONG: unnecessary nesting (specificity bloat) */
.list .listItem .listItemActive { }
```

If you need to style children based on parent state, one level of nesting is acceptable:

```css
.container { }
.container:hover .icon { opacity: 1; }
```

Do not nest more than two levels deep.
