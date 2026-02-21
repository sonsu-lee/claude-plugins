# Component Implementation Patterns

CSS implementation recipes for common UI components. Each pattern covers sizing strategy, layout approach, and key defensive CSS rules.

## Button

### Sizing Strategy

Height is fixed per size variant. Width is content-driven with a minimum.

```css
.button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-component-gap);

  /* Fixed height per size — never let content stretch height */
  height: var(--button-height);
  /* Content-driven width with minimum */
  min-width: var(--button-min-width);
  /* Horizontal padding gives breathing room */
  padding-inline: var(--button-padding-x);
  /* Never set explicit width — let content + padding decide */

  border-radius: var(--button-radius);
  font-size: var(--button-font-size);
  font-weight: var(--font-weight-semibold);
  line-height: 1;
  white-space: nowrap;
  cursor: pointer;
  /* Prevent text selection on rapid clicks */
  user-select: none;
}
```

### Size Variants

```css
.button--sm {
  --button-height: 2rem;       /* 32px */
  --button-min-width: 4rem;    /* 64px */
  --button-padding-x: var(--spacing-3);
  --button-font-size: var(--font-size-sm);
  --button-radius: var(--radius-md);
}

.button--md {
  --button-height: 2.5rem;     /* 40px */
  --button-min-width: 5rem;    /* 80px */
  --button-padding-x: var(--spacing-4);
  --button-font-size: var(--font-size-base);
  --button-radius: var(--radius-md);
}

.button--lg {
  --button-height: 3rem;       /* 48px */
  --button-min-width: 6rem;    /* 96px */
  --button-padding-x: var(--spacing-6);
  --button-font-size: var(--font-size-lg);
  --button-radius: var(--radius-lg);
}
```

### Key Rules

- **Never set `height` with `padding-block`** — use fixed `height` + `align-items: center`. Padding-based height is fragile when content changes.
- **Always `min-width`, never `width`** — let icon-only buttons be narrower, text buttons grow naturally.
- **`line-height: 1`** on buttons — prevents line-height from interfering with vertical centering.
- **Full-width variant** uses `width: 100%` on top of the base pattern.
- **Icon-only buttons** set `min-width: unset` and `aspect-ratio: 1` (or equal width/height).

### Modern Enhancements

- **`text-box: trim-both cap alphabetic`** — Trims extra space above/below text caused by font metrics. Achieves true optical vertical centering without magic-number padding. Progressive enhancement — no visual change in unsupported browsers.
- **Toggle button groups** (segmented controls): Style active state with additive visual weight (bigger, bolder, more saturated) rather than recessive (pressed/dimmed). Use `aria-pressed` for toggle state. Target touch devices with `@media (hover: none) and (pointer: coarse)` for distinct active states.

---

## Input / TextField

### Sizing Strategy

Height is fixed per size variant. Width fills its parent container.

```css
.input {
  display: flex;
  align-items: center;

  height: var(--input-height);
  width: 100%;  /* Always fill parent — parent controls width */
  padding-inline: var(--input-padding-x);

  border: var(--border-width-default) solid var(--border-default);
  border-radius: var(--input-radius);
  background: var(--bg-primary);
  color: var(--fg-primary);
  font-size: var(--input-font-size);
  line-height: 1;

  transition: border-color 0.15s, box-shadow 0.15s;
}

.input:focus {
  outline: none;
  border-color: var(--border-focus);
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.15);
}

.input::placeholder {
  color: var(--fg-tertiary);
}

.input:disabled {
  background: var(--interactive-disabled);
  color: var(--fg-disabled);
  cursor: not-allowed;
}
```

### Size Variants

```css
.input--sm {
  --input-height: 2rem;       /* 32px */
  --input-padding-x: var(--spacing-2);
  --input-font-size: var(--font-size-sm);
  --input-radius: var(--radius-md);
}

.input--md {
  --input-height: 2.5rem;     /* 40px */
  --input-padding-x: var(--spacing-3);
  --input-font-size: var(--font-size-base);
  --input-radius: var(--radius-md);
}

.input--lg {
  --input-height: 3rem;       /* 48px */
  --input-padding-x: var(--spacing-4);
  --input-font-size: var(--font-size-lg);
  --input-radius: var(--radius-lg);
}
```

### Key Rules

- **`width: 100%` always** — inputs should never define their own width. The parent (form layout, grid cell) controls width.
- **Match height to Button height** — `input--md` and `button--md` should be the same height. This is critical for inline form layouts (input + button side-by-side).
- **Focus ring with `box-shadow`**, not `outline` — box-shadow respects `border-radius` and is easier to control.
- **Left/right addons** (icons, prefix text) — wrap input in a container with `position: relative`, position addons with `position: absolute`, add `padding-left`/`padding-right` to the input to avoid overlap.

---

## Textarea

### Sizing Strategy

Width fills parent. Height is configurable with a minimum.

