# TypeScript Prohibited Patterns

## Overview

The following TypeScript features are prohibited in this codebase. Each has alternatives that provide better type safety, consistency, or maintainability.

## Enum

### Why Prohibited

- Build output is complex and non-standard JavaScript
- Unexpected runtime behavior (reverse mapping for numeric enums)
- Cannot be used with `const` assertions
- Inconsistent with other type system patterns

### Alternatives

**String Literal Types** - For simple string unions:

```typescript
// Instead of:
enum Status {
  Pending = 'pending',
  Active = 'active',
  Completed = 'completed',
}

// Use:
type Status = 'pending' | 'active' | 'completed';
```

**Object Hash with `as const`** - For aliased or numeric values:

```typescript
// Instead of:
enum HttpStatus {
  Ok = 200,
  NotFound = 404,
  InternalError = 500,
}

// Use:
const HttpStatus = {
  Ok: 200,
  NotFound: 404,
  InternalError: 500,
} as const;

type HttpStatusCode = (typeof HttpStatus)[keyof typeof HttpStatus];
// Type: 200 | 404 | 500
```

**ValueOf Utility Pattern:**

```typescript
type ValueOf<T> = T[keyof T];

const Month = {
  Jan: 1,
  Feb: 2,
  Mar: 3,
} as const;

function getMonthName(month: ValueOf<typeof Month>): string {
  // month is 1 | 2 | 3
}
```

## Default Export

### Why Prohibited

- Inconsistent naming across import sites
- Harder to refactor (rename requires changes everywhere)
- Cannot be auto-imported reliably
- Mixed default/named exports are confusing

### Alternatives

**Named Exports:**

```typescript
// Instead of:
export default function UserProfile() { ... }

// Use:
export function UserProfile() { ... }

// Import:
import { UserProfile } from './UserProfile';
```

**Exception: Framework Requirements**

Some frameworks require default exports:

```typescript
// Next.js pages - allowed
export default function HomePage() { ... }

// Storybook - allowed
export default {
  title: 'Components/Button',
  component: Button,
};
```

## Namespace

### Why Prohibited

- Pre-ES modules pattern
- Confuses module resolution
- Not tree-shakeable
- Redundant with ES modules

### Alternative

Use ES modules:

```typescript
// Instead of:
namespace Utils {
  export function format() { ... }
  export function parse() { ... }
}

// Use separate modules:
// utils/format.ts
export function format() { ... }

// utils/parse.ts
export function parse() { ... }

// Or barrel export:
// utils/index.ts
export * from './format';
export * from './parse';
```

## any (when unknown is appropriate)

### Why Prohibited

- Completely disables type checking
- Spreads through the codebase
- Hides bugs that TypeScript would catch

### When to Use unknown Instead

```typescript
// Instead of:
function parseJson(text: string): any {
  return JSON.parse(text);
}

// Use:
function parseJson(text: string): unknown {
  return JSON.parse(text);
}

// Then narrow the type:
const result = parseJson(input);
if (isUser(result)) {
  // result is now User
}
```

### Acceptable any Usage

- Third-party library type definitions that require it
- Temporary migration of JavaScript code (with TODO)
- Complex generic constraints where unknown doesn't work

## Interface (prefer type)

### Why type is Preferred

- Consistent syntax across all type definitions
- Union/intersection types only work with `type`
- `type` can represent primitives, tuples, and mapped types
- Avoids confusion about when to use which

### When interface is Acceptable

**Declaration Merging** (rare):

```typescript
// Augmenting a library's types
declare module 'some-library' {
  interface Options {
    customField: string;
  }
}
```

## Non-Null Assertion (!)

### Why Prohibited

- Asserts something the compiler can't verify
- Hides potential null/undefined bugs
- Often indicates incomplete type narrowing

### Alternatives

**Type Guards:**

```typescript
// Instead of:
const element = document.getElementById('app')!;

// Use:
const element = document.getElementById('app');
if (!element) {
  throw new Error('App element not found');
}
// element is now HTMLElement
```

**Early Return:**

```typescript
// Instead of:
function processUser(user: User | null) {
  console.log(user!.name);
}

// Use:
function processUser(user: User | null) {
  if (!user) return;
  console.log(user.name);
}
```

**Optional Chaining (when appropriate):**

```typescript
// Instead of:
const name = user!.profile!.displayName;

// Use (if null is acceptable):
const name = user?.profile?.displayName ?? 'Anonymous';
```

## Type Assertion (as)

### Why Prohibited

- Overrides TypeScript's type inference
- Can hide actual type mismatches
- Often indicates a design problem

### Alternatives

**Type Guards:**

```typescript
// Instead of:
const response = data as ApiResponse;

// Use:
function isApiResponse(data: unknown): data is ApiResponse {
  return (
    typeof data === 'object' &&
    data !== null &&
    'status' in data &&
    'body' in data
  );
}

if (isApiResponse(data)) {
  // data is ApiResponse
}
```

**Generic Type Parameters:**

```typescript
// Instead of:
const users = JSON.parse(response) as User[];

// Use:
function parseUsers(response: string): User[] {
  const parsed = JSON.parse(response);
  // Validate and return
  return validateUsers(parsed);
}
```

### Acceptable Assertion Usage

**`as const`** - Narrows to literal types:

```typescript
const config = {
  apiUrl: 'https://api.example.com',
} as const;
```

**DOM Type Narrowing** (when type is certain):

```typescript
const input = document.querySelector('input[type="text"]') as HTMLInputElement;
```

## Triple-Slash Directives (/// <reference />)

### Why Prohibited

- Outdated pattern from pre-module TypeScript
- Usually indicates misconfigured tsconfig
- Makes dependencies unclear

### Alternative

Configure `tsconfig.json` properly:

```json
{
  "compilerOptions": {
    "types": ["node", "jest"]
  }
}
```

Or use standard imports:

```typescript
import type { SomeType } from 'some-library';
```

## Function Overloads

### Why Prohibited

- Complex to maintain
- Difficult to type correctly
- Often indicates need for separate functions

### Alternatives

**Union Types:**

```typescript
// Instead of:
function format(value: string): string;
function format(value: number): string;
function format(value: string | number): string {
  return String(value);
}

// Use:
function format(value: string | number): string {
  return String(value);
}
```

**Separate Functions:**

```typescript
// Instead of overloads for very different behaviors:
function formatString(value: string): string { ... }
function formatNumber(value: number): string { ... }
```

**Generic Functions:**

```typescript
// Instead of overloads:
function identity<T>(value: T): T {
  return value;
}
```

## CommonJS / AMD Modules

### Why Prohibited

- ES modules are the standard
- Better tree-shaking
- Consistent with browser JavaScript
- Better tooling support

### Use ES Modules

```typescript
// Instead of:
const fs = require('fs');
module.exports = { ... };

// Use:
import fs from 'fs';
export { ... };
```

## Summary Checklist

When reviewing code, ensure none of these patterns are used:

- [ ] No `enum` declarations
- [ ] No `default export` (except framework requirements)
- [ ] No `namespace` declarations
- [ ] No `any` where `unknown` would work
- [ ] Using `type` instead of `interface` (except for merging)
- [ ] No `!` non-null assertions
- [ ] No `as` type assertions (except `as const`)
- [ ] No `/// <reference />` directives
- [ ] No function overloads
- [ ] No CommonJS/AMD module syntax
