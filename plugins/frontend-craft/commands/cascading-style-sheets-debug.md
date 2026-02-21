---
description: Inspect a specific element's DOM structure and computed CSS for debugging
argument-hint: <url> <selector>
allowed-tools: [Read, Glob, Grep, mcp__plugin_playwright_playwright__browser_navigate, mcp__plugin_playwright_playwright__browser_evaluate, mcp__plugin_playwright_playwright__browser_snapshot, mcp__plugin_playwright_playwright__browser_take_screenshot]
---

# Cascading Style Sheets Debug

Inspect a live DOM element and produce a CSS diagnostic report.

## Arguments

The user invoked this command with: $ARGUMENTS

Parse the arguments:
- **First argument**: URL (e.g., `http://localhost:3000/page`)
- **Second argument**: CSS selector (e.g., `.sidebar`, `#main`, `div.card:first-child`)

If only a URL is provided, ask the user for the selector.
If no arguments are provided, ask the user for both URL and selector.

## Instructions

Spawn the `cascading-style-sheets-inspector` agent with the provided URL and selector. The agent will:

1. Navigate to the URL
2. Extract DOM structure, computed styles, box model, parent chain, layout context
3. Auto-detect common issues (overflow clipping, zero-size, off-viewport, hidden elements)
4. Take a screenshot
5. Return a structured diagnostic report

Present the agent's diagnostic report to the user as-is. Do NOT attempt to fix anything — this command is for inspection only. If the user wants fixes, they should describe the problem and let the css-craftsman skill handle the full workflow.

## Examples

```
/frontend-craft:cascading-style-sheets-debug http://localhost:3000 .header__nav
/frontend-craft:cascading-style-sheets-debug http://localhost:6006 [data-testid="card"]
/frontend-craft:cascading-style-sheets-debug http://localhost:3000/settings .sidebar > ul
```
