# React Component Structure Patterns

## Directory Structure

### Component Directory

Every component should be in its own directory:

```
components/
├── Button/
│   ├── index.tsx           # Main component
│   ├── styles.module.css   # Scoped styles
│   └── index.stories.tsx   # Storybook stories
├── UserProfile/
│   ├── index.tsx
│   ├── styles.module.css
│   ├── index.stories.tsx
│   └── Avatar/             # Sub-component
│       ├── index.tsx
│       ├── styles.module.css
│       └── index.stories.tsx
└── Layout/
    ├── index.tsx
    ├── Header/
    │   └── index.tsx
    └── Footer/
        └── index.tsx
```

### Why This Structure

1. **Cohesion** - Related files (component, styles, stories) are together
2. **Encapsulation** - Internal components are nested within parent
3. **Clean imports** - `import { Button } from './Button'`
4. **Scalability** - Easy to add tests, utils, types as needed

### What NOT to Do

```
# Bad - flat file structure
components/
├── Button.tsx
├── Button.module.css
├── Button.stories.tsx
├── UserProfile.tsx
├── UserProfile.module.css
├── UserProfileAvatar.tsx
├── UserProfileAvatar.module.css
└── ...
```

## File Content Order

### Order of Sections

```tsx
// ============================================
// 1. IMPORTS
// ============================================

// External libraries first
import { useState, useCallback } from 'react';
import { clsx } from 'clsx';

// Internal modules
import { formatDate } from '@/utils/date';
import type { User } from '@/types';

// Relative imports
import { Avatar } from './Avatar';
import styles from './styles.module.css';

// ============================================
// 2. EXPORTED COMPONENT
// ============================================

// 2a. Props type definition
type Props = {
  /** The user to display */
  user: User;
  /** Called when profile is clicked */
  onClick?: () => void;
};

// 2b. Component implementation
/**
 * Displays user profile information with avatar.
 */
export const UserProfile = ({ user, onClick }: Props) => {
  const [expanded, setExpanded] = useState(false);

  const handleClick = () => {
    setExpanded(!expanded);
    onClick?.();
  };

  return (
    <div className={styles.container} onClick={handleClick}>
      <Avatar src={user.avatarUrl} />
      <div className={styles.info}>
        <h3>{user.name}</h3>
        {expanded ? <DetailedInfo user={user} /> : null}
      </div>
    </div>
  );
};

// 2c. Component utilities (used only by this component)
function formatUserName(user: User): string {
  return `${user.firstName} ${user.lastName}`;
}

// ============================================
// 3. INTERNAL COMPONENTS (not exported)
// ============================================

// 3a. Internal component props
type DetailedInfoProps = {
  user: User;
};

// 3b. Internal component
const DetailedInfo = ({ user }: DetailedInfoProps) => {
  return (
    <div className={styles.details}>
      <p>Email: {user.email}</p>
      <p>Joined: {formatDate(user.createdAt)}</p>
    </div>
  );
};
```

### Why This Order

1. **Consumer focus** - Exports come first, what consumers care about
2. **Progressive detail** - Implementation details come after API
3. **Locality** - Internal components close to where they're used
4. **Scanability** - Easy to find what you're looking for

## Props Patterns

### Props Type Definition

```tsx
// Simple component
type Props = {
  /** User's display name */
  name: string;
  /** User's age */
  age: number;
  /** Optional profile image URL */
  imageUrl?: string;
};

// With children
type Props = {
  children: React.ReactNode;
  variant?: 'primary' | 'secondary';
};

// With HTML element props
type Props = {
  label: string;
} & Omit<React.ButtonHTMLAttributes<HTMLButtonElement>, 'type'>;
```

### Never Export Props Type

```tsx
// Bad - exposes implementation detail
export type Props = { ... };
export const Component = (props: Props) => { ... };

// Good - props type is internal
type Props = { ... };
export const Component = (props: Props) => { ... };

// Consumer needs props type? Use ComponentProps
import type { ComponentProps } from 'react';
import { Component } from './Component';

type ComponentProps = ComponentProps<typeof Component>;
```

### JSDoc Comments for Props

```tsx
type Props = {
  /**
   * The button's visual style.
   * @default 'primary'
   */
  variant?: 'primary' | 'secondary' | 'ghost';

  /**
   * Whether the button is disabled.
   * When disabled, onClick is not fired.
   */
  disabled?: boolean;

  /**
   * Called when the button is clicked.
   * @param event - The click event
   */
  onClick: (event: React.MouseEvent<HTMLButtonElement>) => void;
};
```

