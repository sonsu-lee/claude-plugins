# React Hooks Patterns

## Core Principles

1. **Follow the Rules of Hooks** - Only call at top level, only in React functions
2. **Complete dependency arrays** - Include all values used inside
3. **Memoize custom hook returns** - Prevent unnecessary re-renders
4. **Avoid premature memoization** - Components don't usually need it

## useState

### Basic Usage

```tsx
// Simple state
const [count, setCount] = useState(0);

// Object state
const [user, setUser] = useState<User | null>(null);

// Lazy initial state (for expensive computations)
const [data, setData] = useState(() => expensiveComputation());
```

### Functional Updates

Use functional form when new state depends on previous:

```tsx
// Good - uses previous state
setCount(prev => prev + 1);

// Bad - may use stale state in async/closures
setCount(count + 1);
```

### Object State Updates

Always create new object references:

```tsx
// Good - new object
setUser(prev => ({ ...prev, name: 'New Name' }));

// Bad - mutation
setUser(prev => {
  prev.name = 'New Name';  // Mutation!
  return prev;
});
```

## useEffect

### Dependency Array Rules

**Always include all referenced values:**

```tsx
// Bad - missing dependency
useEffect(() => {
  fetchUser(userId);  // userId not in deps
}, []);

// Good - all dependencies included
useEffect(() => {
  fetchUser(userId);
}, [userId]);
```

**Never lie about dependencies:**

```tsx
// Bad - skipping effect runs with empty array
useEffect(() => {
  const timer = setInterval(() => {
    setCount(count + 1);  // Uses stale count
  }, 1000);
  return () => clearInterval(timer);
}, []);  // eslint-disable-line - DON'T DO THIS

// Good - use functional update
useEffect(() => {
  const timer = setInterval(() => {
    setCount(c => c + 1);  // No dependency on count
  }, 1000);
  return () => clearInterval(timer);
}, []);
```

### Cleanup Functions

Always clean up subscriptions, timers, etc.:

```tsx
useEffect(() => {
  const subscription = eventEmitter.subscribe(handler);

  // Cleanup on unmount or before re-run
  return () => {
    subscription.unsubscribe();
  };
}, [handler]);
```

### Data Fetching Pattern

```tsx
useEffect(() => {
  let cancelled = false;

  async function fetchData() {
    const result = await api.fetchUser(userId);
    if (!cancelled) {
      setUser(result);
    }
  }

  fetchData();

  return () => {
    cancelled = true;
  };
}, [userId]);
```

## useCallback

### When to Use in Components

Only use when the function is a dependency of another hook:

```tsx
// Necessary - fetchData is a useEffect dependency
const fetchData = useCallback(async () => {
  const result = await api.fetch(query);
  setData(result);
}, [query]);

useEffect(() => {
  fetchData();
}, [fetchData]);
```

### When NOT to Use in Components

Don't memoize event handlers passed to HTML elements:

```tsx
// Unnecessary - onClick doesn't cause re-renders
const handleClick = useCallback(() => {
  doSomething();
}, []);

// Just use regular function
const handleClick = () => {
  doSomething();
};
```

### Always Use in Custom Hooks

Memoize ALL returned functions from custom hooks:

```tsx
function useToggle(initial = false) {
  const [value, setValue] = useState(initial);

  // Always memoize returned functions
  const toggle = useCallback(() => {
    setValue(v => !v);
  }, []);

  const setTrue = useCallback(() => {
    setValue(true);
  }, []);

  const setFalse = useCallback(() => {
    setValue(false);
  }, []);

  return { value, toggle, setTrue, setFalse };
}
```

## useMemo

### When to Use

1. **Expensive computations:**

```tsx
const sortedItems = useMemo(() => {
  return items.slice().sort((a, b) => a.name.localeCompare(b.name));
}, [items]);
```

2. **Referentially stable values for useEffect:**

```tsx
const config = useMemo(() => ({
  url: apiUrl,
  headers: { 'X-Token': token },
}), [apiUrl, token]);

useEffect(() => {
  fetchWithConfig(config);
}, [config]);
```

3. **Always in custom hooks:**

```tsx
function useFilteredItems(items: Item[], filter: string) {
  // Memoize to prevent re-renders in consumers
  const filtered = useMemo(() => {
    return items.filter(item => item.name.includes(filter));
  }, [items, filter]);

  return filtered;
}
```

### When NOT to Use

```tsx
// Unnecessary - simple operations
const fullName = useMemo(() => {
  return `${firstName} ${lastName}`;
}, [firstName, lastName]);

// Just compute directly
const fullName = `${firstName} ${lastName}`;
```

## useRef

### DOM References

```tsx
function TextInput() {
  const inputRef = useRef<HTMLInputElement>(null);

  const focusInput = () => {
    inputRef.current?.focus();
  };

  return (
    <>
      <input ref={inputRef} />
      <button onClick={focusInput}>Focus</button>
    </>
  );
}
```

### Mutable Values (Not Triggering Re-render)

