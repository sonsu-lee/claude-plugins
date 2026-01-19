# TypeScript Naming Patterns

## Naming Convention Reference

### PascalCase

Use for:
- Type aliases
- Interfaces (when required)
- React components
- Classes
- Constant objects (enum alternatives)

```typescript
// Types
type UserProfile = {
  name: string;
  email: string;
};

// React components
export const UserCard = ({ user }: Props) => { ... };

// Classes
class ApiClient { ... }

// Constant objects (enum alternatives)
const HttpStatus = {
  Ok: 200,
  NotFound: 404,
  InternalError: 500,
} as const;
```

### camelCase

Use for everything else:
- Functions
- Variables
- Parameters
- Object properties
- Non-exported constants

```typescript
// Functions
function calculateTotal(items: Item[]): number { ... }

// Variables
const currentUser = await fetchUser();

// Parameters
function processOrder(orderId: string, options: Options) { ... }

// Object properties
const config = {
  apiUrl: 'https://api.example.com',
  maxRetries: 3,
};
```

### UPPER_SNAKE_CASE

Use ONLY for global constants meeting ALL criteria:
1. `const` declared
2. Immutable (including nested values)
3. Exported (globally accessible)

```typescript
// Correct - exported immutable primitive
export const MAX_RETRY_COUNT = 3;

// Correct - exported readonly array
export const SUPPORTED_LOCALES: readonly string[] = ['en', 'ja', 'ko'];

// Correct - exported frozen object
export const API_ENDPOINTS = Object.freeze({
  users: '/api/users',
  posts: '/api/posts',
});

// WRONG - not exported (use camelCase)
const maxRetryCount = 3;

// WRONG - mutable array (use camelCase)
export const supportedLocales: string[] = ['en', 'ja'];
```

### snake_case

Use ONLY when required by external APIs:

```typescript
// API response transformation
interface ApiResponse {
  user_id: string;      // External API format
  created_at: string;
}

// Internal usage - convert to camelCase
type User = {
  userId: string;
  createdAt: Date;
};
```

## Acronym Handling

Treat acronyms as regular words:

```typescript
// Good
const userId = '...';
const apiUrl = 'https://...';
const htmlContent = '<div>...</div>';
const xmlParser = new XmlParser();
const httpClient = createHttpClient();
type JsonResponse = { ... };

// Bad
const userID = '...';
const apiURL = 'https://...';
const HTMLContent = '...';
const XMLParser = ...;
const HTTPClient = ...;
```

## Special Naming Patterns

### Functional Programming Conventions

```typescript
// Array destructuring - head and tail
const [head, ...tail] = items;

// Object destructuring - rest
const { id, ...rest } = user;

// Reduce accumulator
items.reduce((acc, item) => acc + item.value, 0);

// Promise constructor
new Promise((resolve, reject) => { ... });
```

### Boolean Naming

Use adjective/participle form:

```typescript
// Good
type Props = {
  isLoading: boolean;
  isVisible: boolean;
  hasError: boolean;
  canEdit: boolean;
  wasSubmitted: boolean;
};

// Bad - noun form
type Props = {
  loading: boolean;      // OK but less explicit
  visibility: boolean;   // Wrong - noun
  errorState: boolean;   // Wrong - noun
};
```

### Event Handler Naming

- Props: `on` prefix (onSomething)
- Internal handlers: `handle` prefix (handleSomething)

```typescript
type ButtonProps = {
  onClick: () => void;
  onHover?: () => void;
};

function Button({ onClick, onHover }: ButtonProps) {
  const handleClick = () => {
    // internal logic
    onClick();
  };

  return <button onClick={handleClick}>Click</button>;
}
```

## Abbreviations to Avoid

| Avoid | Use Instead |
|-------|-------------|
| `idx` | `index` |
| `tmp` | `temporary` or descriptive name |
| `btn` | `button` |
| `fmt` | `format` |
| `msg` | `message` |
| `err` | `error` |
| `cd` | `code` or `changeDirectory` |
| `e` | `event` or `error` (context-dependent) |

### Acceptable Short Names

| Context | Acceptable |
|---------|------------|
| Array sort callback | `a`, `b` |
| Loop index | `i`, `j`, `k` |
| Generic type parameters | `T`, `U`, `K`, `V` |
| Coordinates | `x`, `y`, `z` |

```typescript
// Acceptable - conventional short forms
items.sort((a, b) => a.value - b.value);

for (let i = 0; i < items.length; i++) { ... }

function identity<T>(value: T): T { return value; }
```

## File and Directory Naming

### Components

```
components/
├── UserProfile/
│   ├── index.tsx           # Main component
│   ├── styles.module.css   # Styles
│   └── index.stories.tsx   # Storybook
└── Button/
    ├── index.tsx
    ├── styles.module.css
    └── index.stories.tsx
```

### Other Files

- Utilities: `camelCase.ts` (e.g., `formatDate.ts`)
- Types: `camelCase.ts` (e.g., `userTypes.ts`)
- Constants: `camelCase.ts` (e.g., `apiEndpoints.ts`)
- Hooks: `useSomething.ts` (e.g., `useAuth.ts`)

## Import Naming

Match file/directory names:

```typescript
// Component from directory
import { Footer } from './Footer';  // Not './Footer/index'

// Named exports
import { formatDate, parseDate } from './utils/dateUtils';

// Type imports
import type { User, UserProfile } from './types';
```
