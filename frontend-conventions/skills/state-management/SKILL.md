---
name: State Management
description: This skill should be used when the user asks to "manage state", "create context", "add provider", "use Constate", "share state", or when implementing state management in React applications. Provides guidance on Constate patterns, React Context, and state organization.
---

# State Management Patterns

## Overview

This skill provides state management conventions for React applications using Constate and React Context. Focus is on minimal boilerplate, proper separation, and scalable patterns.

## Prerequisites

- Constate for state management
- React Context for provider patterns
- TypeScript for type safety

## Constate Pattern

### Basic Constate Usage

```tsx
// states/counterState.ts
import { useState, useCallback } from 'react';
import constate from 'constate';

function useCounterState(initialValue = 0) {
  const [count, setCount] = useState(initialValue);

  const increment = useCallback(() => {
    setCount(prev => prev + 1);
  }, []);

  const decrement = useCallback(() => {
    setCount(prev => prev - 1);
  }, []);

  const reset = useCallback(() => {
    setCount(initialValue);
  }, [initialValue]);

  return { count, increment, decrement, reset };
}

export const [CounterProvider, useCounter] = constate(useCounterState);
```

### Using Constate State

```tsx
// App.tsx
import { CounterProvider } from '@/states/counterState';

export const App = () => (
  <CounterProvider>
    <Counter />
  </CounterProvider>
);

// components/Counter.tsx
import { useCounter } from '@/states/counterState';

export const Counter = () => {
  const { count, increment, decrement } = useCounter();

  return (
    <div>
      <span>{count}</span>
      <button onClick={decrement}>-</button>
      <button onClick={increment}>+</button>
    </div>
  );
};
```

## State Splitting

### Split for Performance

Split state to prevent unnecessary re-renders:

```tsx
// states/authState.ts
import { useState, useCallback, useEffect } from 'react';
import constate from 'constate';
import { authApi } from '@/api/auth';
import type { User } from '@/types/user';

function useAuthState() {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  const login = useCallback(async (email: string, password: string) => {
    const result = await authApi.login({ email, password });
    setUser(result.user);
    localStorage.setItem('token', result.token);
  }, []);

  const logout = useCallback(() => {
    setUser(null);
    localStorage.removeItem('token');
  }, []);

  const checkAuth = useCallback(async () => {
    try {
      const user = await authApi.me();
      setUser(user);
    } catch {
      setUser(null);
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    checkAuth();
  }, [checkAuth]);

  return { user, isLoading, login, logout };
}

// Split into separate hooks for granular subscriptions
export const [
  AuthProvider,
  useUser,      // Components needing just user
  useIsLoading, // Components needing just loading state
  useAuth,      // Components needing full auth (login/logout)
] = constate(
  useAuthState,
  (value) => value.user,
  (value) => value.isLoading,
  (value) => ({ login: value.login, logout: value.logout }),
);
```

### Using Split State

```tsx
// Only re-renders when user changes
const UserAvatar = () => {
  const user = useUser();
  return <img src={user?.avatarUrl} alt="" />;
};

// Only re-renders when loading changes
const LoadingIndicator = () => {
  const isLoading = useIsLoading();
  return isLoading ? <Spinner /> : null;
};

// Full auth access for login/logout
const AuthButtons = () => {
  const { login, logout } = useAuth();
  const user = useUser();

  return user
    ? <button onClick={logout}>Logout</button>
    : <button onClick={() => login(email, password)}>Login</button>;
};
```

## State Organization

### Directory Structure

```
src/states/
├── authState.ts       # Authentication state
├── themeState.ts      # Theme/UI preferences
├── cartState.ts       # Shopping cart
├── modalState.ts      # Modal management
└── index.ts           # Re-exports
```

### State File Template

