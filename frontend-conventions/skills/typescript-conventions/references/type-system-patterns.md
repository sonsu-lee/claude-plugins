# TypeScript Type System Patterns

## Type Alias vs Interface

### Prefer `type` Alias

Use `type` consistently for all type definitions:

```typescript
// Recommended
type User = {
  id: string;
  name: string;
  email: string;
};

type Handler = (event: Event) => void;

type Status = 'pending' | 'active' | 'completed';
```

### When to Use `interface`

Only use `interface` when declaration merging is explicitly required:

```typescript
// Library augmentation - interface merging is needed
declare module 'some-library' {
  interface Config {
    customOption: string;
  }
}
```

## Utility Types

### Pick over Omit

`Omit` creates fragile types - use `Pick` for explicit, change-resistant types:

```typescript
type User = {
  id: string;
  name: string;
  email: string;
  avatarUrl: string;
  createdAt: Date;
};

// Bad - fragile, includes any new fields silently
type PublicUser = Omit<User, 'email' | 'createdAt'>;

// Good - explicit, only includes what's needed
type PublicUser = Pick<User, 'id' | 'name' | 'avatarUrl'>;
```

### Extract over Exclude

Same principle applies to union types:

```typescript
type Permission = 'read' | 'write' | 'delete' | 'admin';

// Bad - fragile
type BasicPermission = Exclude<Permission, 'admin'>;

// Good - explicit
type BasicPermission = Extract<Permission, 'read' | 'write' | 'delete'>;
```

### Practical Utility Types

```typescript
// Partial - all properties optional
type PartialUser = Partial<User>;

// Required - all properties required
type RequiredUser = Required<User>;

// Readonly - all properties readonly
type ReadonlyUser = Readonly<User>;

// Record - object with specific key/value types
type UserById = Record<string, User>;

// NonNullable - remove null/undefined
type DefinitelyUser = NonNullable<User | null | undefined>;

// ReturnType - extract function return type
type FetchResult = ReturnType<typeof fetchUser>;

// Parameters - extract function parameter types
type FetchParams = Parameters<typeof fetchUser>;
```

## as const Pattern

### Object Constants

```typescript
const HttpStatus = {
  Ok: 200,
  Created: 201,
  NotFound: 404,
  InternalError: 500,
} as const;

// Type: 200 | 201 | 404 | 500
type StatusCode = (typeof HttpStatus)[keyof typeof HttpStatus];

// Usage
function handleStatus(code: StatusCode) {
  switch (code) {
    case HttpStatus.Ok:
      return 'Success';
    case HttpStatus.NotFound:
      return 'Not Found';
    // TypeScript ensures all cases are handled
  }
}
```

### Array Constants

```typescript
const SUPPORTED_LANGUAGES = ['en', 'ja', 'ko', 'zh'] as const;

// Type: 'en' | 'ja' | 'ko' | 'zh'
type Language = (typeof SUPPORTED_LANGUAGES)[number];

// Usage
function isSupported(lang: string): lang is Language {
  return SUPPORTED_LANGUAGES.includes(lang as Language);
}
```

### Template Literal Types

```typescript
const eventType = 'click' as const;  // Type: 'click'
const message = `Hello, ${name}` as const;  // Type: `Hello, ${string}`
```

## ValueOf Utility

Create a reusable utility for extracting object value types:

```typescript
type ValueOf<T> = T[keyof T];

const ErrorCode = {
  NotFound: 'E001',
  Unauthorized: 'E002',
  Forbidden: 'E003',
} as const;

type ErrorCodeValue = ValueOf<typeof ErrorCode>;  // 'E001' | 'E002' | 'E003'
```

## XOR Type for Exclusive Properties

When properties should be mutually exclusive:

```typescript
// Install: npm install ts-xor
import type { XOR } from 'ts-xor';

type LinkProps = {
  href: string;
  target?: '_blank';
};

type RouterProps = {
  to: string;
};

// Either href OR to, never both
type NavigationProps = XOR<LinkProps, RouterProps>;

// Valid
const link: NavigationProps = { href: '/home' };
const route: NavigationProps = { to: '/dashboard' };

// Invalid - has both
const invalid: NavigationProps = { href: '/home', to: '/dashboard' };
```