## Export Patterns

### Named Exports Only

```tsx
// Good - named export
export const Button = () => { ... };
export const IconButton = () => { ... };

// Bad - default export
export default function Button() { ... }
```

### Exception: Framework Requirements

```tsx
// Next.js page - default export required
export default function HomePage() {
  return <div>Home</div>;
}

// Storybook meta - default export required
export default {
  title: 'Components/Button',
  component: Button,
} satisfies Meta<typeof Button>;
```

## Component Types

### Simple Presentational

```tsx
type Props = {
  name: string;
  role: string;
};

export const UserCard = ({ name, role }: Props) => (
  <article className={styles.card}>
    <h3>{name}</h3>
    <p>{role}</p>
  </article>
);
```

### With Local State

```tsx
type Props = {
  initialValue?: number;
  onChange?: (value: number) => void;
};

export const Counter = ({ initialValue = 0, onChange }: Props) => {
  const [count, setCount] = useState(initialValue);

  const handleIncrement = () => {
    const newCount = count + 1;
    setCount(newCount);
    onChange?.(newCount);
  };

  return (
    <button onClick={handleIncrement}>
      Count: {count}
    </button>
  );
};
```

### With Custom Hook

```tsx
import { useAuth } from '@/hooks/useAuth';

type Props = {
  requiredRole: string;
  children: React.ReactNode;
};

export const ProtectedContent = ({ requiredRole, children }: Props) => {
  const { user, isLoading } = useAuth();

  if (isLoading) {
    return <LoadingSpinner />;
  }

  if (!user || user.role !== requiredRole) {
    return <AccessDenied />;
  }

  return <>{children}</>;
};
```

### Container Pattern (Separate Logic)

```tsx
// UserProfile/Container.tsx
import { useUser } from '@/hooks/useUser';
import { UserProfileView } from './View';

type Props = {
  userId: string;
};

export const UserProfileContainer = ({ userId }: Props) => {
  const { user, isLoading, error } = useUser(userId);

  if (isLoading) return <Skeleton />;
  if (error) return <ErrorMessage error={error} />;
  if (!user) return <NotFound />;

  return <UserProfileView user={user} />;
};

// UserProfile/View.tsx
type Props = {
  user: User;
};

export const UserProfileView = ({ user }: Props) => (
  <div className={styles.profile}>
    <Avatar src={user.avatarUrl} />
    <h2>{user.name}</h2>
    <p>{user.bio}</p>
  </div>
);

// UserProfile/index.tsx - re-export container as main
export { UserProfileContainer as UserProfile } from './Container';
```

## Internal Components

### When to Extract

Extract internal components when:
- Logic is complex enough to benefit from isolation
- JSX block is repeated
- Improves readability of parent component

```tsx
// Before - everything in one component
export const Dashboard = () => {
  return (
    <div>
      <header>
        <h1>Dashboard</h1>
        <nav>
          <a href="/home">Home</a>
          <a href="/settings">Settings</a>
        </nav>
      </header>
      {/* More complex JSX... */}
    </div>
  );
};

// After - extracted internal component
export const Dashboard = () => {
  return (
    <div>
      <DashboardHeader />
      {/* More complex JSX... */}
    </div>
  );
};

// Internal - not exported
const DashboardHeader = () => (
  <header>
    <h1>Dashboard</h1>
    <nav>
      <a href="/home">Home</a>
      <a href="/settings">Settings</a>
    </nav>
  </header>
);
```

### Internal Component Naming

```tsx
// Parent component name prefix for context
const DashboardHeader = () => { ... };
const DashboardSidebar = () => { ... };

// Or generic names if truly internal
const Header = () => { ... };
const Sidebar = () => { ... };
```

## Imports Order

```tsx
// 1. React and external libraries
import { useState, useEffect } from 'react';
import { clsx } from 'clsx';
import { format } from 'date-fns';

// 2. Internal absolute imports (utils, hooks, types)
import { formatCurrency } from '@/utils/format';
import { useAuth } from '@/hooks/useAuth';
import type { User, Product } from '@/types';

// 3. Relative imports (sibling components)
import { ProductCard } from '../ProductCard';

// 4. Current component imports (styles, sub-components)
import { ProductImage } from './ProductImage';
import styles from './styles.module.css';
```