```css
.textarea {
  width: 100%;
  min-height: 5rem;     /* 80px — minimum usable area */
  padding: var(--spacing-3);

  border: var(--border-width-default) solid var(--border-default);
  border-radius: var(--input-radius);
  background: var(--bg-primary);
  font-size: var(--font-size-base);
  line-height: var(--leading-normal);
  resize: vertical;     /* Allow vertical resize only */

  /* Same focus ring as input */
  transition: border-color 0.15s, box-shadow 0.15s;
}
```

### Key Rules

- **`resize: vertical`** — horizontal resize breaks layouts. Only allow vertical.
- **`min-height` not `height`** — let the user resize within bounds.
- **Use `padding`** (not `height` + `align-items`) — textarea content is multi-line, needs real padding.
- **Auto-resize pattern**: use JavaScript to set `height = scrollHeight` on input event. Reset `height` to `auto` first to allow shrinking.

---

## Select / Dropdown

### Sizing Strategy

Trigger matches Input sizing. Listbox is a floating layer.

```css
/* Trigger — reuses Input sizing */
.select-trigger {
  display: flex;
  align-items: center;
  justify-content: space-between;

  height: var(--input-height);
  width: 100%;
  padding-inline: var(--input-padding-x);

  border: var(--border-width-default) solid var(--border-default);
  border-radius: var(--input-radius);
  background: var(--bg-primary);
  cursor: pointer;
}

/* Listbox — floating panel */
.select-listbox {
  position: absolute;
  z-index: var(--z-dropdown);
  width: 100%;               /* Match trigger width */
  max-height: 15rem;         /* 240px — show ~6 items */
  overflow-y: auto;

  border: var(--border-width-default) solid var(--border-default);
  border-radius: var(--input-radius);
  background: var(--bg-primary);
  box-shadow: var(--elevation-mid);
}

/* Option item */
.select-option {
  display: flex;
  align-items: center;
  padding: var(--spacing-2) var(--spacing-3);
  min-height: 2.75rem;       /* 44px baseline touch target */
  cursor: pointer;
}

.select-option:hover,
.select-option[data-highlighted] {
  background: var(--bg-secondary);
}

.select-option[data-selected] {
  color: var(--fg-brand);
  font-weight: var(--font-weight-medium);
}
```

### Key Rules

- **Trigger height = Input height** — Select must look identical to Input in forms.
- **Listbox `max-height`** with `overflow-y: auto` — never let the listbox grow beyond viewport.
- **`width: 100%` on listbox** to match trigger width. For content-driven width, use `min-width: 100%` instead.
- **Positioning**: use CSS anchor positioning or a positioning library (Floating UI). Account for viewport edges — flip to top if insufficient space below.

### Native Styleable Select (Progressive Enhancement)

The `appearance: base-select` API enables full styling of native `<select>` without custom dropdown reimplementations.

```css
/* Progressive opt-in */
select {
  appearance: none;
  @supports (appearance: base-select) {
    &,
    &::picker(select) {
      appearance: base-select;
    }
  }
}

/* Custom picker icon with rotation */
select::picker-icon {
  transition: rotate 0.2s ease-out;
}
select:open::picker-icon {
  rotate: 180deg;
}

/* Mobile bottom-sheet positioning */
select::picker(select) {
  @media (width < 400px) {
    bottom: 0;
    width: 100%;
  }
}

/* Staggered option entrance animation */
option {
  transition: opacity 0.2s, scale 0.2s;
  transition-delay: calc(sibling-index() * 50ms);
  scale: 0.9;
  opacity: 0;
}
select:open option {
  scale: 1;
  opacity: 1;
  @starting-style {
    scale: 0.9;
    opacity: 0;
  }
}
```

**Key points:**
- `::picker(select)` targets the dropdown panel. `::picker-icon` targets the chevron.
- `:open` pseudo-class detects expanded state.
- `sibling-index()` enables staggered animations without JS or inline `style="--i: N"`. **Browser support:** Chrome 138+, Safari 26.2+; no Firefox support yet (~70% global coverage). Use with progressive enhancement.
- `@starting-style` defines the entry state for elements transitioning from `display: none`.
- Wrap in `@supports (appearance: base-select)` — feature detection is mandatory.
- `<selectedoption>` element mirrors selected content into the trigger (enables rich content like icons/images).

---

## Modal / Dialog

### Sizing Strategy

Centered overlay. Width is constrained with a maximum. Height adapts to content with a viewport-based cap.

