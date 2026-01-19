---
name: create-component
description: Create a new React component with proper structure
arguments:
  - name: name
    description: Component name in PascalCase
    required: true
  - name: path
    description: Path where to create the component
    required: false
  - name: --with-stories
    description: Include Storybook stories file
    required: false
  - name: --with-tests
    description: Include test file scaffold
    required: false
---

# Create Component

Create a new React component following frontend conventions.

## Process

1. **Validate name**: Ensure component name is in PascalCase
2. **Determine location**: Use provided path or infer from component type
3. **Invoke component-scaffolder agent**: Generate files with proper structure
4. **Report created files**: List all generated files with paths

## Default Locations

If no path is provided:
- UI primitives → `src/components/primitives/`
- Feedback components → `src/components/feedback/`
- Layout components → `src/components/layout/`
- Data display → `src/components/data/`
- Otherwise → `src/components/`

## Generated Files

**Always created:**
- `index.tsx` - Main component file
- `styles.module.css` - CSS Module styles

**With `--with-stories`:**
- `index.stories.tsx` - Storybook stories

**With `--with-tests`:**
- `index.test.tsx` - Test file scaffold

## Examples

```
/create-component Button
```
Creates `src/components/Button/` with index.tsx and styles.module.css.

```
/create-component UserCard src/routes/users/components --with-stories
```
Creates UserCard in the users feature with Storybook stories.

```
/create-component Modal --with-stories --with-tests
```
Creates Modal component with stories and test scaffold.

## Component Template

The generated component follows these conventions:
- Named export only
- Props defined inline (not exported)
- Uses `clsx` for class composition
- Uses CSS Modules with camelCase
- No margin on root element
- Proper focus-visible styles