## Type Guards

### typeof Guards

```typescript
function processValue(value: string | number) {
  if (typeof value === 'string') {
    return value.toUpperCase();  // TypeScript knows it's string
  }
  return value.toFixed(2);  // TypeScript knows it's number
}
```

### in Guards

```typescript
type Cat = { meow: () => void };
type Dog = { bark: () => void };

function makeSound(pet: Cat | Dog) {
  if ('meow' in pet) {
    pet.meow();
  } else {
    pet.bark();
  }
}
```

### Custom Type Guards

```typescript
type User = { type: 'user'; name: string };
type Admin = { type: 'admin'; name: string; permissions: string[] };

function isAdmin(person: User | Admin): person is Admin {
  return person.type === 'admin';
}

function getPermissions(person: User | Admin): string[] {
  if (isAdmin(person)) {
    return person.permissions;  // TypeScript knows it's Admin
  }
  return [];
}
```

## Exhaustive Switch/Object Pattern

Ensure all union cases are handled:

```typescript
type Status = 'pending' | 'active' | 'completed' | 'cancelled';

// Object pattern - TypeScript error if case missing
const statusMessage: Record<Status, string> = {
  pending: 'Waiting...',
  active: 'In progress',
  completed: 'Done!',
  cancelled: 'Cancelled',
};

// Switch pattern - no default ensures exhaustiveness
function getStatusMessage(status: Status): string {
  switch (status) {
    case 'pending':
      return 'Waiting...';
    case 'active':
      return 'In progress';
    case 'completed':
      return 'Done!';
    case 'cancelled':
      return 'Cancelled';
    // No default - TypeScript errors if case is missing
  }
}
```

## Generic Patterns

### Constrained Generics

```typescript
// Ensure T has an id property
function getById<T extends { id: string }>(items: T[], id: string): T | undefined {
  return items.find(item => item.id === id);
}

// Ensure key exists on object
function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] {
  return obj[key];
}
```

### Default Generic Types

```typescript
type Response<T = unknown> = {
  data: T;
  status: number;
};

// Usage
const generic: Response = { data: 'anything', status: 200 };
const typed: Response<User> = { data: user, status: 200 };
```

## Function Return Types

### When to Specify Return Types

```typescript
// Specify when return type should be specific union
function getColor(): 'red' | 'green' | 'blue' {
  return 'red';  // Without explicit type, would be inferred as string
}

// Specify for public API clarity
export function fetchUser(id: string): Promise<User> {
  return api.get(`/users/${id}`);
}

// Can omit for internal simple functions
function double(n: number) {
  return n * 2;  // Obviously returns number
}
```

## Import Types

### Explicit Type Imports

```typescript
// Type-only imports
import type { User, UserProfile } from './types';
import type { ComponentProps } from 'react';

// Mixed imports
import { validateUser, type ValidationResult } from './validation';
```

### ComponentProps Pattern

Extract component props without exporting Props type:

```typescript
// Component file
type Props = {
  name: string;
  age: number;
};

export const UserCard = ({ name, age }: Props) => { ... };

// Consumer file
import type { ComponentProps } from 'react';
import { UserCard } from './UserCard';

type UserCardProps = ComponentProps<typeof UserCard>;
```

## Strict Null Handling

### Prefer Type Narrowing over Assertions

```typescript
function processUser(user: User | null) {
  // Bad - assertion
  const name = (user as User).name;

  // Bad - non-null assertion
  const name = user!.name;

  // Good - type guard
  if (!user) return;
  const name = user.name;

  // Good - early return
  if (user === null) {
    throw new Error('User is required');
  }
  const name = user.name;
}
```

### Optional Chaining

```typescript
const userName = user?.profile?.displayName ?? 'Anonymous';
```