```css
/* Backdrop */
.modal-backdrop {
  position: fixed;
  inset: 0;
  z-index: var(--z-modal-backdrop);
  background: var(--bg-overlay);
}

/* Dialog container — centers the modal */
.modal-container {
  position: fixed;
  inset: 0;
  z-index: var(--z-modal);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: var(--spacing-4);  /* Safe margin from viewport edges */
}

/* Modal panel */
.modal-panel {
  width: 100%;
  max-width: var(--modal-max-width, 32rem);  /* 512px default */
  max-height: calc(100vh - var(--spacing-8));
  overflow: hidden;   /* Children handle their own scroll */

  display: flex;
  flex-direction: column;

  border-radius: var(--radius-xl);
  background: var(--bg-primary);
  box-shadow: var(--elevation-overlay);
}

/* Internal scroll structure */
.modal-header {
  flex-shrink: 0;
  padding: var(--spacing-6);
  border-bottom: var(--border-width-default) solid var(--border-default);
}

.modal-body {
  flex: 1 1 auto;
  overflow-y: auto;
  padding: var(--spacing-6);
  /* Prevent body from growing beyond max-height */
  min-height: 0;
}

.modal-footer {
  flex-shrink: 0;
  padding: var(--spacing-4) var(--spacing-6);
  border-top: var(--border-width-default) solid var(--border-default);
}
```

### Size Variants

```css
.modal--sm  { --modal-max-width: 24rem; }  /* 384px */
.modal--md  { --modal-max-width: 32rem; }  /* 512px */
.modal--lg  { --modal-max-width: 42rem; }  /* 672px */
.modal--xl  { --modal-max-width: 56rem; }  /* 896px */
.modal--full { --modal-max-width: calc(100vw - var(--spacing-8)); }
```

### Key Rules

- **`max-height: calc(100vh - ...)`** on the panel — prevents modal from exceeding viewport on small screens.
- **Header/footer `flex-shrink: 0`**, body `flex: 1 1 auto` + `overflow-y: auto` — only the body scrolls, header and footer stay fixed.
- **`min-height: 0` on modal-body** — required for flex children to actually shrink below their content size.
- **`padding` on the container**, not the panel — ensures the modal never touches viewport edges even on mobile.

### Native Dialog Enhancements

**Sizing with dynamic viewport units:**

```css
dialog {
  block-size: 90dvb;
  inset-block-start: 5dvb;
  inline-size: min(50ch, 90dvi);
  margin-inline: auto;
}
```

- `dvb`/`dvi` (dynamic viewport block/inline) adapt to mobile browser chrome. Prefer them when your browser support matrix allows it, and keep `vh`/`vw` fallback for older engines.
- `min(50ch, 90dvi)` — readable on desktop (character-width cap), full-width on mobile.

**Entry/exit animations (CSS-only):**

```css
dialog {
  --duration: 0.3s;
  transition:
    translate var(--duration) ease-in-out,
    scale var(--duration) ease-in-out,
    display var(--duration) ease-in-out allow-discrete;

  &[open] {
    translate: 0 0;
    scale: 1;
    @starting-style {
      translate: 0 8vh;
      scale: 1.1;
    }
  }

  &:not([open]) {
    translate: 0 -8vh;
    scale: 1.1;
  }
}
```

- `allow-discrete` enables transitioning `display` from `none` to `block`.
- `@starting-style` defines the entry animation start state.
- Entry and exit can be different directions.

**Light dismiss and margin trim:**

- `closedby="any"` on `<dialog>` enables click-outside-to-close natively (no backdrop click detection needed).
- `closedby="none"` for critical confirmation dialogs that must not be accidentally dismissed.
- `margin-trim: block` on dialog content containers eliminates first/last child margin hacks.

**Invoker Commands API (declarative triggers):**

```html
<button command="show-modal" commandfor="my-dialog">Open</button>
<dialog id="my-dialog">...</dialog>
```

---

## Card

### Sizing Strategy

Width fills parent or is controlled by grid/layout. Height is content-driven.

```css
.card {
  display: flex;
  flex-direction: column;

  border-radius: var(--radius-lg);
  background: var(--bg-primary);
  border: var(--border-width-default) solid var(--border-default);
  overflow: hidden;  /* Clips image/header to border-radius */
}

.card-media {
  /* Image/video at top */
  width: 100%;
  aspect-ratio: 16 / 9;   /* Consistent shape regardless of image size */
  object-fit: cover;
}

.card-body {
  flex: 1 1 auto;
  padding: var(--spacing-4);
  display: flex;
  flex-direction: column;
  gap: var(--spacing-2);
}

.card-footer {
  padding: var(--spacing-3) var(--spacing-4);
  border-top: var(--border-width-default) solid var(--border-default);
}
```

### Key Rules

- **Never set card width in the card component** — the parent grid/flex layout controls card width.
- **`overflow: hidden`** on the card — makes the top image respect `border-radius`.
- **`aspect-ratio` on media** — prevents layout shift when images load.
- **`flex: 1 1 auto` on card-body** — pushes footer to the bottom in equal-height card grids.

---

## Badge / Tag

### Sizing Strategy

Inline element. Height from padding + line-height. Width from content.

```css
.badge {
  display: inline-flex;
  align-items: center;
  gap: var(--spacing-1);

  height: 1.5rem;           /* 24px — fixed height */
  padding-inline: var(--spacing-2);
  border-radius: var(--radius-full);

  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-medium);
  line-height: 1;
  white-space: nowrap;
}

/* Dot indicator */
.badge--dot::before {
  content: '';
  width: 0.375rem;          /* 6px */
  height: 0.375rem;
  border-radius: var(--radius-full);
  background: currentColor;
}
```

