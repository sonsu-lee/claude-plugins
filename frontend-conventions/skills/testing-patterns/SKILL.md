---
name: Testing Patterns
description: This skill should be used when the user asks to "write tests", "add test", "test component", "mock API", "test hook", or when writing tests for React/TypeScript applications. Provides guidance on Vitest, React Testing Library, MSW, and hook testing patterns.
---

# Testing Patterns

## Overview

This skill provides testing conventions for React/TypeScript applications using Vitest and React Testing Library. Focus is on user-centric testing, proper query priorities, and maintainable test patterns.

## Prerequisites

- Vitest for test runner
- React Testing Library for component testing
- MSW (Mock Service Worker) for API mocking
- Testing Library User Event for interactions

## Query Priority

Use queries in this order (most to least preferred):

### Accessible Queries (Preferred)

```tsx
// 1. getByRole - Best, tests accessibility
screen.getByRole('button', { name: 'Submit' });
screen.getByRole('heading', { level: 1 });
screen.getByRole('textbox', { name: 'Email' });

// 2. getByLabelText - For form fields
screen.getByLabelText('Email');
screen.getByLabelText(/password/i);

// 3. getByPlaceholderText - When no label
screen.getByPlaceholderText('Search...');

// 4. getByText - For non-interactive elements
screen.getByText('Welcome back');
screen.getByText(/error/i);
```

### Semantic Queries

```tsx
// 5. getByAltText - For images
screen.getByAltText('User avatar');

// 6. getByTitle - For tooltips
screen.getByTitle('Close dialog');
```

### Escape Hatches (Avoid When Possible)

```tsx
// 7. getByTestId - Last resort
screen.getByTestId('custom-element');
```

## Component Testing

### Basic Component Test

```tsx
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { Button } from './Button';

describe('Button', () => {
  it('renders children', () => {
    render(<Button>Click me</Button>);
    expect(screen.getByRole('button')).toHaveTextContent('Click me');
  });

  it('calls onClick when clicked', async () => {
    const user = userEvent.setup();
    const handleClick = vi.fn();

    render(<Button onClick={handleClick}>Click</Button>);

    await user.click(screen.getByRole('button'));

    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  it('is disabled when loading', () => {
    render(<Button isLoading>Submit</Button>);
    expect(screen.getByRole('button')).toBeDisabled();
  });
});
```

### Testing User Interactions

Always use `userEvent` over `fireEvent`:

```tsx
import userEvent from '@testing-library/user-event';

describe('Form', () => {
  it('submits form data', async () => {
    const user = userEvent.setup();
    const handleSubmit = vi.fn();

    render(<LoginForm onSubmit={handleSubmit} />);

    await user.type(screen.getByLabelText('Email'), 'test@example.com');
    await user.type(screen.getByLabelText('Password'), 'password123');
    await user.click(screen.getByRole('button', { name: 'Login' }));

    expect(handleSubmit).toHaveBeenCalledWith({
      email: 'test@example.com',
      password: 'password123',
    });
  });

  it('shows validation error for invalid email', async () => {
    const user = userEvent.setup();

    render(<LoginForm onSubmit={vi.fn()} />);

    await user.type(screen.getByLabelText('Email'), 'invalid-email');
    await user.click(screen.getByRole('button', { name: 'Login' }));

    expect(screen.getByRole('alert')).toHaveTextContent('Invalid email');
  });
});
```

### Async Testing

```tsx
describe('UserProfile', () => {
  it('loads and displays user data', async () => {
    render(<UserProfile userId="123" />);

    // Wait for loading to finish
    expect(screen.getByRole('status')).toHaveTextContent('Loading...');

    // Wait for content
    await screen.findByRole('heading', { name: 'John Doe' });

    expect(screen.getByText('john@example.com')).toBeInTheDocument();
  });

  it('shows error on fetch failure', async () => {
    server.use(
      http.get('/api/users/:id', () => {
        return HttpResponse.json({ error: 'Not found' }, { status: 404 });
      })
    );

    render(<UserProfile userId="invalid" />);

    await screen.findByRole('alert');
    expect(screen.getByRole('alert')).toHaveTextContent('User not found');
  });
});
```