```tsx
// states/themeState.ts
import { useState, useCallback, useMemo } from 'react';
import constate from 'constate';

type Theme = 'light' | 'dark' | 'system';

function useThemeState() {
  const [theme, setTheme] = useState<Theme>(() => {
    return (localStorage.getItem('theme') as Theme) || 'system';
  });

  const toggleTheme = useCallback(() => {
    setTheme(prev => {
      const next = prev === 'light' ? 'dark' : 'light';
      localStorage.setItem('theme', next);
      return next;
    });
  }, []);

  const setThemeMode = useCallback((mode: Theme) => {
    localStorage.setItem('theme', mode);
    setTheme(mode);
  }, []);

  const resolvedTheme = useMemo(() => {
    if (theme === 'system') {
      return window.matchMedia('(prefers-color-scheme: dark)').matches
        ? 'dark'
        : 'light';
    }
    return theme;
  }, [theme]);

  return { theme, resolvedTheme, toggleTheme, setThemeMode };
}

export const [ThemeProvider, useTheme] = constate(useThemeState);
```

## Provider Setup

### Provider Hierarchy

```tsx
// App.tsx
import { AuthProvider } from '@/states/authState';
import { ThemeProvider } from '@/states/themeState';
import { ModalProvider } from '@/states/modalState';
import { Router } from './routes';

export const App = () => (
  <AuthProvider>
    <ThemeProvider>
      <ModalProvider>
        <Router />
      </ModalProvider>
    </ThemeProvider>
  </AuthProvider>
);
```

### Provider with Initial Values

```tsx
// Constate supports initial values via hook parameters
export const [CounterProvider, useCounter] = constate(useCounterState);

// Usage with initial value
<CounterProvider initialValue={10}>
  <Counter />
</CounterProvider>

// Hook receives the value
function useCounterState(initialValue = 0) {
  const [count, setCount] = useState(initialValue);
  // ...
}
```

## React Context (Without Constate)

### When to Use Raw Context

- Simple boolean/primitive state
- No complex logic needed
- Third-party library integration

### Context Pattern

```tsx
// contexts/SidebarContext.tsx
import { createContext, useContext, useState, useCallback, useMemo } from 'react';

type SidebarContextValue = {
  isOpen: boolean;
  toggle: () => void;
  open: () => void;
  close: () => void;
};

const SidebarContext = createContext<SidebarContextValue | null>(null);

export const SidebarProvider = ({ children }: { children: React.ReactNode }) => {
  const [isOpen, setIsOpen] = useState(false);

  const toggle = useCallback(() => setIsOpen(prev => !prev), []);
  const open = useCallback(() => setIsOpen(true), []);
  const close = useCallback(() => setIsOpen(false), []);

  const value = useMemo(
    () => ({ isOpen, toggle, open, close }),
    [isOpen, toggle, open, close]
  );

  return (
    <SidebarContext.Provider value={value}>
      {children}
    </SidebarContext.Provider>
  );
};

export const useSidebar = (): SidebarContextValue => {
  const context = useContext(SidebarContext);
  if (!context) {
    throw new Error('useSidebar must be used within SidebarProvider');
  }
  return context;
};
```

## Memoization Rules

### Always Memoize in State Hooks

```tsx
function useStateHook() {
  const [value, setValue] = useState(initialValue);

  // Always useCallback for functions
  const updateValue = useCallback((newValue: Value) => {
    setValue(newValue);
  }, []);

  // Always useMemo for computed values
  const derivedValue = useMemo(() => {
    return computeExpensiveValue(value);
  }, [value]);

  // Always useMemo for object returns
  return useMemo(
    () => ({ value, derivedValue, updateValue }),
    [value, derivedValue, updateValue]
  );
}
```

### Why Memoization Matters

Without memoization:

```tsx
// Bad - new object on every render
function useBadState() {
  const [items, setItems] = useState([]);

  // New function every render
  const addItem = (item) => setItems([...items, item]);

  // New object every render
  return { items, addItem };
}

// Consumer re-renders unnecessarily
const Component = () => {
  const { items, addItem } = useBadState();

  useEffect(() => {
    // Runs every render because addItem changes!
    console.log('Items changed');
  }, [addItem]);
};
```

With memoization:

```tsx
// Good - stable references
function useGoodState() {
  const [items, setItems] = useState([]);

  // Stable function reference
  const addItem = useCallback((item) => {
    setItems(prev => [...prev, item]);
  }, []);

  // Stable object reference
  return useMemo(
    () => ({ items, addItem }),
    [items, addItem]
  );
}
```

