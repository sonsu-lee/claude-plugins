# UX Patterns: Decision Criteria

## Pagination

### Must-Have Behaviors

- [ ] Truncation with ellipsis for large page counts — never render all page numbers
- [ ] Always show first and last page
- [ ] Show 1-2 neighbor pages around the current page
- [ ] Current page visually highlighted and marked with `aria-current="page"`
- [ ] Previous/Next buttons present and disabled at boundaries (page 1 / last page)

### Known Patterns

**Ellipsis Truncation Algorithm** — Given `currentPage`, `totalPages`, and `siblingCount`, calculates which page numbers to display and where to insert ellipsis placeholders. The output is an array like `[1, '...', 4, 5, 6, '...', 20]`. Core logic: always include page 1 and the last page, always include `siblingCount` pages on each side of the current page, replace gaps of more than one missing page with an ellipsis.

### Framework References

- React Aria usePagination: https://react-spectrum.adobe.com/react-aria/usePagination.html
- MUI Pagination: https://mui.com/material-ui/react-pagination/
- Ellipsis algorithm reference: https://gist.github.com/kottenator/9d936eb3e4e3c3e02598

---

## Modal / Dialog

### Must-Have Behaviors

- [ ] Focus trap — Tab and Shift+Tab cycle within the modal, never escaping to content behind
- [ ] Escape key closes the modal
- [ ] Backdrop/overlay click closes the modal (make this configurable; some confirmation dialogs should not close on backdrop click)
- [ ] Scroll lock on body — background content does not scroll while modal is open
- [ ] Return focus to the trigger element when the modal closes
- [ ] ARIA: `role="dialog"`, `aria-modal="true"`, `aria-labelledby` pointing to the modal title

### Known Patterns

**Focus Trap Pattern** — Intercepts Tab and Shift+Tab keydown events to cycle focus among focusable elements within a container. On Tab from the last focusable element, focus wraps to the first. On Shift+Tab from the first, focus wraps to the last.

**Inert Attribute Pattern** — Applies the `inert` attribute to all content outside the modal, making it non-interactive and hidden from assistive technology. Preferred over manual `aria-hidden` on sibling elements.

**Scroll Lock** — Prevents body scroll while preserving the current scroll position. Technique: set `overflow: hidden` on the body and apply `padding-right` equal to the scrollbar width to prevent layout shift.

### Framework References

- Radix Dialog: https://www.radix-ui.com/primitives/docs/components/dialog
- Headless UI Dialog: https://headlessui.com/react/dialog
- React Aria useDialog: https://react-spectrum.adobe.com/react-aria/useDialog.html

---

## Dropdown / Select

### Must-Have Behaviors

- [ ] Opens on click (not hover) for select-type controls
- [ ] Keyboard navigation: ArrowUp/ArrowDown to move highlight, Enter to select, Escape to close
- [ ] Type-ahead search — typing characters rapidly selects the first matching option
- [ ] Auto-positioning — listbox flips to the opposite side when it would overflow the viewport edge
- [ ] Selected value displayed in the trigger element
- [ ] `aria-expanded` on trigger, `role="listbox"` on options container, `role="option"` on each item, `aria-selected` on the selected item

### Known Patterns

**Listbox Pattern** — A single-select (or multi-select) list with keyboard navigation. Use when the set of options is fixed and does not need filtering. The user picks from a known, visible set.

**Combobox Pattern** — A text input combined with a listbox. The input filters the listbox options as the user types. Use when the option list is long or searchable, or when the user may need to enter a value not in the list.

Decision: use Listbox for short, fixed option sets (e.g., country selector with < 20 items). Use Combobox when options exceed ~15-20 items or when search/filter improves the experience.

### Framework References

- Radix Select: https://www.radix-ui.com/primitives/docs/components/select
- Headless UI Listbox: https://headlessui.com/react/listbox
- React Aria useSelect: https://react-spectrum.adobe.com/react-aria/useSelect.html
- React Aria useComboBox: https://react-spectrum.adobe.com/react-aria/useComboBox.html

---

## Form Validation

### Must-Have Behaviors

- [ ] Do not show errors on untouched fields — a field that has never been focused or changed should show no error state
- [ ] Validate on blur for the first interaction — when the user leaves a field for the first time, validate and show any error
- [ ] Validate on change after the first error is shown — once an error is displayed, re-validate on every keystroke so the user gets immediate feedback when they fix it
- [ ] Error message placed directly below the field, associated via `aria-describedby`
- [ ] Required field indication — use an asterisk or "(required)" label; be consistent across the form
- [ ] Form-level error summary for complex forms — list all errors at the top with links/anchors to each field, focused on submission failure

