# Design Review Checklist

Use this checklist when reviewing shared UI component proposals, implementations, or pull requests. Each item includes the check, why it matters, and what to do if it fails.

---

## Necessity

- [ ] **Is this component used or planned for 3+ places?**
  If not, keep it as a local component in the feature that needs it. Premature abstraction into the shared library creates maintenance burden and coupling. Extract to shared only when the third use case appears and the API has stabilized.

- [ ] **Does a similar shared component already exist?**
  Search the component library before creating anything new. If a similar component exists, extend it with a new variant or prop rather than building a parallel component. Two components that do almost the same thing confuse consumers and diverge over time.

---

## Single Responsibility

- [ ] **Does the component do exactly one thing?**
  If it handles rendering AND data fetching, split them. If it manages two unrelated UI concerns (e.g., layout and interactive behavior), split them. A component that does one thing is easier to test, reuse, and replace.

- [ ] **Is there a boolean prop that fundamentally changes behavior?**
  This is the number one sign that two components have been merged into one. If a prop like `multiline` changes the component from an input to a textarea, or `isModal` changes a panel into an overlay — these should be separate components. `<Input>` and `<Textarea>` are right. `<Input type="textarea">` is wrong. Boolean props should toggle minor visual or behavioral variations, not switch the component's identity.

- [ ] **Does the component have more than 3 conditional rendering branches based on a mode/type prop?**
  When a `type` or `variant` prop leads to 4+ fundamentally different render paths, extract each path into its own component. Share logic through a common hook or base component, not through a single monolith with switch statements.

---

## API Quality

- [ ] **Prop count under 10?**
  More than 10 props signals the component is doing too much. Strategies to reduce: split into smaller components, use composition via children or compound components (e.g., `<Select><Select.Option>` instead of `options` array prop), group related props into an object.

- [ ] **Do prop names follow the project's conventions?**
  Check naming against established patterns: `size`, `variant`, `colorScheme`, `disabled`, `className`, `children`. Refer to api-design.md for the full naming convention. Inconsistent naming across the library forces consumers to guess or look up every component.

- [ ] **Are defaults sensible?**
  `<Component />` with zero props should render something reasonable and useful. If a component requires 3 props just to show up, the API is too demanding. Required props should be limited to things the component truly cannot guess (e.g., `label` for accessibility, `onSelect` for callbacks that have no meaningful default).

- [ ] **Is controlled + uncontrolled supported for stateful values?**
  If the component manages a value (open/closed, selected item, input value), support both `value` + `onChange` (controlled) and `defaultValue` (uncontrolled). This lets consumers choose the right mode for their use case. Never force controlled-only — it adds boilerplate for simple cases.

- [ ] **Is ref forwarded to the root DOM element?**
  Use `forwardRef` (or the ref prop in React 19+) to expose the root DOM element. This is required for focus management, measuring, scroll-into-view, and integration with third-party libraries like Floating UI or animation libraries. Missing ref forwarding is a common source of workaround hacks downstream.

---

## UX Pattern Compliance

- [ ] **Does the behavior match standard UX patterns?**
  Check against ux-patterns.md for the relevant component type. Specifically: Does a Dialog have focus trap? Does Pagination truncate with ellipsis? Does a Select support keyboard navigation and type-ahead? Does Form Validation follow the blur-then-change sequence? Standard patterns exist because they have been tested across millions of users. Deviating without reason creates confusion.

- [ ] **If the spec deviates from standard patterns — is the deviation documented and justified?**
  Do not silently implement non-standard behavior. If a design asks for a dropdown that opens on hover, or a modal that does not trap focus, flag it. Document the deviation explicitly in the component's documentation. Propose the standard alternative to the designer/PM with reasoning. If the deviation is intentional after discussion, add a code comment explaining why.

---

## Accessibility