## Common Patterns

### Modal State

```tsx
// states/modalState.ts
import { useState, useCallback } from 'react';
import constate from 'constate';

type ModalType = 'confirm' | 'alert' | 'custom';

type ModalState = {
  type: ModalType | null;
  props: Record<string, unknown>;
  isOpen: boolean;
};

function useModalState() {
  const [modal, setModal] = useState<ModalState>({
    type: null,
    props: {},
    isOpen: false,
  });

  const openModal = useCallback((type: ModalType, props = {}) => {
    setModal({ type, props, isOpen: true });
  }, []);

  const closeModal = useCallback(() => {
    setModal(prev => ({ ...prev, isOpen: false }));
  }, []);

  return { modal, openModal, closeModal };
}

export const [ModalProvider, useModal] = constate(useModalState);
```

### Toast/Notification State

```tsx
// states/toastState.ts
import { useState, useCallback } from 'react';
import constate from 'constate';

type Toast = {
  id: string;
  message: string;
  type: 'success' | 'error' | 'info';
};

function useToastState() {
  const [toasts, setToasts] = useState<Toast[]>([]);

  const addToast = useCallback((message: string, type: Toast['type'] = 'info') => {
    const id = crypto.randomUUID();
    setToasts(prev => [...prev, { id, message, type }]);

    // Auto-remove after 3 seconds
    setTimeout(() => {
      setToasts(prev => prev.filter(t => t.id !== id));
    }, 3000);
  }, []);

  const removeToast = useCallback((id: string) => {
    setToasts(prev => prev.filter(t => t.id !== id));
  }, []);

  return { toasts, addToast, removeToast };
}

export const [ToastProvider, useToasts] = constate(useToastState);
```

### Form State (Local)

For form state, prefer local state over global:

```tsx
// Local form state - better for isolation
const useForm = <T extends Record<string, unknown>>(initialValues: T) => {
  const [values, setValues] = useState(initialValues);
  const [errors, setErrors] = useState<Partial<Record<keyof T, string>>>({});

  const handleChange = useCallback((field: keyof T, value: unknown) => {
    setValues(prev => ({ ...prev, [field]: value }));
    setErrors(prev => ({ ...prev, [field]: undefined }));
  }, []);

  const reset = useCallback(() => {
    setValues(initialValues);
    setErrors({});
  }, [initialValues]);

  return { values, errors, setErrors, handleChange, reset };
};
```

## State Colocation

### Keep State Close to Usage

```
# Good - state colocated with feature
routes/settings/
├── components/
├── hooks/
│   └── useSettingsForm.ts  # Feature-specific state
└── index.tsx

# Global state only in states/
states/
├── authState.ts            # App-wide authentication
└── themeState.ts           # App-wide theme
```

### When to Use Global State

| Use Global State | Use Local State |
|------------------|-----------------|
| Authentication | Form inputs |
| Theme/preferences | UI toggle states |
| Shopping cart | Component animations |
| Notifications | Modal open/close |
| Multi-page data | Single component data |

## Things to Avoid

### Anti-Patterns

```tsx
// Bad - mutating state directly
const [user, setUser] = useState(initialUser);
user.name = 'New Name';  // Mutation!
setUser(user);

// Good - create new object
setUser(prev => ({ ...prev, name: 'New Name' }));

// Bad - not memoizing returned functions
return { value, setValue };  // New object every render

// Good - memoize return value
return useMemo(() => ({ value, setValue }), [value, setValue]);

// Bad - using global state for local concerns
const [isButtonHovered, setIsButtonHovered] = useGlobalState();

// Good - keep local state local
const [isButtonHovered, setIsButtonHovered] = useState(false);
```

## Quick Reference

**Constate:**
- Use for global state
- Split for performance
- Always memoize

**Context:**
- Use for simple cases
- Always provide default error
- Memoize value object

**State Organization:**
- Global: `src/states/`
- Feature: `routes/feature/hooks/`
- Component: `useState` in component

**Memoization:**
- `useCallback` for functions
- `useMemo` for objects/computed
- Never skip in state hooks
