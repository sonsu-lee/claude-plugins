---
name: frontend-review
description: Review frontend code for convention compliance
arguments:
  - name: path
    description: File or directory to review (defaults to current directory)
    required: false
---

# Frontend Convention Review

Review the specified files or directory for frontend convention compliance.

## Process

1. **Identify target**: Use the provided path or default to reviewing recent changes
2. **Invoke code-reviewer agent**: Launch the code-reviewer agent to perform the analysis
3. **Report findings**: Present categorized results with remediation guidance

## Scope

If no path is provided:
- Check git status for modified files
- Review only frontend files (`.tsx`, `.ts`, `.css`, `.module.css`)
- Exclude test files and stories unless explicitly requested

If a path is provided:
- Review all frontend files in that path
- Recursively scan directories

## File Types

Review these file types:
- `*.tsx` - React components (TypeScript/React conventions)
- `*.ts` - TypeScript files (TypeScript conventions)
- `*.css`, `*.module.css` - Stylesheets (CSS conventions)

## Output

Provide a structured report with:
- Summary of files reviewed and issues found
- Critical issues (must fix)
- Recommended fixes (should fix)
- Suggestions (optional improvements)

Each issue includes:
- File path and line number
- Convention violated
- Problem description
- Fix example

## Examples

```
/frontend-review
```
Reviews modified files in current working directory.

```
/frontend-review src/components/Button
```
Reviews all files in the Button component directory.

```
/frontend-review src/routes/users
```
Reviews all frontend files in the users feature.
