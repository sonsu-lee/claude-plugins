---
name: Project Structure
description: This skill should be used when the user asks to "organize project", "structure application", "create feature folder", "add route", "set up project layout", or when structuring React/TypeScript frontend projects. Provides guidance on directory organization, feature-based structure, and file placement.
---

# Project Structure Conventions

## Overview

This skill provides project structure conventions for React/TypeScript frontend applications. Focus is on feature-based organization, clear separation of concerns, and scalable directory layouts.

## Prerequisites

- React with TypeScript
- File-based routing (optional)
- CSS Modules for styling

## Top-Level Structure

```
src/
├── api/              # API clients and request functions
├── components/       # Shared UI components
├── constants/        # Application constants
├── hooks/            # Shared custom hooks
├── layouts/          # Page layout components
├── routes/           # Feature-based pages and routes
├── states/           # Global state management
├── styles/           # Global styles and themes
├── types/            # Shared type definitions
└── utils/            # Utility functions
```

### Directory Purposes

| Directory | Purpose | Example Contents |
|-----------|---------|------------------|
| `api/` | HTTP clients, API calls | `userApi.ts`, `client.ts` |
| `components/` | Reusable UI components | `Button/`, `Modal/`, `Card/` |
| `constants/` | Static values | `routes.ts`, `config.ts` |
| `hooks/` | Shared custom hooks | `useDebounce.ts`, `useLocalStorage.ts` |
| `layouts/` | Page wrapper components | `MainLayout/`, `AuthLayout/` |
| `routes/` | Feature pages | `dashboard/`, `settings/`, `users/` |
| `states/` | Global state (Constate) | `authState.ts`, `themeState.ts` |
| `styles/` | Global CSS, themes | `global.css`, `variables.css` |
| `types/` | Shared TypeScript types | `user.ts`, `api.ts` |
| `utils/` | Helper functions | `format.ts`, `validation.ts` |

## Feature-Based Organization

### Routes Directory Structure

Organize by feature, not by file type:

```
src/routes/
├── dashboard/
│   ├── index.tsx
│   ├── components/
│   │   ├── DashboardCard/
│   │   │   ├── index.tsx
│   │   │   └── styles.module.css
│   │   └── RecentActivity/
│   │       ├── index.tsx
│   │       └── styles.module.css
│   ├── hooks/
│   │   └── useDashboardData.ts
│   └── styles.module.css
├── users/
│   ├── index.tsx           # User list page
│   ├── [userId]/
│   │   ├── index.tsx       # User detail page
│   │   └── edit.tsx        # User edit page
│   ├── components/
│   │   └── UserCard/
│   └── hooks/
│       └── useUsers.ts
└── settings/
    ├── index.tsx
    └── components/
```

### When to Use Feature Directories

**In `routes/` (feature-specific):**
- Components used only within the feature
- Hooks specific to the feature
- Feature-specific types

**In `components/` (shared):**
- Components used across multiple features
- Generic UI primitives (Button, Input, Modal)

**In `hooks/` (shared):**
- Hooks used across multiple features
- Generic utility hooks

## Component Directory Pattern

Every component in its own directory:

```
components/
├── Button/
│   ├── index.tsx           # Component implementation
│   ├── styles.module.css   # Scoped styles
│   └── index.stories.tsx   # Storybook stories (optional)
├── Modal/
│   ├── index.tsx
│   ├── styles.module.css
│   ├── index.stories.tsx
│   └── ModalHeader/        # Sub-component
│       ├── index.tsx
│       └── styles.module.css
└── Card/
    ├── index.tsx
    └── styles.module.css
```

### Why Directory Per Component

1. **Cohesion** - Related files grouped together
2. **Clean imports** - `import { Button } from '@/components/Button'`
3. **Encapsulation** - Sub-components nested within parent
4. **Scalability** - Easy to add tests, utils, types

## Import Aliases

Configure path aliases in `tsconfig.json`:

```json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["src/*"]
    }
  }
}
```

### Import Examples

```tsx
// Absolute imports with alias
import { Button } from '@/components/Button';
import { useAuth } from '@/hooks/useAuth';
import { User } from '@/types/user';
import { formatDate } from '@/utils/format';

// Relative imports for same feature
import { UserCard } from './components/UserCard';
import { useUsers } from './hooks/useUsers';
```

