---
name: TypeScript Conventions
description: This skill should be used when the user asks to "write TypeScript code", "review TypeScript", "check naming conventions", "fix type issues", "refactor types", or when writing/reviewing TypeScript code in React applications. Provides guidance on naming patterns, type system usage, and prohibited patterns.
---

# TypeScript Conventions

## Overview

This skill provides TypeScript coding conventions focusing on readability, consistency, and leveraging the type system effectively. The conventions prioritize **consistency over efficiency** and **declarative over procedural** code.

## Core Principles

1. **Write declaratively** - Code is read more than written. Avoid clever tricks and excessive shorthand.
2. **Consistency over efficiency** - Unified conventions benefit maintainability, especially for new team members.
3. **Maximize tsc benefits** - Use strict compiler options and avoid type assertions.
4. **Be explicit** - Prefer clear, unambiguous expressions.

## Naming Conventions

### Pattern Summary

| Pattern | Usage |
|---------|-------|
| `PascalCase` | Types, React components, classes, constant objects |
| `UPPER_SNAKE_CASE` | Global constants (exported, immutable, application-wide) |
| `camelCase` | Functions, variables, parameters, everything else |
| `snake_case` | Only when required by external APIs |

### Global Constants

A global constant must satisfy ALL conditions:
1. Declared with `const`
2. Immutable (including nested properties)
3. Global scope (exported or on `window`/`globalThis`)

```typescript
// UPPER_SNAKE_CASE - exported immutable constant
export const ANSWER_TO_THE_ULTIMATE_QUESTION = 42;

// camelCase - not exported
const id = '491DF306-A2AD-4AC8-B61F-CD21719CC365';

// camelCase - mutable (array can be modified)
export const calledDateTime: Date[] = [];

// UPPER_SNAKE_CASE - readonly array
export const CALLED_DATE_TIME: readonly Date[] = [];
```

### Acronyms

Treat acronyms as regular words in camelCase/PascalCase:

```typescript
// Good
const userId = '...';
const baseUrl = 'https://example.com';

// Bad
const userID = '...';
const baseURL = 'https://example.com';
```

For detailed naming patterns and special cases, see `references/naming-patterns.md`.

## Prohibited Patterns

The following features should NOT be used:

| Feature | Reason |
|---------|--------|
| `enum` | Complex build output, unexpected behavior |
| `default export` | Inconsistent naming across imports |
| `namespace` | Pre-module system syntax |
| `any` (where `unknown` fits) | Breaks type safety |
| `interface` (prefer `type`) | Use `type` for consistency |
| `/// <reference />` | Rarely needed |
| Non-null assertion (`!`) | Hides potential issues |
| `as` type assertion | Masks type inconsistencies |

### Enum Alternatives

**String literal types** for string-based enums:

```typescript
// Instead of enum
type Status = 'pending' | 'active' | 'completed';
```

**Object hash with `as const`** for numeric or aliased values:

```typescript
const Month = {
  Jan: 1,
  Feb: 2,
  Mar: 3,
} as const;

type Month = (typeof Month)[keyof typeof Month]; // 1 | 2 | 3
```

For complete prohibited patterns and alternatives, see `references/prohibited-patterns.md`.

## Type System Patterns

### Prefer `type` over `interface`

Use `type` alias consistently. Only use `interface` when declaration merging is explicitly required.

```typescript
// Good
type UserProps = {
  name: string;
  age: number;
};

// Avoid unless declaration merging needed
interface UserProps {
  name: string;
  age: number;
}
```

### Use `Pick` over `Omit`

`Omit` creates fragile types that don't track when source types change:

```typescript
type User = {
  name: string;
  age: number;
  imageUrl: string;
};

// Bad - if User adds new fields, they're included silently
type ImageProps = Omit<User, 'name' | 'age'>;

// Good - explicitly states what's included
type ImageProps = Pick<User, 'imageUrl'>;
```

### Use `as const` Liberally

Enables precise type inference:

```typescript
const config = {
  apiUrl: 'https://api.example.com',
  timeout: 5000,
} as const;
// Type: { readonly apiUrl: 'https://api.example.com'; readonly timeout: 5000 }
```

### Import Types Explicitly

Use `import type` for type-only imports:

```typescript
import type { UserProps } from './types';
import { validateUser } from './validators';
```

For comprehensive type system patterns, see `references/type-system-patterns.md`.

## Function Patterns

### Prefer Function Declarations

Use `function` keyword over arrow functions for top-level functions:

```typescript
// Good
function processUser(user: User): ProcessedUser {
  // ...
}

// Acceptable when type signature is predefined
type Handler = (event: Event) => void;
const handleClick: Handler = (event) => { ... };
```

### Use Async/Await

Prefer `async/await` over Promise chains:

```typescript
// Good
async function fetchUser() {
  const response = await fetch('/api/user');
  return response.json();
}

// Avoid
function fetchUser() {
  return fetch('/api/user')
    .then(response => response.json());
}
```

### Separate Key Parameters from Options

```typescript
// Good - id is the key, options are secondary
type Options = {
  name?: string;
  age?: number;
};
function updateUser(id: string, { name = '', age = 42 }: Options = {}) {
  // ...
}

// Avoid - everything lumped together
function updateUser(args: { id: string; name?: string; age?: number }) {
  // ...
}
```

## Array and Object Patterns

### Use Appropriate Array Methods

Prefer declarative methods over loops:
- `map()` - Transform elements
- `filter()` - Select elements
- `find()` - Get first match
- `some()`/`every()` - Boolean checks
- `reduce()` - Aggregate values

### Use Destructuring

```typescript
// Good
const { name, age } = user;

// Avoid
const name = user.name;
const age = user.age;
```

### Immutable Updates

Create new objects instead of mutating:

```typescript
// Good
const { removed, ...rest } = original;
return rest;

// Avoid
delete original.removed;
return original;
```

## Comments

### When to Comment

Add comments for:
- Server-side/external service constraints
- Library-specific workarounds
- Business logic decisions
- Temporary solutions (with TODO/FIXME)

Do NOT comment obvious code behavior.

### Use JSDoc with Markdown

```typescript
/**
 * Adds two numbers.
 *
 * @example
 * ```ts
 * add(1, 2); // 3
 * ```
 */
function add(a: number, b: number): number {
  return a + b;
}
```

## Quick Reference

**Always use:**
- `type` over `interface`
- `Pick` over `Omit`
- `as const` for constant objects
- `import type` for type imports
- Function declarations for top-level functions
- Destructuring for object/array access

**Never use:**
- `enum`
- `default export`
- `namespace`
- `any` (use `unknown`)
- `!` non-null assertion
- Implicit type assertions

## Additional Resources

### Reference Files

For detailed patterns and examples, consult:
- **`references/naming-patterns.md`** - Complete naming conventions with examples
- **`references/type-system-patterns.md`** - Advanced type patterns
- **`references/prohibited-patterns.md`** - Detailed prohibited features and alternatives
