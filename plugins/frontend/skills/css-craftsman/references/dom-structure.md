# DOM Structure for CSS

## Wrapper Divs Are Acceptable

Add wrapper `<div>` elements freely when layout requires them. Semantic meaning lives in landmarks, headings, and ARIA — not in minimizing div count. A clean layout structure is more important than a flat DOM.

```html
<!-- CORRECT: wrapper for layout, semantics preserved -->
<section>
  <div class="sectionInner">
    <h2>Title</h2>
    <div class="contentGrid">
      <article>...</article>
      <article>...</article>
    </div>
  </div>
</section>
```

## Flatten Unnecessary Nesting

Flex and grid only control **direct children**. Do not add intermediate wrappers that break this relationship unless they serve a layout purpose.

```html
<!-- WRONG: unnecessary wrapper breaks grid item relationship -->
<div class="grid">
  <div class="wrapper">
    <div class="card">...</div>
  </div>
</div>

<!-- CORRECT: card is a direct grid child -->
<div class="grid">
  <div class="card">...</div>
</div>
```

Before adding a wrapper div, ask: "Does this div serve as a layout boundary (flex/grid container, scroll container, positioning context)?" If not, remove it.

## Component Library Handling

When styling third-party or shared component library elements, follow this sequence strictly:

### 1. Check for supported styling props first

Look for these props before doing anything else:

- `className` — merge with your module class
- `style` — inline style object
- `UNSAFE_className` — some libraries (e.g., React Aria, Spectrum) expose this
- `classNames` — some libraries accept a map of classes for sub-elements

```jsx
// CORRECT: use the provided API
<LibraryButton className={styles.customButton} />
```

### 2. Inspect the rendered DOM

Before writing any CSS targeting a library component, open DevTools and inspect the actual rendered HTML. Do not guess at the DOM structure. Library internals change between versions.

### 3. Wrap externally for layout control

Never attempt to override a component's internal layout. Wrap it in your own element and control positioning from outside:

```jsx
// CORRECT: external wrapper for layout
<div className={styles.buttonContainer}>
  <LibraryButton />
</div>

// WRONG: trying to override internal layout
<LibraryButton style={{ display: 'flex', justifyContent: 'center' }} />
```

### 4. Do not target internal DOM elements

Never write selectors that reach into a library component's internal structure. These are undocumented and will break on updates:

```css
/* WRONG: fragile, depends on library internals */
.myWrapper [class*="LibraryButton-inner"] { padding: 8px; }

/* CORRECT: style your own wrapper */
.buttonSlot { padding: 8px; }
```

## Positioning Contexts

When you need `position: absolute` on a child, always set `position: relative` on the intended parent explicitly. Never rely on an ancestor happening to have it:

```css
.parent {
  position: relative; /* explicit context */
}

.badge {
  position: absolute;
  top: -4px;
  right: -4px;
}
```

## Semantic Structure Checklist

Before finalizing DOM structure, verify:

- Use `<nav>`, `<main>`, `<aside>`, `<header>`, `<footer>`, `<section>`, `<article>` where they carry meaning
- `<ul>`/`<ol>` for lists of items (nav links, card grids, menu items)
- `<button>` for actions, `<a>` for navigation — never swap them
- Headings follow hierarchy (`h1` > `h2` > `h3`) without skipping levels
- Do not choose elements for their default styling — choose for semantics, then restyle
