# Layout Strategy

## Grid vs Flex Decision

Use this decision tree:

1. Laying out items in **one direction** (row OR column) -> **Flexbox**
2. Laying out items in **two dimensions** (rows AND columns) -> **Grid**
3. Content should **dictate its own size** -> **Flexbox**
4. Layout should **dictate content placement** -> **Grid**

When in doubt, start with flex. Promote to grid when you need column alignment across rows or explicit track sizing.

```css
/* Flex: single axis, content-driven */
.toolbar { display: flex; gap: 8px; align-items: center; }

/* Grid: two axes, layout-driven */
.dashboard { display: grid; grid-template-columns: 250px 1fr; grid-template-rows: auto 1fr auto; }
```

## Sizing Priority

Always prefer sizes higher on this list. Move down only when the higher option cannot work.

1. **Content-based** (`auto`, `min-content`, `max-content`, `fit-content`) — let content decide
2. **Ratio-based** (`%`, `fr`, `flex-grow`) — proportional to container
3. **Range-based** (`min-width`/`max-width`, `clamp()`) — bounded flexibility
4. **Fixed** (`px`, `rem` on widths) — last resort, only when exact sizing is required

## Width Patterns

Never set a bare fixed width. Use constrained fluid patterns:

```css
/* CORRECT: fluid with a cap */
.container { width: 100%; max-width: 960px; margin-inline: auto; }

/* CORRECT: grid track with fluid floor */
.grid { grid-template-columns: minmax(min(300px, 100%), 1fr); }

/* WRONG: breaks on small screens */
.container { width: 960px; }
```

## flex-1 Rules

Always pair `flex: 1` with `min-width: 0` to prevent overflow from long content.

```css
/* CORRECT */
.fill { flex: 1; min-width: 0; }

/* With a cap */
.fill-capped { flex: 1; min-width: 0; max-width: 400px; }
```

For vertical flex layouts, use `min-height: 0` instead.

## Gap Over Margin

Use `gap` on the flex/grid container. Do not add margin between sibling children.

```css
/* CORRECT */
.stack { display: flex; flex-direction: column; gap: 16px; }

/* WRONG: fragile, requires :last-child overrides */
.stack > * { margin-bottom: 16px; }
.stack > *:last-child { margin-bottom: 0; }
```

## Responsive Design

### Mobile-first by default

Write base styles for mobile, then layer up with `min-width` queries:

```css
.layout { display: flex; flex-direction: column; }

@media (min-width: 768px) {
  .layout { flex-direction: row; }
}
```

### Container queries for components

For any component that may be reused in different layout contexts, prefer container queries over media queries:

```css
.card-container { container-type: inline-size; }

@container (min-width: 400px) {
  .card { flex-direction: row; }
}
```

### Breakpoints

Never pick arbitrary breakpoint values. Base breakpoints on where the content breaks. Common anchors: 480px, 768px, 1024px, 1280px — but only use the ones the design actually needs.

### Fluid values with clamp()

Use `clamp(min, preferred, max)` for spacing and type that scales smoothly:

```css
.heading { font-size: clamp(1.5rem, 2vw + 1rem, 3rem); }
.section { padding: clamp(1rem, 3vw, 3rem); }
```

### Auto-fit grids over fixed column counts

Never hard-code column counts behind media queries. Use intrinsic responsive grids:

```css
/* CORRECT: responsive without media queries */
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(min(250px, 100%), 1fr));
  gap: 16px;
}

/* WRONG: fragile, verbose */
.grid { grid-template-columns: 1fr; }
@media (min-width: 600px) { .grid { grid-template-columns: repeat(2, 1fr); } }
@media (min-width: 900px) { .grid { grid-template-columns: repeat(3, 1fr); } }
```

Use `auto-fill` when you want empty tracks to hold space. Use `auto-fit` when you want items to stretch into available space.

## Grid Track Sizing Rules

### 1fr vs auto vs percentage

| Approach | With `gap` | Large Content | Best For |
|----------|-----------|---------------|----------|
| `1fr 1fr` | Adjusts | Can overflow cell | Equal-width columns (default pick) |
| `auto auto` | Adjusts | Grows to fit | Content-driven column widths |
| `50% 50%` | Overflows | Overflows | Almost never appropriate with gap |

**Prevent content blowout:**

```css
.grid {
  grid-template-columns: repeat(2, minmax(0, 1fr));
}
```

Without `minmax(0, 1fr)`, long URLs or pre-formatted text can blow out `1fr` columns. The `minmax(0, ...)` allows the column to shrink below its content minimum.

**Mixed sizing:**

```css
.grid { grid-template-columns: auto 1fr; }      /* Sidebar + content */
.grid { grid-template-columns: 2fr 5fr 50px; }  /* Proportional + fixed */
```

**Rule: Never use percentage columns with `gap`.** `50% + 50% + gap = overflow`.

## Full-Bleed & Centering Patterns

### Max-width centering one-liner

```css
.page-wrap {
  margin-inline: max(1.5rem, ((100% - 800px) / 2));
}
```

Replaces the classic `max-width: 800px; margin: 0 auto` plus parent padding. The `max()` function handles small-screen gutters intrinsically. No media queries needed.

### Full-bleed child

```css
html { container-type: inline-size; }

.full-bleed {
  margin-inline: calc(50% - 50cqw);
}
```

Use `100cqw` (container query width) instead of `100vw` — accounts for scrollbar width and avoids horizontal overflow.

### Breakout child (wider than content, narrower than full-bleed)

```css
.breakout {
  justify-self: center;
  width: min(100cqw, 100% + 2 * 4em);
}
```

## Intrinsic Sizing with min() / max() / clamp()

Use `min()` as the default sizing strategy for responsive components:

```css
.card { width: min(100%, 400px); }         /* Card never exceeds 400px or its container */
.section { padding: min(4rem, 8vw); }      /* Padding scales but has a cap */
.content { width: min(60ch, 100%); }       /* Readable line length, shrinks on small screens */
.wrapper { inline-size: min(300px, 100dvw); } /* Preferred width, viewport cap */
```

Pattern: `min(<ideal-size>, <constraint>)`. Eliminates many media queries.

**clamp() for ranges:**

```css
font-size: clamp(1rem, 0.95rem + 0.25vw, 1.125rem);
/* same as: max(1rem, min(0.95rem + 0.25vw, 1.125rem)) */
```

## Sticky Positioning

### Flex/Grid fix

Sticky fails silently in flex/grid when the element stretches to full sibling height (default `align-items: stretch`). Apply `align-self: flex-start` on the **sticky element** to prevent stretching:

```css
.layout-grid {
  display: grid;
  grid-template-columns: 250px 1fr;
}

.sidebar {
  position: sticky;
  top: 0;
  align-self: flex-start;  /* Applied to the child, not the parent */
  max-height: 100dvh;
  overflow-y: auto;
}
```

### Scroll-state detection (emerging)

```css
.sticky-wrapper {
  container-type: scroll-state;
  position: sticky;
  top: 0;
}

@container scroll-state(stuck: top) {
  .header { box-shadow: var(--shadow-md); }
}
```

Detects "stuck" state in CSS — replaces `IntersectionObserver` patterns. Chrome-only currently.
