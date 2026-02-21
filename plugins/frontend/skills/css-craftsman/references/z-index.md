# z-index Management

## Project-Wide Scale

Define these z-index tokens in `:root` and use them everywhere. Never use raw z-index numbers.

```css
:root {
  --z-base: 0;        /* Default stacking — in-flow elements */
  --z-dropdown: 100;  /* Dropdowns, tooltips, popovers */
  --z-sticky: 200;    /* Sticky headers, sidebars, floating toolbars */
  --z-overlay: 300;   /* Overlays, backdrops, dimming layers */
  --z-modal: 400;     /* Modals, dialogs, full-screen sheets */
  --z-toast: 500;     /* Toast notifications, snackbars */
  --z-max: 9999;      /* NEVER use — reserved for debugging only */
}
```

## Rules

### Always use the scale

```css
/* Correct */
.dropdown { z-index: var(--z-dropdown); }
.modal { z-index: var(--z-modal); }

/* Wrong — raw numbers */
.dropdown { z-index: 10; }
.modal { z-index: 999; }
```

### `z-index: 9999` is a bug, not a solution

If you need a high z-index to make something appear on top, you have a stacking context problem. Fix the root cause, do not inflate the number.

### z-index requires positioning — with one exception

`z-index` has no effect on `position: static` (the default). The element must be `position: relative`, `absolute`, `fixed`, or `sticky` for z-index to apply.

**Exception: flex and grid items.** Flex and grid items can use `z-index` without any `position` set. Per the CSS Flexbox and Grid specs, `z-index` values other than `auto` create a stacking context on flex/grid items even when `position` is `static`.

```css
/* This does nothing on a normal element */
.broken {
  z-index: var(--z-modal); /* ignored — no position set */
}

/* This works — positioned element */
.working {
  position: relative;
  z-index: var(--z-modal);
}

/* This also works — flex/grid item (no position needed) */
.flex-container { display: flex; }
.flex-child {
  z-index: 1; /* works without position on flex items */
}
```

### Stacking context awareness

These properties create new stacking contexts. z-index within a stacking context is scoped to that context — it cannot escape the parent.

Stacking context creators:
- `position` (non-static) combined with `z-index` (non-auto)
- `transform` (any value other than `none`)
- `opacity` less than `1`
- `will-change` (when specifying a stacking-related property)
- `filter` (any value other than `none`)
- `isolation: isolate`
- `contain: layout` or `contain: paint`

### Use `isolation: isolate` to contain z-index scope

When building a component that uses z-index internally, wrap it with `isolation: isolate` to prevent its internal z-index values from leaking into the rest of the page.

```css
.card {
  isolation: isolate; /* Contains internal z-index stacking */
}

.card__image {
  position: relative;
  z-index: 1;
}

.card__badge {
  position: absolute;
  z-index: 2; /* Only competes within .card, not the whole page */
}
```

### Debugging z-index issues

When z-index "doesn't work," follow this checklist:

1. Is the element positioned (not `static`)? Or is it a flex/grid item?
2. Is an ancestor creating a stacking context that traps the element?
3. Does the competing element share the same stacking context?
4. Is `transform`, `opacity`, or `filter` on an ancestor creating an unexpected stacking context?

Fix the stacking context hierarchy. Do not increase the z-index number.

### Avoid z-index on elements that don't need it

Do not add z-index preemptively. Only add it when an element must stack above or below a sibling. Unnecessary z-index creates stacking contexts that cause problems later.

### Within a scale tier, use offsets sparingly

If two elements both need to be at the dropdown level but one must be above the other, use `calc()`:

```css
.dropdown { z-index: var(--z-dropdown); }
.dropdown-nested { z-index: calc(var(--z-dropdown) + 1); }
```

Keep offsets to +1 or +2. If you need more, reconsider the architecture.
