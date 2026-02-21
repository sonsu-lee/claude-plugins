---
name: component-craft
description: UI component design guidance for shared component libraries, focused on component boundaries, composition strategy, prop API design, and UX pattern compliance. Use when creating or reviewing reusable UI-kit components, deciding extend-vs-split, defining controlled/uncontrolled APIs, or validating behavior against standard interaction patterns. Prefer this skill for component architecture decisions; use css-craftsman for rendering/debugging issues and design-system for token architecture/Figma alignment.
---

# Component Craft

## Workflow

When you work on a shared UI component, follow these five steps in order. Do NOT skip steps.

### Step 1: Survey

Read existing component code, find usage sites (grep for imports), understand the component's current role and dependencies. If creating a new component, check if similar ones already exist.

### Step 2: Design Decision

Apply composition.md and api-design.md criteria:

- **Extend or separate?** Extend existing component (add variant) or create new component?
- **Composition pattern?** Which pattern fits best? (children, compound component, render props)
- **Prop API**: Naming conventions, defaults, controlled/uncontrolled support.

### Step 3: UX Verification

Check against ux-patterns.md:

- Does the planned behavior match established UX patterns?
- If the spec/design deviates from standard patterns, flag it and propose the standard alternative with reasoning.

### Step 4: Review

Run through review-guide.md checklist. Flag any concerns before implementation.

### Step 5: Implement

Build according to the design decisions. Follow the guidelines.

---

**KEY RULE: When a spec or design deviates from established UX patterns, do not silently implement it. Always flag the deviation and propose the standard alternative with reasoning. The user decides whether to follow the standard or proceed with the custom approach.**

---

## Guidelines

Apply these rules whenever you create, modify, or review shared UI components. Each rule is summarized below. For detailed guidance, examples, and edge cases, read the corresponding reference file.

### Composition — `references/composition.md`

- Same purpose → extend (variant). Different purpose → separate. Compound components for complex shared UI.

### API Design — `references/api-design.md`

- Consistent prop naming. Controlled/uncontrolled support. Defaults for common cases. No breaking changes without deprecation.

### UX Patterns — `references/ux-patterns.md`

- 10 pattern checklists: Pagination, Modal, Select, Form Validation, Toast, Tabs, Tooltip/Popover, Accordion, Dropdown Menu, Toggle/Switch. Framework references (Radix, React Aria, Headless UI). Known algorithm/pattern names.

### Review Guide — `references/review-guide.md`

- 3+ usage sites for shared. Single responsibility. Prop count under 10. Standard UX patterns respected.

### Implementation Patterns — `references/implementation-patterns.md`

- CSS implementation recipes per component type. Height consistency across inline elements. Width strategy: block (100%), inline (min-width), overlay (max-width). Sizing, layout, and defensive CSS for Button, Input, Textarea, Select, Modal/Dialog, Card, Badge, Toast, Tabs, Tooltip, Accordion, Avatar, Skeleton, Sidebar, Sticky Header, Carousel, OTP Input. Modern CSS patterns: anchor positioning, native styleable select (`appearance: base-select`), CSS-only entry/exit animations (`@starting-style`), `calc-size(auto)`, popover API, scroll-snap carousels with `::scroll-marker`. Defensive CSS patterns for flex/grid overflow, text truncation, scroll isolation, transition safety, `overflow: clip`, sticky positioning fixes, `margin-trim`, and reduced motion.