### Known Patterns

**Touched/Dirty State Pattern** — Track two states per field: `touched` (field has received and lost focus at least once) and `dirty` (field value differs from initial value). Show validation errors only for fields that are `touched`. This prevents overwhelming the user with errors before they have had a chance to fill anything in.

**Optimistic Validation** — After a field enters an error state, switch its validation trigger from `blur` to `change`. This gives the user instant positive feedback as they correct their input, rather than forcing them to leave the field again to see if the error cleared.

### Framework References

- React Hook Form: https://react-hook-form.com/
- Formik: https://formik.org/
- React Aria useTextField: https://react-spectrum.adobe.com/react-aria/useTextField.html

---

## Toast / Notification

### Must-Have Behaviors

- [ ] Auto-dismiss with sensible defaults: ~5 seconds for info/success, NO auto-dismiss for error/warning toasts
- [ ] Stack order configurable: newest on top or newest on bottom
- [ ] Dismiss button always visible on every toast
- [ ] Accessible via `role="status"` for informational toasts and `role="alert"` for errors
- [ ] Pause auto-dismiss timer on hover — resume when the pointer leaves
- [ ] Support action buttons (e.g., "Undo") within the toast body

### Known Patterns

**Live Region Pattern** — Uses ARIA live regions (`role="status"` with `aria-live="polite"`, `role="alert"` with `aria-live="assertive"`) to announce messages to screen readers without moving focus. Info/success messages use polite; errors use assertive. The toast container element must exist in the DOM before the toast is inserted so screen readers can detect the change.

**Promise Toast Pattern** — Shows a loading state while an async operation is in progress, then transitions to success or error based on the result. Avoids the flicker of showing nothing then showing a result. Useful for operations like form submission or file upload.

### Framework References

- Radix Toast: https://www.radix-ui.com/primitives/docs/components/toast
- Sonner: https://sonner.emilkowal.dev/
- React Hot Toast: https://react-hot-toast.com/

---

## Tabs

### Must-Have Behaviors

- [ ] ArrowLeft/ArrowRight navigates between tabs (ArrowUp/ArrowDown for vertical tabs)
- [ ] Tab key moves focus from the tab list into the panel content — it does NOT move to the next tab
- [ ] Selected tab indicated visually and via `aria-selected="true"`
- [ ] No page scroll when switching tabs
- [ ] Tab panel associated to its tab via `aria-labelledby`
- [ ] Tab list has `role="tablist"`, each tab has `role="tab"`, each panel has `role="tabpanel"`

### Known Patterns

**Roving Tabindex** — Only the currently active tab has `tabindex="0"`. All other tabs have `tabindex="-1"`. Arrow keys move focus between tabs and update the tabindex values accordingly. Pressing Tab exits the tab list entirely and moves focus to the tab panel. This gives keyboard users a single Tab stop for the entire tab list rather than forcing them to Tab through every tab.

**Lazy Panel Rendering** — Two strategies: (1) Only mount the active panel's content in the DOM (saves memory, but destroys state on switch). (2) Mount all panels but show/hide with CSS `display: none` (preserves state, but increases initial render cost). Choose based on whether panel state preservation matters — forms or videos benefit from strategy 2; static content is fine with strategy 1.

### Framework References

- Radix Tabs: https://www.radix-ui.com/primitives/docs/components/tabs
- Headless UI Tab: https://headlessui.com/react/tabs
- React Aria useTabList: https://react-spectrum.adobe.com/react-aria/useTabList.html

---

## Tooltip / Popover

### Must-Have Behaviors

- [ ] Show delay: ~200ms for tooltips (prevents flicker on casual mouse movement), configurable
- [ ] Hide delay: ~0-100ms (small grace period prevents flicker when moving between nearby triggers)
- [ ] Hover bridge — a diagonal safe area between the trigger and the floating element that prevents premature closing
- [ ] Dismiss on Escape key
- [ ] Tooltip dismisses on scroll; Popover stays open on scroll (different expectations)
- [ ] Auto-positioning: flip to opposite side when near viewport edge, shift along axis to stay in view
- [ ] Tooltip: triggered by hover and focus, contains only text, `role="tooltip"`. Popover: triggered by click, can contain interactive content, `role="dialog"`.

### Known Patterns

**Hover Bridge / Safe Triangle** — When the user moves their cursor from the trigger element to the floating tooltip/popover, there is a gap. Without a hover bridge, moving through this gap closes the floating element. The safe triangle pattern creates a virtual triangular hit area between the trigger and the floating element. The triangle vertices are the cursor position and the two nearest corners of the floating element. As long as the cursor stays within this triangle, the floating element remains open.