### Key Rules

- **`white-space: nowrap`** — badges should never wrap to multiple lines.
- **`border-radius: var(--radius-full)`** (pill shape) or `var(--radius-sm)` (rounded rectangle) — pick one and be consistent across the system.
- **Fixed height** like buttons. Use `line-height: 1` + `align-items: center`.
- **Color variants via component tokens** — not conditional classes for each color.

---

## Toast / Notification

### Sizing Strategy

Fixed width floating element. Stacks vertically.

```css
.toast-container {
  position: fixed;
  z-index: var(--z-toast);
  bottom: var(--spacing-4);
  right: var(--spacing-4);

  display: flex;
  flex-direction: column-reverse;  /* New toasts appear at bottom */
  gap: var(--spacing-2);

  /* Prevent toast container from blocking page interaction */
  pointer-events: none;
}

.toast {
  pointer-events: auto;  /* Restore interactivity on individual toasts */
  width: 22rem;           /* 352px — consistent width */

  display: flex;
  align-items: flex-start;
  gap: var(--spacing-3);
  padding: var(--spacing-4);

  border-radius: var(--radius-lg);
  background: var(--bg-primary);
  box-shadow: var(--elevation-high);
}
```

### Key Rules

- **`pointer-events: none` on container**, `auto` on individual toasts — prevents the toast stack from blocking clicks on the page.
- **`flex-direction: column-reverse`** — new toasts appear at the insertion point (bottom), pushing older ones up. This prevents layout shift from the top.
- **Fixed `width`**, not `max-width` — toasts should be a consistent size for visual stability.
- **Auto-dismiss timer** should pause on hover (`mouseenter`/`mouseleave` events).

---

## Tabs

### Sizing Strategy

Tab list is a horizontal row. Each tab is content-width. The panel fills available space.

```css
.tab-list {
  display: flex;
  border-bottom: var(--border-width-default) solid var(--border-default);
  overflow-x: auto;           /* Scroll when too many tabs */
  scrollbar-width: none;      /* Hide scrollbar */
  -webkit-overflow-scrolling: touch;
}

.tab-list::-webkit-scrollbar {
  display: none;
}

.tab {
  flex-shrink: 0;              /* Don't compress tab text */
  padding: var(--spacing-3) var(--spacing-4);
  font-size: var(--font-size-base);
  font-weight: var(--font-weight-medium);
  color: var(--fg-secondary);
  border-bottom: 2px solid transparent;
  white-space: nowrap;
  cursor: pointer;

  transition: color 0.15s, border-color 0.15s;
}

.tab[aria-selected="true"] {
  color: var(--fg-brand);
  border-bottom-color: var(--interactive-primary);
}

.tab-panel {
  padding: var(--spacing-4) 0;
}
```

### Key Rules

- **`overflow-x: auto`** on tab list — allows horizontal scroll when tabs exceed container width. Never wrap tabs to a second line.
- **`flex-shrink: 0`** on each tab — prevents tab text from being compressed.
- **Active indicator with `border-bottom`** (or pseudo-element) — not a separate element.
- **`scrollbar-width: none`** + `-webkit-scrollbar: none` — horizontal scrollbars on tab bars are ugly. Users scroll via touch/mousewheel.

---

## Tooltip / Popover

### Sizing Strategy

Floating element anchored to a trigger. Width adapts to content with a maximum.

```css
/* Modern approach: Popover API + CSS Anchor Positioning */
.tooltip-trigger {
  anchor-name: --tooltip-anchor;
}

.tooltip {
  /* Popover API handles stacking context and top-layer */
  position: absolute;
  position-anchor: --tooltip-anchor;
  position-area: top;       /* Place above trigger */
  margin-bottom: var(--spacing-1);  /* Gap from trigger */

  max-width: 20rem;          /* 320px — keep tooltips concise */
  padding: var(--spacing-2) var(--spacing-3);

  border-radius: var(--radius-md);
  background: var(--bg-inverse);
  color: var(--fg-inverse);
  font-size: var(--font-size-sm);
  line-height: var(--leading-snug);

  /* Subtle entry animation */
  opacity: 0;
  transition: opacity 0.15s, overlay 0.15s allow-discrete, display 0.15s allow-discrete;
}

.tooltip:popover-open {
  opacity: 1;
}

/* Fallback for browsers without anchor positioning */
@supports not (anchor-name: --a) {
  .tooltip-wrapper {
    position: relative;
  }

  .tooltip {
    position: absolute;
    bottom: 100%;
    left: 50%;
    transform: translateX(-50%);
  }
}
```

### Popover vs Tooltip

```css
/* Popover — richer content, click-triggered */
.popover {
  max-width: 24rem;          /* 384px — wider for richer content */
  padding: var(--spacing-4);
  background: var(--bg-primary);
  color: var(--fg-primary);
  border: var(--border-width-default) solid var(--border-default);
  box-shadow: var(--elevation-mid);
}
```

### Key Rules

