---
description: Audit a project's design system compliance — finds hardcoded values, token violations, theme gaps, and Figma misalignment
argument-hint: [path] [--figma <figma-url>]
allowed-tools: [Read, Glob, Grep, mcp__plugin_figma_figma__get_variable_defs]
---

# Design System Audit

Run a design system compliance audit on the target project.

## Arguments

The user invoked this command with: $ARGUMENTS

Parse the arguments:
- **First argument** (optional): Target path to audit (directory or file). Defaults to current working directory.
- **--figma \<url\>** (optional): Figma file URL for cross-referencing variables against code tokens.

If no arguments are provided, audit the current working directory without Figma cross-referencing.

## Instructions

Spawn the `design-system-auditor` agent with the parsed arguments. The agent will:

1. Discover existing token/variable files
2. Scan CSS files for hardcoded values
3. Check token hierarchy compliance
4. Verify theme coverage (light/dark)
5. Cross-reference with Figma variables (if URL provided)
6. Generate a structured audit report

Present the agent's audit report to the user as-is. Do NOT attempt to fix anything — this command is for auditing only. If the user wants fixes, they should describe what to fix and let the design-system skill handle the workflow.

## Examples

```
/frontend-craft:design-system-audit
/frontend-craft:design-system-audit src/components
/frontend-craft:design-system-audit src/components/Button --figma https://www.figma.com/file/abc123
/frontend-craft:design-system-audit --figma https://www.figma.com/file/abc123
```
