---
name: React Component Conventions
description: This skill should be used when the user asks to "write React components", "review React code", "create a component", "fix component structure", "refactor component", or when writing/reviewing React components. Provides guidance on component structure, props patterns, hooks usage, and JSX patterns.
---

# React Component Conventions

## Overview

This skill provides React component conventions focusing on readability, maintainability, and React's functional programming principles. Components are stateless functions that combine to build UIs.

## Core Principles

1. **Components are functions** - They take props and return JSX, nothing more.
2. **Prefer stateless** - Use state only for component-lifetime-dependent values (form inputs, UI state).
3. **Semantic HTML** - Use proper HTML elements, not just divs.
4. **Explicit over implicit** - Be clear about what props are passed and how handlers work.

## Component File Structure

### File Organization

Each component lives in its own directory:

```
components/
├── UserProfile/
│   ├── index.tsx           # Component implementation
│   ├── styles.module.css   # CSS Module styles
│   └── index.stories.tsx   # Storybook stories
└── Button/
    ├── index.tsx
    ├── styles.module.css
    └── index.stories.tsx
```

### Code Order Within File

Arrange code in order of consumer interest (most relevant first):

```tsx
// 1. Imports
import { useState } from 'react';
import styles from './styles.module.css';

// 2. Exported component
// 2a. Props type
type Props = {
  /** User's display name */
  name: string;
};

// 2b. Component implementation
export const UserProfile = ({ name }: Props) => {
  const formattedName = formatName(name);

  return (
    <div className={styles.container}>
      <span>{formattedName}</span>
      <InternalAvatar />
    </div>
  );
};

// 2c. Component utilities
function formatName(name: string): string {
  return name.toUpperCase();
}

// 3. Internal components (not exported)
// 3a. Internal props
type InternalAvatarProps = {
  size?: number;
};

// 3b. Internal component
const InternalAvatar = ({ size = 32 }: InternalAvatarProps) => {
  return <img width={size} height={size} />;
};
```

For detailed structure patterns, see `references/component-structure.md`.

## Props Patterns

### Props Type Definition

- Name the type `Props` for exported components
- Name `{ComponentName}Props` for internal components
- Never export Props types (use `ComponentProps<typeof Component>` instead)

```tsx
// Component file
type Props = {
  name: string;
  age: number;
};

export const User = ({ name, age }: Props) => { ... };

// Consumer file - if props type needed
import type { ComponentProps } from 'react';
import { User } from './User';

type UserProps = ComponentProps<typeof User>;
```

### Destructuring Props

Always destructure props in the parameter list:

```tsx
// Good
export const Profile = ({ name, age }: Props) => { ... };

// Bad
export const Profile = (props: Props) => {
  return <div>{props.name}</div>;
};
```

### No Props Spreading

Never use spread operator to pass props:

```tsx
// Bad - unclear what props are passed
const MyComponent = (props: Props) => (
  <div {...props}>Content</div>
);

// Good - explicit props
const MyComponent = ({ className, id }: Props) => (
  <div className={className} id={id}>Content</div>
);
```

### Reserved Prop Names

Do not use DOM property names for custom purposes:

```tsx
// Bad - style/className have expected meanings
<MyComponent style="fancy" className="big" />

// Good - use semantic prop names
<MyComponent variant="fancy" size="large" />
```

### Boolean Props Naming

Use adjective/participle form:

```tsx
type Props = {
  isVisible: boolean;     // Good
  isLoading: boolean;     // Good
  hasError: boolean;      // Good
  visibility: boolean;    // Bad - noun
};
```

## Event Handlers

### Naming Convention

- Props: `on` prefix → `onClick`, `onSubmit`, `onChange`
- Internal handlers: `handle` prefix → `handleClick`, `handleSubmit`

```tsx
type Props = {
  onClick: () => void;
  onHover?: () => void;
};

export const Button = ({ onClick, onHover }: Props) => {
  // Internal handler wraps prop handler
  const handleClick = () => {
    // Internal logic here
    onClick();
  };

  return <button onClick={handleClick}>Click</button>;
};
```

### Define Handlers as Variables

Never inline handler logic in JSX:

```tsx
// Bad
<button onClick={(e) => {
  setValue(v => v + 1);
  trackClick();
}}>
  Click
</button>

// Good
const handleClick = () => {
  setValue(v => v + 1);
  trackClick();
};

<button onClick={handleClick}>Click</button>
```