- **`max-width` on tooltips** — never let tooltips grow wider than ~320px. Short sentences only.
- **Arrow/caret** — use a `::before` pseudo-element with `border` trick or `clip-path` rotated square.
- **Popover API** (`popover` attribute) — handles top-layer stacking, light-dismiss, and focus management natively. Prefer over manual z-index solutions.
- **Flip behavior** — when tooltip would overflow viewport, flip to opposite side. CSS Anchor Positioning handles this with `position-try-fallbacks: flip-block`.
- **Delay on hover** — show tooltip after 200–300ms delay, hide after 100ms. This prevents tooltip flash on quick mouse movements.

### Anchor Positioning Deep Dive

**Arrow/tail with clip-path polygon (replaces border-hack triangles):**

```css
.tooltip::before {
  content: "";
  position: absolute;
  z-index: -1;
  width: var(--arrow-size, 1.2em);
  background: inherit;
  inset: calc(-1 * var(--arrow-gap, 0.5em)) 0;
  clip-path: polygon(
    50% 0.2em,
    100% var(--arrow-gap),
    100% calc(100% - var(--arrow-gap)),
    50% calc(100% - 0.2em),
    0 calc(100% - var(--arrow-gap)),
    0 var(--arrow-gap)
  );
}
```

- Draw arrows on all four sides simultaneously — the tooltip body clips all but the visible one.
- `background: inherit` ensures the arrow always matches the tooltip body color.

**Multi-directional flip fallbacks:**

```css
.tooltip {
  position-area: top;
  justify-self: unsafe anchor-center;
  position-try-fallbacks: flip-block, flip-start, flip-start flip-inline;
}
```

- `flip-block`: top ↔ bottom.
- `flip-start`: mirrors across diagonal (top → left, bottom → right).
- `unsafe anchor-center`: centers on anchor center, not position-area center.

**Sizing relative to anchor:**

```css
.tooltip::before {
  width: anchor-size(width);
  height: anchor-size(height);
}
```

- `anchor-size()` queries anchor dimensions — useful for dropdowns matching trigger width.

### Popover Types

| Type | Light Dismiss | Closes Others | Use Case |
|------|--------------|---------------|----------|
| `popover` (auto) | Yes | Yes | Menus, dropdowns |
| `popover="manual"` | No | No | Toasts, persistent notifications |
| `popover="hint"` | Yes | No | Tooltips (coexists with open menus) |

- `interestfor` attribute enables hover/focus triggering without JavaScript.
- `[popover] { inset: auto; }` — critical reset for anchor positioning (overrides UA `inset: 0`).

---

## Accordion

### Sizing Strategy

Full-width collapsible sections. Height animates between 0 and content height.

```css
.accordion-item {
  border-bottom: var(--border-width-default) solid var(--border-default);
}

.accordion-trigger {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  padding: var(--spacing-4) 0;

  font-size: var(--font-size-base);
  font-weight: var(--font-weight-medium);
  text-align: left;
  cursor: pointer;
}

/* Chevron icon rotation */
.accordion-trigger svg {
  transition: transform 0.2s ease;
  flex-shrink: 0;
}

.accordion-trigger[aria-expanded="true"] svg {
  transform: rotate(180deg);
}

/* Content panel — smooth height animation */
.accordion-panel {
  display: grid;
  grid-template-rows: 0fr;
  transition: grid-template-rows 0.3s ease;
}

.accordion-panel[data-open] {
  grid-template-rows: 1fr;
}

.accordion-panel-inner {
  overflow: hidden;
}
```

### Key Rules

- **`grid-template-rows: 0fr` → `1fr`** for smooth height animation — this is the modern CSS-only approach to animate unknown heights. No JavaScript measurement needed.
- **`overflow: hidden` on inner wrapper** — prevents content from being visible during collapse.
- **`<details>/<summary>` as base** — use native HTML disclosure element for progressive enhancement. Style with `::details-content` pseudo-element where supported.
- **Only one open at a time** — if exclusive mode is needed, use the `name` attribute on `<details>` elements (same `name` = only one open) or manage state in JavaScript.
- **`calc-size(auto, size)`** for transitioning to intrinsic height — the modern replacement for the grid `0fr→1fr` trick. Set `interpolate-size: allow-keywords` globally to enable. Falls back gracefully (no animation in unsupported browsers).
- **`transition-behavior: allow-discrete`** — enables animating `display` property changes. Pair with `@starting-style` for show/hide patterns.

---

## Avatar

### Sizing Strategy

Fixed square with border-radius for circle. Three states: image, initials fallback, icon fallback.

```css
.avatar {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;

  width: var(--avatar-size);
  height: var(--avatar-size);
  border-radius: var(--radius-full);
  overflow: hidden;

  background: var(--bg-tertiary);
  color: var(--fg-secondary);
  font-size: calc(var(--avatar-size) * 0.4);
  font-weight: var(--font-weight-semibold);
  line-height: 1;
  user-select: none;
}

/* Image fills the circle */
.avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* Hide broken image icon when src fails */
.avatar img[src=""],
.avatar img:not([src]) {
  display: none;
}
```

