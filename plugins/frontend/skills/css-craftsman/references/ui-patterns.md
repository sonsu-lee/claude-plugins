# UI Pattern Recipes

Use these patterns as the default baseline before writing custom layout logic. Match the UI to the nearest pattern, then apply minimal deltas.

## Layout Level Contract

Apply this contract before picking selectors/properties:

- **Page shell level**: Grid first
- **Region/content flow level**: Flex first (1D), Grid when true 2D alignment is needed
- **Component internals**: Flex first, nested Grid only when row+column constraints both matter

DOM boundary rule:
- Shell container -> region container -> component container
- Do not skip boundaries when layout ownership changes.

## 1) App Shell (Header + Sidebar + Content)

When the page has a persistent global layout, use Grid.

```css
.appShell {
  display: grid;
  grid-template-columns: 16rem minmax(0, 1fr);
  grid-template-rows: auto minmax(0, 1fr);
  min-block-size: 100dvh;
}

.header {
  grid-column: 1 / -1;
  position: sticky;
  inset-block-start: 0;
  z-index: var(--z-sticky);
}

.sidebar {
  overflow: auto;
}

.main {
  min-width: 0;
  overflow: auto;
}
```

Rules:
- Use `minmax(0, 1fr)` for the main content track.
- Keep content panes scrollable locally to avoid body-level scroll conflicts.

## 2) Responsive Card Grid

For card collections, use intrinsic grid tracks instead of breakpoint-based hardcoded columns.

```css
.cardGrid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(18rem, 100%), 1fr));
  gap: 1rem;
}
```

Rules:
- Prefer `auto-fit/auto-fill + minmax()` over `1/2/3-column` media breakpoints.
- Inside each card, use flex for vertical stacking only.

## 3) Media Row (Avatar + Text + Meta/Action)

For one-line row composition, use Flex and force shrink behavior on the text region.

```css
.mediaRow {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.mediaBody {
  flex: 1;
  min-width: 0;
}

.mediaTitle {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
```

Rules:
- `min-width: 0` on the flexible text column is required for truncation to work.
- Reserve fixed-width areas (avatar/action) with `flex: none`.

## 4) Label + Field Form Rows

For forms with aligned labels, use Grid. For simple vertical forms, use Flex column.

```css
.formRow {
  display: grid;
  grid-template-columns: minmax(8rem, 12rem) minmax(0, 1fr);
  gap: 0.75rem 1rem;
  align-items: start;
}
```

Rules:
- Use `minmax(0, 1fr)` on input track to prevent overflow.
- Keep helper/error text inside the field column to preserve alignment.

## 5) Toolbar + Table Shell

Use a stable shell around tables with clear overflow boundaries.

```css
.tableShell {
  display: grid;
  grid-template-rows: auto minmax(0, 1fr);
  gap: 0.75rem;
  min-block-size: 0;
}

.tableViewport {
  overflow: auto;
  min-width: 0;
}
```

Rules:
- Keep filters/actions in a toolbar row.
- Put horizontal scroll on table viewport, not on page root.

## 6) Dialog / Drawer Body Layout

Use Grid for header/body/footer separation.

```css
.dialog {
  display: grid;
  grid-template-rows: auto minmax(0, 1fr) auto;
  max-block-size: min(90dvh, 48rem);
}

.dialogBody {
  overflow: auto;
  min-width: 0;
}
```

Rules:
- Keep header/footer fixed in dialog; only body scrolls.
- Constrain max block size with dynamic viewport units (`dvh`).

## Pattern Selection Heuristics

- **One axis** alignment/spacing -> Flex
- **Two axis** placement/alignment -> Grid
- **Repeated cards or tiles** -> Grid with intrinsic tracks
- **Text + controls in a row** -> Flex + `min-width: 0` on text column
- **Complex shells (header/sidebar/body)** -> Grid

## Validation Checklist

After applying a pattern:
- No horizontal overflow at 320px width.
- Long strings do not blow out tracks.
- Truncation works in flex/grid contexts.
- Keyboard focus order follows DOM order.
- `overflow` ownership is intentional (single scroll owner per area).