```tsx
function Timer() {
  const intervalRef = useRef<number | null>(null);
  const [count, setCount] = useState(0);

  useEffect(() => {
    intervalRef.current = window.setInterval(() => {
      setCount(c => c + 1);
    }, 1000);

    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
      }
    };
  }, []);

  return <div>{count}</div>;
}
```

### Previous Value Pattern

```tsx
function usePrevious<T>(value: T): T | undefined {
  const ref = useRef<T>();

  useEffect(() => {
    ref.current = value;
  }, [value]);

  return ref.current;
}
```

## Custom Hooks

### Naming Convention

Always start with `use`:

```tsx
function useAuth() { ... }
function useLocalStorage() { ... }
function useDebounce() { ... }
```

### Return Value Patterns

**Single value:**

```tsx
function useWindowWidth(): number {
  const [width, setWidth] = useState(window.innerWidth);
  // ...
  return width;
}
```

**Object (most common):**

```tsx
function useAuth() {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  const login = useCallback(async (credentials: Credentials) => {
    // ...
  }, []);

  const logout = useCallback(() => {
    // ...
  }, []);

  return { user, isLoading, login, logout };
}
```

**Tuple (for simple state + action):**

```tsx
function useToggle(initial = false): [boolean, () => void] {
  const [value, setValue] = useState(initial);
  const toggle = useCallback(() => setValue(v => !v), []);
  return [value, toggle];
}
```

### Memoization Requirements

**Always memoize returned values and functions:**

```tsx
function useSearch(items: Item[]) {
  const [query, setQuery] = useState('');

  // Memoize computed values
  const filteredItems = useMemo(() => {
    return items.filter(item =>
      item.name.toLowerCase().includes(query.toLowerCase())
    );
  }, [items, query]);

  // Memoize callbacks
  const clearSearch = useCallback(() => {
    setQuery('');
  }, []);

  return {
    query,
    setQuery,
    filteredItems,
    clearSearch,
  };
}
```

**Why this matters:**

```tsx
// Without memoization in hook
function useBadSearch(items: Item[]) {
  const [query, setQuery] = useState('');

  // New array every render!
  const filteredItems = items.filter(...);

  // New function every render!
  const clearSearch = () => setQuery('');

  return { filteredItems, clearSearch };
}

// Consumer re-renders even when items/query unchanged
function SearchResults() {
  const { filteredItems, clearSearch } = useBadSearch(items);

  // These effects run every render!
  useEffect(() => {
    console.log(filteredItems);
  }, [filteredItems]);
}
```

## useContext

### Creating Context

```tsx
type Theme = 'light' | 'dark';

type ThemeContextValue = {
  theme: Theme;
  toggleTheme: () => void;
};

const ThemeContext = createContext<ThemeContextValue | null>(null);
```

### Provider Component

```tsx
export function ThemeProvider({ children }: { children: React.ReactNode }) {
  const [theme, setTheme] = useState<Theme>('light');

  const toggleTheme = useCallback(() => {
    setTheme(t => t === 'light' ? 'dark' : 'light');
  }, []);

  const value = useMemo(() => ({
    theme,
    toggleTheme,
  }), [theme, toggleTheme]);

  return (
    <ThemeContext.Provider value={value}>
      {children}
    </ThemeContext.Provider>
  );
}
```

### Custom Hook for Context

```tsx
export function useTheme(): ThemeContextValue {
  const context = useContext(ThemeContext);

  if (!context) {
    throw new Error('useTheme must be used within ThemeProvider');
  }

  return context;
}
```

## Common Patterns

### Debounced Value

```tsx
function useDebounce<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState(value);

  useEffect(() => {
    const timer = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);

    return () => clearTimeout(timer);
  }, [value, delay]);

  return debouncedValue;
}
```

### Local Storage

```tsx
function useLocalStorage<T>(key: string, initialValue: T) {
  const [storedValue, setStoredValue] = useState<T>(() => {
    try {
      const item = window.localStorage.getItem(key);
      return item ? JSON.parse(item) : initialValue;
    } catch {
      return initialValue;
    }
  });

  const setValue = useCallback((value: T | ((prev: T) => T)) => {
    setStoredValue(prev => {
      const valueToStore = value instanceof Function ? value(prev) : value;
      window.localStorage.setItem(key, JSON.stringify(valueToStore));
      return valueToStore;
    });
  }, [key]);

  return [storedValue, setValue] as const;
}
```

### Event Listener

```tsx
function useEventListener<K extends keyof WindowEventMap>(
  eventName: K,
  handler: (event: WindowEventMap[K]) => void
) {
  const savedHandler = useRef(handler);

  useEffect(() => {
    savedHandler.current = handler;
  }, [handler]);

  useEffect(() => {
    const eventListener = (event: WindowEventMap[K]) => {
      savedHandler.current(event);
    };

    window.addEventListener(eventName, eventListener);
    return () => window.removeEventListener(eventName, eventListener);
  }, [eventName]);
}
```