### Size Variants

```css
.avatar--xs  { --avatar-size: 1.5rem; }   /* 24px */
.avatar--sm  { --avatar-size: 2rem; }     /* 32px */
.avatar--md  { --avatar-size: 2.5rem; }   /* 40px */
.avatar--lg  { --avatar-size: 3rem; }     /* 48px */
.avatar--xl  { --avatar-size: 4rem; }     /* 64px */
.avatar--2xl { --avatar-size: 5rem; }     /* 80px */
```

### Avatar Group (Stacked)

```css
.avatar-group {
  display: flex;
  flex-direction: row-reverse;  /* Reverse so first avatar is on top */
}

.avatar-group .avatar {
  margin-left: -0.5rem;        /* Overlap amount */
  border: 2px solid var(--bg-primary);  /* Ring separates avatars */
}

.avatar-group .avatar:last-child {
  margin-left: 0;
}
```

### Key Rules

- **`flex-shrink: 0`** — avatars must never compress in flex layouts.
- **`object-fit: cover`** on the image — prevents distortion regardless of uploaded aspect ratio.
- **Font size relative to avatar size** (`calc(var(--avatar-size) * 0.4)`) — initials scale proportionally.
- **Image error fallback** — use `onError` in JavaScript to hide `<img>` and show initials. CSS-only fallback: use initials as the background/content and layer `<img>` on top.
- **Status indicator** — position a small dot with `position: absolute` at bottom-right of the avatar wrapper.

---

## Skeleton / Loading Placeholder

### Sizing Strategy

Skeleton matches the dimensions of the content it replaces. Shimmer animation indicates loading.

```css
.skeleton {
  background: var(--bg-tertiary);
  border-radius: var(--radius-md);

  /* Shimmer animation */
  background-image: linear-gradient(
    90deg,
    transparent 0%,
    rgba(255, 255, 255, 0.4) 50%,
    transparent 100%
  );
  background-size: 200% 100%;
  animation: skeleton-shimmer 1.5s ease-in-out infinite;
}

@keyframes skeleton-shimmer {
  0%   { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

/* Shape variants */
.skeleton--text {
  height: 1rem;
  width: 100%;
  border-radius: var(--radius-sm);
}

.skeleton--text:nth-child(odd) {
  width: 80%;  /* Vary widths for realistic text appearance */
}

.skeleton--circle {
  width: var(--avatar-size, 2.5rem);
  height: var(--avatar-size, 2.5rem);
  border-radius: var(--radius-full);
}

.skeleton--rect {
  width: 100%;
  aspect-ratio: 16 / 9;
}

/* Synchronized shimmer across all skeletons */
.skeleton {
  background-attachment: fixed;
}
```

### Key Rules

- **Match the final layout** — skeleton should mirror the exact dimensions and positions of the real content. Users should see no layout shift when content loads.
- **`background-attachment: fixed`** — syncs the shimmer gradient across all skeleton elements on the page. Without this, each element shimmers independently (looks chaotic).
- **Respect `prefers-reduced-motion`** — disable animation for users who prefer reduced motion.

```css
@media (prefers-reduced-motion: reduce) {
  .skeleton {
    animation: none;
    /* Static pulse instead */
    opacity: 0.7;
  }
}
```

- **Don't skeleton everything** — only skeleton the content area. Navigation, sidebars, and chrome should be real.

---

## Sidebar Navigation

### Sizing Strategy

Fixed width sidebar. Main content fills remaining space. Collapses on mobile.

```css
.layout {
  display: grid;
  grid-template-columns: var(--sidebar-width, 16rem) 1fr;
  min-height: 100dvh;
}

.sidebar {
  position: sticky;
  top: 0;
  height: 100dvh;
  overflow-y: auto;
  overscroll-behavior: contain;  /* Prevent scroll chaining */

  padding: var(--spacing-4);
  border-right: var(--border-width-default) solid var(--border-default);
  background: var(--bg-secondary);
}

.sidebar-nav-item {
  display: flex;
  align-items: center;
  gap: var(--spacing-3);
  padding: var(--spacing-2) var(--spacing-3);
  min-height: 2.25rem;        /* 36px touch target */
  border-radius: var(--radius-md);

  font-size: var(--font-size-sm);
  color: var(--fg-secondary);
  text-decoration: none;
  transition: background 0.15s, color 0.15s;
}

.sidebar-nav-item:hover {
  background: var(--bg-tertiary);
  color: var(--fg-primary);
}

.sidebar-nav-item[aria-current="page"] {
  background: var(--interactive-secondary);
  color: var(--fg-brand);
  font-weight: var(--font-weight-semibold);
}

/* Collapsed sidebar — icon only */
.layout--collapsed {
  --sidebar-width: 4rem;
}

.layout--collapsed .sidebar-nav-label {
  display: none;
}
```

### Mobile Responsive

