# Framework Benchmarks (CSS Architecture)

Use these as external benchmarks for layout and styling architecture. The goal is not to copy a framework API, but to extract stable CSS decisions.

## Why these references

These ecosystems are widely adopted and actively evolving:
- Chakra UI
- Mantine
- MUI (Material UI)
- Radix UI
- React Aria Components
- Ark UI
- Base UI

## Extracted Patterns

## 1) Macro layout primitives are separate from component internals

- Mantine's `AppShell` treats app-level regions (header/navbar/aside/main) as first-class layout structure.
- Recommendation: keep shell layout explicit and centralized. Use Grid at shell level.

```css
.appShell {
  display: grid;
  grid-template-columns: 16rem minmax(0, 1fr);
  grid-template-rows: auto minmax(0, 1fr);
}
```

## 2) 1D spacing/alignment defaults to Flex stack abstractions

- Chakra `Stack` is a flex container with direction and gap controls.
- Recommendation: for row/column flow and spacing, default to Flex + `gap`.

```css
.stack {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}
```

## 3) Repeated card/tile regions should use intrinsic Grid

- Chakra `SimpleGrid` and Mantine `SimpleGrid` emphasize repeatable grid tracks.
- Recommendation: use `repeat(auto-fit|auto-fill, minmax())` for resilient card layout.

```css
.cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(18rem, 100%), 1fr));
  gap: 1rem;
}
```

## 4) Treat Flex and Grid as complementary, not mutually exclusive

- MUI Grid documentation explicitly notes its Grid component uses **Flexbox**, and recommends CSS Grid for row spanning needs.
- Recommendation: use Flex for flow, CSS Grid for true 2D placement/alignment.

## 5) State styling should be DOM-driven via attributes

- Radix and React Aria expose interaction states via data attributes.
- Ark UI uses stable part/state hooks with `data-scope`, `data-part`, and `data-state`.
- Base UI exposes state attributes like `[data-checked]` and `[data-unchecked]` and supports state-aware className/style functions.

Recommendation:
- Prefer state attributes over class toggling for interactive states.
- Keep selectors shallow and part-scoped.

```css
.item[data-selected],
.item[data-state='open'],
.SwitchThumb[data-checked] {
  background: var(--surface-selected);
}
```

## 6) Expose layout metrics through CSS variables

- React Aria documents CSS variable contracts (example: trigger width).
- Ark UI exposes component variables for styling/animation and scroll effects.
- Base UI exposes dynamic variables like `--available-height` and `--anchor-width` on popup parts.

Recommendation:
- Propagate measured values through CSS variables instead of hardcoded numbers.

```css
.popup {
  max-height: var(--available-height);
  inline-size: var(--anchor-width);
}
```

## 7) Recent direction (2025-03 to 2026-03)

- Ark UI v5 introduced major performance improvements and frequent incremental updates. Recent releases increased part-level control (e.g., new Drawer structure, extra state attributes, more CSS-variable hooks).
- Base UI progressed from alpha/beta to stable v1.x with strong emphasis on accessibility, popup semantics, state hooks, and rendering/performance refinements.

Recommendation:
- Treat both as signals for "headless + attribute/part hooks + CSS vars" architecture.
- Keep component markup part-based and state-addressable in CSS.

## Framework-Derived Rules for this plugin

- Shell-level layout: Grid first.
- Section-level flow: Flex first.
- Card/list dashboards: intrinsic Grid tracks.
- Component internals: Flex first, then nested Grid only for true 2D requirements.
- State styling: prefer data attributes over deep selectors or JS-driven class churn.
- Dynamic sizing/positioning: consume exposed CSS variables where available.
- Keep DOM semantics aligned with layout boundaries.

## References

- Chakra `Stack`: https://chakra-ui.com/docs/components/stack
- Chakra `SimpleGrid`: https://chakra-ui.com/docs/components/simple-grid
- Mantine `AppShell`: https://mantine.dev/core/app-shell/
- MUI `Grid` docs: https://mui.com/material-ui/react-grid/
- Radix styling guide: https://www.radix-ui.com/primitives/docs/guides/styling
- React Aria styling (`data-*` states): https://react-spectrum.adobe.com/react-aria/styling.html
- Ark UI styling (`data-scope`, `data-part`, `data-state`): https://ark-ui.com/docs/guides/styling
- Ark UI changelog: https://ark-ui.com/docs/overview/changelog
- Base UI styling: https://base-ui.com/react/handbook/styling
- Base UI releases: https://base-ui.com/react/overview/releases