**Floating UI Positioning** — Automatic placement calculation using middleware: `flip` (switches to opposite side if overflowing), `shift` (slides along the axis to stay in viewport), `offset` (adds distance between trigger and floating element), `arrow` (positions the arrow indicator). Use Floating UI or Popper.js rather than writing positioning logic from scratch.

### Framework References

- Radix Tooltip: https://www.radix-ui.com/primitives/docs/components/tooltip
- Radix Popover: https://www.radix-ui.com/primitives/docs/components/popover
- Floating UI: https://floating-ui.com/

---

## Accordion / Disclosure

### Must-Have Behaviors

- [ ] Enter or Space toggles the section open/closed
- [ ] Single-expand or multi-expand mode (configurable) — single-expand closes other sections when one opens
- [ ] Smooth height animation on expand/collapse
- [ ] `aria-expanded` on the trigger button reflects open/closed state
- [ ] `aria-controls` on the trigger points to the panel's `id`
- [ ] Panel has `role="region"` with `aria-labelledby` pointing back to the trigger
- [ ] Trigger is a `<button>` inside a heading element (e.g., `<h3><button aria-expanded="true">...</button></h3>`)

### Known Patterns

**Animate Height Pattern** — Use CSS `grid-template-rows: 0fr` transitioning to `1fr` on a wrapper element, with `overflow: hidden` on the inner content. This achieves smooth expand/collapse animation without JavaScript height measurement. The inner element uses `min-height: 0` in the collapsed state. This approach avoids the pitfalls of animating `height: auto` (which CSS cannot transition natively).

**Disclosure Pattern** — A single expand/collapse unit: one trigger button and one collapsible panel. An Accordion is a group of coordinated Disclosures — the coordination logic (single-expand vs multi-expand) lives at the group level, not within each Disclosure.

### Framework References

- Radix Accordion: https://www.radix-ui.com/primitives/docs/components/accordion
- Headless UI Disclosure: https://headlessui.com/react/disclosure

---

## Dropdown Menu

### Must-Have Behaviors

- [ ] Opens on click (button trigger). Hover-to-open only for navigation menus, never for action menus
- [ ] ArrowUp/ArrowDown moves highlight between items. Enter/Space activates the highlighted item
- [ ] Type-ahead — typing a character focuses the first item starting with that letter
- [ ] Escape closes the menu and returns focus to the trigger
- [ ] Light dismiss — clicking outside the menu closes it
- [ ] Submenus open on ArrowRight, close on ArrowLeft (or reverse for RTL)
- [ ] `role="menu"` on the container, `role="menuitem"` on each item, `aria-haspopup="true"` on the trigger

### Known Patterns

**Menu Button Pattern** — A button that opens a menu of actions. Not a select — the user is performing an action, not choosing a value. The trigger button does not display the selected item; it displays a fixed label (e.g., "Actions", "More", or an icon).

**Nested Menu Pattern** — Submenus require careful hover intent detection. Use a delay (~300ms) or safe triangle (same as tooltip hover bridge) before opening a submenu, to prevent accidental opening while moving the cursor across parent menu items.

### Framework References

- Radix DropdownMenu: https://www.radix-ui.com/primitives/docs/components/dropdown-menu
- Headless UI Menu: https://headlessui.com/react/menu
- React Aria useMenuTrigger: https://react-spectrum.adobe.com/react-aria/useMenuTrigger.html

---

## Toggle / Switch

### Must-Have Behaviors

- [ ] Click or Space toggles the state. Enter should also toggle (not all implementations do this — be explicit)
- [ ] Visual state clearly distinguishable: on vs off must differ in more than just color (position, icon, or label change)
- [ ] `role="switch"` with `aria-checked="true"` / `"false"`
- [ ] Label associated via `aria-labelledby` or wrapping `<label>`
- [ ] Disabled state: `aria-disabled="true"`, visually dimmed, cursor: not-allowed
- [ ] Immediate effect — toggles apply instantly (unlike checkboxes in forms which apply on submit)

### Known Patterns

**Switch vs Checkbox** — Use a Switch when the setting takes effect immediately (e.g., "Enable notifications"). Use a Checkbox when the setting is part of a form that must be submitted. Switches imply instant action; checkboxes imply deferred action.

### Framework References

- Radix Switch: https://www.radix-ui.com/primitives/docs/components/switch
- Headless UI Switch: https://headlessui.com/react/switch
- React Aria useSwitch: https://react-spectrum.adobe.com/react-aria/useSwitch.html
