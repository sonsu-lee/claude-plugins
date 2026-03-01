# Browser Support Window & Release-Note Gate

## Support window

As of **2026-03-01 (JST)**, this plugin assumes a rolling support window of the last 12 months:
- Start: **2025-03-01**
- End: **2026-03-01**

Operational rule:
- Prefer CSS features that are stable across this window.
- For newer/partial features, require fallback paths via `@supports` and safe defaults.

## Practical targeting rule

Use Browserslist as a guardrail for build/tooling checks:

```bash
npx browserslist "last 1 year and not dead"
```

## Feature tiers

## Tier A — default-on (safe for this plugin)

Use by default unless project-specific constraints say otherwise:
- CSS Grid/Flex + `gap`
- `minmax(0, 1fr)` and `clamp()`
- container queries (`@container`, `container-type`)
- `:has()` for local parent-state styling
- subgrid (where nested track alignment matters)
- `overflow: clip` (prefer over `hidden` when BFC side-effects are not needed)

## Tier B — progressive enhancement required

Use only with fallback path:
- `@scope`
- standard `line-clamp` (keep prefixed fallback path)
- `light-dark()` and advanced color functions when design tokens have non-modern fallbacks
- very new functions/features from current-cycle release notes (`if()`, `shape()`, `sibling-index()`, etc.)

## Release-note checklist (engine by engine)

For any new CSS API proposal in this plugin:

1. Check Chromium release notes in the window.
2. Check Firefox release notes in the window.
3. Check Safari/WebKit release notes in the window.
4. If all three have stable support in-window -> Tier A.
5. Otherwise -> Tier B with documented fallback.

## Examples from the 2025-03 to 2026-03 window

- Chromium
  - Chrome 134 stable rollout (baseline anchor for the window)
  - Chrome 140: CSS `if()` function (new)
  - Chrome 142: style container query range syntax; `if()` in more CSS properties
  - Chrome 143: advanced `anchor()` fallback / anchor-positioning improvements
  - Chrome 144: nested pseudo-elements and additional CSS enhancements

- Firefox
  - Firefox 136: `shape()` function and `hyphenate-limit-chars`
  - Firefox 140+: ongoing CSS additions noted in release docs
  - Firefox 145: additional CSS updates including `text-autospace`

- Safari / WebKit
  - Safari 18.4: `shape()`, `sibling-index()`, and broader CSS feature updates
  - Safari 18.6: follow-up CSS fixes/updates in WebKit feature notes

## Adoption template for new CSS in reviews

When proposing a modern property/function, include:
- Why it simplifies layout or improves maintainability.
- Tier classification (A or B).
- Fallback snippet (required for Tier B).
- Verification note using text diagnostics (`css-inspector`) after applying.

## Headless UI Ecosystem Checks

In addition to browser engines, track major headless UI library release notes when they affect CSS hooks:
- Ark UI changelog (parts/states/variables, composition changes)
- Base UI releases (state attributes, popup variables, accessibility semantics)

Adoption rule:
- If a library introduces a new stable styling hook (`data-*`, part slot, CSS variable), prefer that hook over custom wrapper classes.
- If a library changes part structure, update selectors to part/state hooks and re-run text diagnostics.

## References

- Chrome 134: https://developer.chrome.com/blog/chrome-134/
- New in Chrome 140: https://developer.chrome.com/blog/new-in-chrome-140/
- New in Chrome 142: https://developer.chrome.com/blog/new-in-chrome-142/
- New in Chrome 143: https://developer.chrome.com/blog/new-in-chrome-143/
- New in Chrome 144: https://developer.chrome.com/blog/new-in-chrome-144/
- Firefox 136 for developers: https://developer.mozilla.org/en-US/docs/Mozilla/Firefox/Releases/136
- Firefox 140 for developers: https://developer.mozilla.org/en-US/docs/Mozilla/Firefox/Releases/140
- Firefox 145 for developers: https://developer.mozilla.org/en-US/docs/Mozilla/Firefox/Releases/145
- Safari 18.4 (WebKit features): https://webkit.org/blog/16574/webkit-features-in-safari-18-4/
- Safari 18.6 (WebKit features): https://webkit.org/blog/17330/webkit-features-in-safari-18-6/
- Baseline Explorer (subgrid): https://web-platform-dx.github.io/web-features-explorer/features/subgrid/
- Baseline Explorer (`:has()`): https://web-platform-dx.github.io/web-features-explorer/features/has/
- MDN `line-clamp`: https://developer.mozilla.org/docs/Web/CSS/line-clamp
- MDN `@scope`: https://developer.mozilla.org/docs/Web/CSS/@scope
- Ark UI changelog: https://ark-ui.com/docs/overview/changelog
- Base UI releases: https://base-ui.com/react/overview/releases