### Import Guidelines

| Import Type | When to Use |
|-------------|-------------|
| `@/...` | Cross-feature imports |
| `./...` | Same feature/directory |
| `../...` | Avoid when possible |

## API Organization

### API Client Structure

```
src/api/
├── client.ts           # HTTP client configuration
├── endpoints.ts        # API endpoint constants
├── types.ts            # API response types
├── users/
│   ├── index.ts        # User API functions
│   └── types.ts        # User-specific types
└── auth/
    ├── index.ts
    └── types.ts
```

### API File Pattern

```tsx
// api/users/index.ts
import { client } from '../client';
import type { User, CreateUserInput } from './types';

export const usersApi = {
  getAll: () => client.get<User[]>('/users'),
  getById: (id: string) => client.get<User>(`/users/${id}`),
  create: (data: CreateUserInput) => client.post<User>('/users', data),
  update: (id: string, data: Partial<User>) => client.patch<User>(`/users/${id}`, data),
  delete: (id: string) => client.delete(`/users/${id}`),
};
```

## State Organization

### Constate Pattern

```
src/states/
├── authState.ts        # Authentication state
├── themeState.ts       # Theme/UI state
└── index.ts            # Re-exports
```

### State File Pattern

```tsx
// states/authState.ts
import { useState, useCallback } from 'react';
import constate from 'constate';

function useAuthState() {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  const login = useCallback(async (credentials: Credentials) => {
    // Login logic
  }, []);

  const logout = useCallback(() => {
    setUser(null);
  }, []);

  return { user, isLoading, login, logout };
}

export const [AuthProvider, useAuth] = constate(useAuthState);
```

## Types Organization

### Shared Types Structure

```
src/types/
├── user.ts             # User domain types
├── api.ts              # API utility types
├── common.ts           # Generic utility types
└── index.ts            # Re-exports
```

### Type File Pattern

```tsx
// types/user.ts
export type User = {
  id: string;
  email: string;
  name: string;
  role: UserRole;
  createdAt: string;
};

export type UserRole = 'admin' | 'user' | 'guest';

export type CreateUserInput = Omit<User, 'id' | 'createdAt'>;
```

## File Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Components | PascalCase directory | `Button/`, `UserCard/` |
| Component files | `index.tsx` | `Button/index.tsx` |
| Styles | `styles.module.css` | `Button/styles.module.css` |
| Hooks | camelCase with `use` | `useDebounce.ts` |
| Utils | camelCase | `formatDate.ts` |
| Types | camelCase | `user.ts` |
| Constants | camelCase | `routes.ts` |
| API | camelCase | `usersApi.ts` |

## Things to Avoid

### Avoid Grouping by Type

```
# Bad - groups by type across features
src/
├── components/
│   ├── DashboardCard.tsx
│   ├── UserCard.tsx
│   └── SettingsForm.tsx
├── hooks/
│   ├── useDashboard.ts
│   ├── useUsers.ts
│   └── useSettings.ts
└── styles/
    ├── dashboard.css
    ├── users.css
    └── settings.css
```

### Avoid Flat Component Directories

```
# Bad - flat files, no grouping
src/components/
├── Button.tsx
├── Button.module.css
├── Button.stories.tsx
├── Card.tsx
├── Card.module.css
└── Card.stories.tsx
```

### Avoid Deep Nesting

```
# Bad - too deep
src/routes/dashboard/components/widgets/charts/line/LineChart/index.tsx
```

## Quick Reference

**Create new feature:**
1. Create `routes/feature-name/` directory
2. Add `index.tsx` for main page
3. Create `components/` for feature-specific components
4. Create `hooks/` for feature-specific hooks

**Create shared component:**
1. Create `components/ComponentName/` directory
2. Add `index.tsx` and `styles.module.css`
3. Optionally add `index.stories.tsx`

**Create new API:**
1. Create `api/resource/` directory
2. Add `index.ts` with API functions
3. Add `types.ts` for resource types

## Additional Resources

### Reference Files

For detailed patterns, consult:
- **`references/app-structure.md`** - Complete application structure examples
- **`references/component-organization.md`** - Component organization patterns