```css
@media (max-width: 768px) {
  .layout {
    grid-template-columns: 1fr;
  }

  .sidebar {
    position: fixed;
    inset: 0;
    z-index: var(--z-sidebar);
    width: 18rem;
    transform: translateX(-100%);
    transition: transform 0.3s ease;
  }

  .sidebar[data-open] {
    transform: translateX(0);
  }

  .sidebar-backdrop {
    position: fixed;
    inset: 0;
    z-index: calc(var(--z-sidebar) - 1);
    background: var(--bg-overlay);
  }
}
```

### Key Rules

- **`position: sticky` + `height: 100dvh`** on sidebar — sticks to viewport while main content scrolls. Must also set `align-self: start` if the parent is a grid.
- **`overscroll-behavior: contain`** — prevents sidebar scroll from chaining to the main content.
- **`100dvh` not `100vh`** — `dvh` accounts for mobile browser chrome (address bar, toolbar) that changes dynamically.
- **Mobile: off-canvas with `transform`** — use `transform: translateX(-100%)` instead of `display: none` for smooth animation. Don't forget the backdrop overlay.

---

## Sticky Header

### Sizing Strategy

Full-width fixed header. Content below must account for header height.

```css
.header {
  position: sticky;
  top: 0;
  z-index: var(--z-header);
  height: var(--header-height, 4rem);

  display: flex;
  align-items: center;
  padding-inline: var(--spacing-4);
  gap: var(--spacing-4);

  background: var(--bg-primary);
  border-bottom: var(--border-width-default) solid var(--border-default);
  /* Blur effect for content scrolling behind */
  backdrop-filter: blur(8px);
  background: rgba(255, 255, 255, 0.8);
}

/* Prevent content from hiding behind sticky header */
:target {
  scroll-margin-top: calc(var(--header-height, 4rem) + var(--spacing-4));
}

/* Auto-hide on scroll pattern */
.header--auto-hide {
  transition: transform 0.3s ease;
}

.header--auto-hide[data-hidden] {
  transform: translateY(-100%);
}
```

### Key Rules

- **`backdrop-filter: blur()`** with semi-transparent background — modern glass effect that lets content show through subtly.
- **`scroll-margin-top`** on `:target` — when navigating to anchor links, content won't be hidden behind the sticky header.
- **Announce header height as a CSS variable** (`--header-height`) — other components (modals, sticky sidebars) need this value to position correctly.
- **Auto-hide pattern**: track scroll direction in JavaScript, toggle `data-hidden` attribute. Use `transform: translateY(-100%)` not `display: none` for smooth transition.

---

## Carousel

### Sizing Strategy

Horizontal scroll container with snap points. Native CSS carousel pseudo-elements for indicators and navigation.

```css
.carousel {
  display: flex;
  overflow-x: auto;
  scroll-snap-type: x mandatory;
  scroll-behavior: smooth;
  overscroll-behavior-x: contain;

  /* Native carousel features */
  anchor-name: --carousel;
  scroll-marker-group: after;
}

.carousel-item {
  flex: 0 0 100%;     /* Full-width slides */
  scroll-snap-align: center;
}

/* Scroll indicators (native) */
.carousel::scroll-marker-group {
  display: flex;
  gap: var(--spacing-2);
  justify-self: anchor-center;
  position: fixed;
  position-anchor: --carousel;
  bottom: calc(anchor(bottom) + var(--spacing-3));
}

.carousel-item::scroll-marker {
  content: "";
  width: 0.5rem;
  aspect-ratio: 1;
  border-radius: var(--radius-full);
  background: var(--fg-tertiary);
}

.carousel-item::scroll-marker:target-current {
  background: var(--fg-primary);
}

/* Prev/Next buttons (native) */
.carousel::scroll-button(left),
.carousel::scroll-button(right) {
  position: fixed;
  position-anchor: --carousel;
  align-self: anchor-center;
}
```

### Quantity Query Adaptation

Switch layout based on item count using `:has()`:

```css
.grid {
  display: grid;
  gap: var(--spacing-4);
}

/* 2 items: two columns */
.grid:has(> :nth-child(2)) {
  grid-template-columns: 1fr 1fr;
}

/* 5+ items: become horizontal carousel */
.grid:has(> :nth-child(5)) {
  grid-auto-flow: column;
  grid-auto-columns: 200px;
  overflow-x: auto;
  scroll-snap-type: x mandatory;
}
```

### Key Rules

- **`scroll-snap-type: x mandatory`** ensures items always snap to alignment points.
- **`overscroll-behavior-x: contain`** prevents page scrolling when carousel reaches its end.
- **`::scroll-marker`** and **`::scroll-button()`** are native pseudo-elements replacing JS carousel indicators (Chrome 135+). **Spec status:** CSS Overflow Module Level 5, Working Draft — subject to change.
- **`:target-current`** / **`:target-before`** / **`:target-after`** style active, previous, and next indicators.
- **Quantity queries** with `:has(:nth-child(N))` enable adaptive layouts — a single component can switch between grid and carousel based on item count without JavaScript.
- The `position: fixed` + `position-anchor` on `::scroll-marker-group` shown above is a **positioning technique**, not spec-mandated behavior. The pseudo-element can be styled with any positioning approach.