## Hook Testing

### Testing Custom Hooks

```tsx
import { renderHook, act } from '@testing-library/react';
import { useCounter } from './useCounter';

describe('useCounter', () => {
  it('initializes with default value', () => {
    const { result } = renderHook(() => useCounter());
    expect(result.current.count).toBe(0);
  });

  it('initializes with provided value', () => {
    const { result } = renderHook(() => useCounter(10));
    expect(result.current.count).toBe(10);
  });

  it('increments count', () => {
    const { result } = renderHook(() => useCounter());

    act(() => {
      result.current.increment();
    });

    expect(result.current.count).toBe(1);
  });

  it('decrements count', () => {
    const { result } = renderHook(() => useCounter(5));

    act(() => {
      result.current.decrement();
    });

    expect(result.current.count).toBe(4);
  });
});
```

### Testing Hooks with Dependencies

```tsx
import { renderHook, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { useUser } from './useUser';

const createWrapper = () => {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: { retry: false },
    },
  });

  return ({ children }: { children: React.ReactNode }) => (
    <QueryClientProvider client={queryClient}>
      {children}
    </QueryClientProvider>
  );
};

describe('useUser', () => {
  it('fetches user data', async () => {
    const { result } = renderHook(() => useUser('123'), {
      wrapper: createWrapper(),
    });

    expect(result.current.isLoading).toBe(true);

    await waitFor(() => {
      expect(result.current.isLoading).toBe(false);
    });

    expect(result.current.user).toEqual({
      id: '123',
      name: 'John Doe',
    });
  });
});
```

## API Mocking with MSW

### Setup MSW

```tsx
// src/test/server.ts
import { setupServer } from 'msw/node';
import { handlers } from './handlers';

export const server = setupServer(...handlers);
```

```tsx
// src/test/handlers.ts
import { http, HttpResponse } from 'msw';

export const handlers = [
  http.get('/api/users', () => {
    return HttpResponse.json([
      { id: '1', name: 'John Doe' },
      { id: '2', name: 'Jane Doe' },
    ]);
  }),

  http.get('/api/users/:id', ({ params }) => {
    return HttpResponse.json({
      id: params.id,
      name: 'John Doe',
      email: 'john@example.com',
    });
  }),

  http.post('/api/users', async ({ request }) => {
    const body = await request.json();
    return HttpResponse.json({ id: '3', ...body }, { status: 201 });
  }),
];
```

### Setup in Tests

```tsx
// src/test/setup.ts
import { beforeAll, afterEach, afterAll } from 'vitest';
import { server } from './server';

beforeAll(() => server.listen({ onUnhandledRequest: 'error' }));
afterEach(() => server.resetHandlers());
afterAll(() => server.close());
```

### Override Handlers in Tests

```tsx
import { http, HttpResponse } from 'msw';
import { server } from '@/test/server';

describe('UserList', () => {
  it('shows empty state when no users', async () => {
    server.use(
      http.get('/api/users', () => {
        return HttpResponse.json([]);
      })
    );

    render(<UserList />);

    await screen.findByText('No users found');
  });

  it('shows error on server error', async () => {
    server.use(
      http.get('/api/users', () => {
        return HttpResponse.json(
          { error: 'Server error' },
          { status: 500 }
        );
      })
    );

    render(<UserList />);

    await screen.findByRole('alert');
  });
});
```

## Test Organization

### File Structure

```
Component/
├── index.tsx
├── styles.module.css
└── index.test.tsx    # Co-located tests
```

### Test Structure