- [ ] **Keyboard navigation works?**
  The component must be fully operable with keyboard only. Tab to reach it, Enter/Space to activate, Arrow keys for internal navigation where applicable, Escape to dismiss. Test by unplugging your mouse (or not touching the trackpad) and using the component end-to-end.

- [ ] **ARIA attributes present?**
  Apply the correct attributes for the component's pattern: `role`, `aria-label` or `aria-labelledby`, `aria-expanded`, `aria-selected`, `aria-controls`, `aria-describedby`, `aria-modal`. Do not invent custom roles. Refer to WAI-ARIA Authoring Practices for the correct pattern.

- [ ] **Focus management correct?**
  Focus moves to the expected element on open (e.g., first focusable element in a dialog), returns to the trigger on close, moves predictably during navigation (e.g., arrow keys in a listbox). Focus should never be lost — after an action, the user should always know where focus is.

---

## Customizability

- [ ] **Can it be styled from outside?**
  At minimum, the root element accepts a `className` prop. For deeper customization, support one or more of: CSS custom property overrides (e.g., `--button-bg`), slot props or render props for internal parts (e.g., `renderIcon`), `data-*` attributes for state-based CSS targeting (e.g., `data-state="open"`). Never rely on consumers overriding internal class names that may change.

- [ ] **Is it independent of business logic?**
  The component must not make API calls, assume specific data shapes, or manage feature-specific state. It receives data via props and reports interactions via callbacks. If the component fetches its own data or knows about a specific backend model, it is a domain component and does not belong in the shared library. Move it to the feature module that owns that domain.

---

## Maintainability

- [ ] **Will changing this component break existing usages?**
  Before modifying a shared component, check its consumers. Search for import statements across the codebase. If the change will break existing usages — renaming a prop, removing a variant, changing default behavior — follow the deprecation pattern from api-design.md: add the new API alongside the old, mark the old as deprecated with a console warning, migrate consumers, then remove the old API.

- [ ] **Is the file under 300 lines?**
  Larger files often indicate the component is doing too much. Split into: the main component file, a hooks file for complex logic, a types file for shared TypeScript types, a utils file for pure helper functions. If the JSX alone exceeds 200 lines, the template is too complex and should be broken into subcomponents.

- [ ] **Are there tests for the public API?**
  At minimum, every shared component needs tests for: renders with default props (no crash), each variant/size renders correctly, each interaction works (click handlers, keyboard events), edge cases (empty content, overflow text, disabled state, loading state). Test behavior, not implementation details — assert on what the user sees and does, not on internal state or class names.

---

## Red Flags

When you encounter these patterns, do not implement them silently. Propose the standard alternative with an explanation.

| Red Flag | Proposed Alternative | Why |
|---|---|---|
| Dropdown that opens on hover instead of click | Click-to-open | Hover is inaccessible on touch devices and triggers accidentally on desktop. |
| Pagination without truncation | Ellipsis truncation (see ux-patterns.md) | Rendering 100 page buttons is unusable. Users need landmarks (first, last, current neighborhood). |
| Modal without focus trap | Add focus trap | Without it, keyboard users Tab behind the modal into invisible content. Screen readers lose context. |
| Custom scrollbar that replaces native behavior | Style the native scrollbar with CSS, or use `scrollbar-width`/`scrollbar-color` | Custom scroll implementations break momentum scrolling, accessibility, and platform conventions. |
| Infinite scroll without "Load more" fallback | Add a manual "Load more" button | Infinite scroll prevents access to footer content and is disorienting for keyboard/screen reader users. |
| Form validation on every keystroke from the start | Validate on blur first, then switch to on-change after the first error | Immediate keystroke validation on untouched fields is hostile — the user sees errors before they finish typing. |
| Drag-and-drop without keyboard alternative | Add keyboard reordering (e.g., select item, then use ArrowUp/ArrowDown + modifier key to move) | Drag-and-drop is mouse/touch only. Keyboard and switch-device users are completely locked out without an alternative. |