---

## OTP Input

### Sizing Strategy

Single input element styled to appear as separate digit boxes. Never use multiple `<input>` elements.

```html
<input
  type="text"
  autocomplete="one-time-code"
  inputmode="numeric"
  maxlength="4"
  pattern="\d{4}"
>
```

```css
.otp-input {
  font-family: var(--font-mono, monospace);
  font-size: var(--font-size-2xl);
  letter-spacing: 1.5em;         /* Space between digits */
  text-indent: 0.75em;           /* Center first digit in its box */
  width: calc(4 * 3em);          /* 4 digits × box width */

  /* Visual digit boxes via background */
  background-image: repeating-linear-gradient(
    to right,
    var(--border-default) 0,
    var(--border-default) 2.5em,
    transparent 2.5em,
    transparent 3em
  );
  background-position: bottom;
  background-size: 100% 2px;
  background-repeat: no-repeat;
  border: none;
  outline: none;
}

.otp-input:focus {
  background-image: repeating-linear-gradient(
    to right,
    var(--border-focus) 0,
    var(--border-focus) 2.5em,
    transparent 2.5em,
    transparent 3em
  );
}
```

### Key Rules

- **`type="text"` not `type="number"`** — number inputs have spinners, allow `e`/`E`/`+`/`-`, and strip leading zeros.
- **`autocomplete="one-time-code"`** — triggers WebOTP API and platform-level autofill on mobile.
- **`inputmode="numeric"`** — shows numeric keyboard without `type="number"` downsides.
- **Single input** — multiple inputs break paste handling, confuse arrow key navigation, and fragment screen reader experience.
- Visual multi-box appearance is achieved purely through CSS (letter-spacing + background gradients).

---

## Defensive CSS for Components

> For comprehensive defensive CSS rules (flex overflow, images, heights, scroll containers, sticky positioning, transitions, overflow clip vs hidden, margin-trim), see **css-craftsman** skill's `references/defensive-css.md`. This section covers only component-specific patterns.

### Text Truncation (Single Line)

```css
.truncate {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
```

### Text Truncation (Multi-line)

```css
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
```

### Focus Visible Ring

```css
:focus-visible {
  outline: 2px solid var(--border-focus);
  outline-offset: 2px;
}

:focus:not(:focus-visible) {
  outline: none;
}
```

Use `:focus-visible` instead of `:focus` for all interactive components. Mouse users don't need focus rings; keyboard users do.

### Component-Specific Quick Rules

- **`min-width: 0`** on all flex/grid children that contain text — prevents overflow.
- **`overflow-wrap: break-word`** on user-generated content containers.
- **`overscroll-behavior: contain`** on scroll containers (modals, drawers, listboxes).
- **Never `transition: all`** — be explicit about which properties to transition.
- **`@media (prefers-reduced-motion: reduce)`** — respect in every component with animation.

---

## Shared Sizing Principles

### Height Consistency

All inline interactive elements that appear together must share the same height scale:

| Size | Height | Used by |
|------|--------|---------|
| sm   | 32px (2rem)   | Button, Input, Select trigger, Badge (small variant) |
| md   | 40px (2.5rem) | Button, Input, Select trigger |
| lg   | 48px (3rem)   | Button, Input, Select trigger |

This ensures Button + Input + Select can sit side-by-side in a form row without misalignment.

### Width Strategy by Component Type

| Type | Width strategy | Examples |
|------|---------------|----------|
| Block | `width: 100%` (parent decides) | Input, Textarea, Select, Card |
| Inline | Content-driven + `min-width` | Button, Badge, Tab |
| Overlay | Fixed `width` or `max-width` | Modal, Toast, Dropdown listbox |

### Spacing Consistency

- **Inner component gap** (icon + text inside a button): `var(--space-component-gap)` — typically 8px.
- **Between sibling elements** (label + input, buttons in a group): `var(--space-element-gap)` — typically 16px.
- **Between sections** (form groups, card sections): `var(--space-section-gap)` — typically 32px.

## References

- MDN `appearance`: https://developer.mozilla.org/docs/Web/CSS/appearance
- MDN `::picker()`: https://developer.mozilla.org/docs/Web/CSS/::picker
- MDN `:open`: https://developer.mozilla.org/docs/Web/CSS/:open
- MDN `@starting-style`: https://developer.mozilla.org/docs/Web/CSS/@starting-style
- MDN `transition-behavior`: https://developer.mozilla.org/docs/Web/CSS/transition-behavior
- MDN `interpolate-size`: https://developer.mozilla.org/docs/Web/CSS/interpolate-size
- MDN `<details>` element: https://developer.mozilla.org/docs/Web/HTML/Element/details
- MDN `prefers-reduced-motion`: https://developer.mozilla.org/docs/Web/CSS/@media/prefers-reduced-motion