## JSX Patterns

### Semantic HTML

Use appropriate HTML elements:

```tsx
// Bad - div soup
<div onClick={handleClick}>
  <div className="icon" />
  <div>Submit</div>
</div>

// Good - semantic elements
<button onClick={handleClick}>
  <span className="icon" />
  Submit
</button>
```

### Clickable Elements

Use native clickable elements:

| Use Case | Element |
|----------|---------|
| Navigation | `<a>` or `<Link>` |
| Form input labels | `<label>` |
| Everything else | `<button>` |

Never add `onClick` to non-interactive elements like `<div>` or `<span>`.

### Conditional Rendering

Use ternary operator, not `&&`:

```tsx
// Bad - can render '0' or 'undefined'
{message && <span>{message}</span>}
{count && <Counter value={count} />}

// Good - explicit about both branches
{message ? <span>{message}</span> : null}
{count > 0 ? <Counter value={count} /> : null}
```

Return `null` for "nothing" (not `undefined` or `<></>`).

### Navigation

Use `<Link>` or `<a>`, not programmatic navigation:

```tsx
// Bad - breaks right-click, ctrl+click
<div onClick={() => navigate('/home')}>Home</div>

// Good - standard link behavior
<Link to="/home">Home</Link>
```

### Decorative Text

Use CSS pseudo-elements for decorative characters:

```tsx
// Instead of hardcoding decorative text
<span>※ Note content</span>

// Use CSS
.note::before {
  content: '※ ';
}
<span className="note">Note content</span>
```

For comprehensive JSX patterns, see `references/jsx-patterns.md`.

## Hooks Patterns

### Dependency Arrays

Always include all referenced values in dependency arrays:

```tsx
// Bad - missing dependency
useEffect(() => {
  console.log(counter);
}, []);  // counter should be in deps

// Good - complete dependencies
useEffect(() => {
  console.log(counter);
}, [counter]);
```

Use `eslint-plugin-react-hooks` with `exhaustive-deps` rule.

### Memoization in Components

Avoid `useCallback`/`useMemo` in components unless needed for `useEffect` dependencies:

```tsx
// Usually unnecessary
const handleClick = useCallback(() => {
  doSomething();
}, []);

// Just use regular function
const handleClick = () => {
  doSomething();
};
```

### Memoization in Custom Hooks

Always memoize custom hook return values:

```tsx
function useTemperature(value: number) {
  const [unit, setUnit] = useState<'C' | 'F'>('C');

  // Memoize computed value
  const temperature = useMemo(() => {
    return unit === 'C' ? value : value * 1.8 + 32;
  }, [unit, value]);

  // Memoize callback
  const toggle = useCallback(() => {
    setUnit(u => u === 'C' ? 'F' : 'C');
  }, []);

  return { temperature, toggle };
}
```

For detailed hooks patterns, see `references/hooks-patterns.md`.

## Function Components

### Prefer Function Components

Always use function components unless lifecycle methods not available in hooks are needed:

```tsx
// Good
export const Counter = ({ initial }: Props) => {
  const [count, setCount] = useState(initial);
  return <button onClick={() => setCount(c => c + 1)}>{count}</button>;
};

// Avoid class components
class Counter extends React.Component { ... }
```

### Component Naming

Component name matches directory name:

```tsx
// File: components/UserProfile/index.tsx
export const UserProfile = () => { ... };

// Import
import { UserProfile } from './UserProfile';
```

## Quick Reference

**File Structure:**
- One component per directory
- `index.tsx`, `styles.module.css`, `index.stories.tsx`

**Props:**
- Type named `Props` (not exported)
- Always destructure
- No spreading

**Event Handlers:**
- Props: `on*` prefix
- Internal: `handle*` prefix
- Define as variables, not inline

**JSX:**
- Semantic HTML elements
- Ternary for conditionals (not `&&`)
- `null` for empty render

**Hooks:**
- Complete dependency arrays
- Memoize custom hook returns
- Avoid memoization in components

## Additional Resources

### Reference Files

For detailed patterns and examples, consult:
- **`references/component-structure.md`** - Complete file structure patterns
- **`references/hooks-patterns.md`** - Hook usage patterns and memoization
- **`references/jsx-patterns.md`** - JSX best practices and accessibility