```tsx
describe('ComponentName', () => {
  // Setup/teardown if needed
  beforeEach(() => {
    vi.clearAllMocks();
  });

  // Group related tests
  describe('rendering', () => {
    it('renders default state', () => { ... });
    it('renders with props', () => { ... });
  });

  describe('interactions', () => {
    it('handles click', async () => { ... });
    it('handles input', async () => { ... });
  });

  describe('error states', () => {
    it('shows error message', () => { ... });
    it('handles API error', async () => { ... });
  });
});
```

## Testing Patterns

### Arrange-Act-Assert

```tsx
it('adds item to cart', async () => {
  // Arrange
  const user = userEvent.setup();
  render(<ProductCard product={mockProduct} />);

  // Act
  await user.click(screen.getByRole('button', { name: 'Add to cart' }));

  // Assert
  expect(screen.getByRole('status')).toHaveTextContent('Added to cart');
});
```

### Testing Accessibility

```tsx
import { axe, toHaveNoViolations } from 'jest-axe';

expect.extend(toHaveNoViolations);

it('has no accessibility violations', async () => {
  const { container } = render(<Button>Click me</Button>);
  const results = await axe(container);
  expect(results).toHaveNoViolations();
});
```

### Testing Conditional Rendering

```tsx
describe('AuthButton', () => {
  it('shows login when not authenticated', () => {
    render(<AuthButton isAuthenticated={false} />);
    expect(screen.getByRole('button', { name: 'Login' })).toBeInTheDocument();
    expect(screen.queryByRole('button', { name: 'Logout' })).not.toBeInTheDocument();
  });

  it('shows logout when authenticated', () => {
    render(<AuthButton isAuthenticated={true} />);
    expect(screen.getByRole('button', { name: 'Logout' })).toBeInTheDocument();
    expect(screen.queryByRole('button', { name: 'Login' })).not.toBeInTheDocument();
  });
});
```

## Mocking

### Mocking Functions

```tsx
const mockOnSubmit = vi.fn();

render(<Form onSubmit={mockOnSubmit} />);

// After interaction
expect(mockOnSubmit).toHaveBeenCalledWith(expectedData);
expect(mockOnSubmit).toHaveBeenCalledTimes(1);
```

### Mocking Modules

```tsx
vi.mock('@/hooks/useAuth', () => ({
  useAuth: () => ({
    user: { id: '1', name: 'Test User' },
    isAuthenticated: true,
  }),
}));
```

### Mocking Browser APIs

```tsx
beforeEach(() => {
  Object.defineProperty(window, 'localStorage', {
    value: {
      getItem: vi.fn(),
      setItem: vi.fn(),
      removeItem: vi.fn(),
    },
  });
});
```

## Things to Avoid

### Anti-Patterns

```tsx
// Bad - testing implementation details
expect(component.state.isOpen).toBe(true);

// Good - testing behavior
expect(screen.getByRole('dialog')).toBeVisible();

// Bad - using container queries
container.querySelector('.button');

// Good - using accessible queries
screen.getByRole('button');

// Bad - waiting with arbitrary timeouts
await new Promise(r => setTimeout(r, 1000));

// Good - using waitFor or findBy
await screen.findByText('Loaded');
```

### What NOT to Test

- Implementation details
- Third-party library internals
- CSS class names
- Private methods
- Component structure

### What TO Test

- User interactions
- Component output/rendering
- Accessibility
- Error states
- Loading states
- Edge cases

## Quick Reference

**Query Priority:**
1. `getByRole` - Accessible name
2. `getByLabelText` - Form fields
3. `getByText` - Non-interactive content
4. `getByTestId` - Last resort

**User Events:**
- Always use `userEvent.setup()`
- Prefer `userEvent` over `fireEvent`
- Use `await` for all interactions

**Async:**
- Use `findBy*` for async content
- Use `waitFor` for assertions
- Never use arbitrary timeouts

**Mocking:**
- MSW for API calls
- `vi.fn()` for callbacks
- `vi.mock()` for modules
