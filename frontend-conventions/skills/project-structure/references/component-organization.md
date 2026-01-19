# Component Organization Patterns

## Component Directory Pattern

Every component lives in its own directory with related files:

```
ComponentName/
├── index.tsx           # Main component
├── styles.module.css   # Scoped styles
├── index.stories.tsx   # Storybook stories (optional)
├── index.test.tsx      # Tests (optional)
└── types.ts            # Component types (optional)
```

### Why Directory Per Component

| Benefit | Description |
|---------|-------------|
| **Cohesion** | Related files grouped together |
| **Clean imports** | `import { Button } from '@/components/Button'` |
| **Encapsulation** | Internal components stay private |
| **Scalability** | Easy to add tests, utils, stories |
| **Refactoring** | Move/delete entire directory |

### What NOT to Do

```
# Bad - flat files
components/
├── Button.tsx
├── Button.module.css
├── Button.stories.tsx
├── Card.tsx
├── Card.module.css
├── Card.stories.tsx
└── ... (grows into unmaintainable mess)
```

## Shared vs Feature Components

### Decision Matrix

| Question | If Yes → | If No → |
|----------|----------|---------|
| Used in multiple features? | Shared | Feature |
| Generic/primitive UI element? | Shared | Feature |
| Has business logic? | Feature | Either |
| Could be extracted to library? | Shared | Feature |

### Shared Components (`components/`)

```
components/
├── primitives/              # Base UI elements
│   ├── Button/
│   ├── Input/
│   ├── Select/
│   └── Checkbox/
├── feedback/                # User feedback
│   ├── Modal/
│   ├── Toast/
│   ├── Alert/
│   └── Spinner/
├── layout/                  # Layout helpers
│   ├── Container/
│   ├── Grid/
│   ├── Stack/
│   └── Divider/
├── navigation/              # Navigation elements
│   ├── Tabs/
│   ├── Breadcrumb/
│   └── Pagination/
└── data/                    # Data display
    ├── Table/
    ├── Card/
    └── Badge/
```

### Feature Components (`routes/feature/components/`)

```
routes/users/components/
├── UserTable/              # Users-specific table
├── UserCard/               # User display card
├── UserForm/               # User create/edit form
├── UserAvatar/             # User avatar display
└── UserFilters/            # User list filters
```

## Component Hierarchy

### Nesting Pattern

Sub-components nest within parent directories:

```
Modal/
├── index.tsx
├── styles.module.css
├── ModalHeader/
│   ├── index.tsx
│   └── styles.module.css
├── ModalBody/
│   ├── index.tsx
│   └── styles.module.css
└── ModalFooter/
    ├── index.tsx
    └── styles.module.css
```

### Export Pattern

```tsx
// Modal/index.tsx
export { Modal } from './Modal';
export { ModalHeader } from './ModalHeader';
export { ModalBody } from './ModalBody';
export { ModalFooter } from './ModalFooter';
```

### Usage

```tsx
import { Modal, ModalHeader, ModalBody, ModalFooter } from '@/components/Modal';

<Modal isOpen={isOpen} onClose={handleClose}>
  <ModalHeader>Title</ModalHeader>
  <ModalBody>Content</ModalBody>
  <ModalFooter>
    <Button onClick={handleClose}>Close</Button>
  </ModalFooter>
</Modal>
```

## Component Types

### Presentational Components

Display data, no business logic:

```tsx
// components/UserCard/index.tsx
type Props = {
  name: string;
  email: string;
  avatarUrl: string;
};

export const UserCard = ({ name, email, avatarUrl }: Props) => (
  <article className={styles.card}>
    <img src={avatarUrl} alt="" className={styles.avatar} />
    <h3 className={styles.name}>{name}</h3>
    <p className={styles.email}>{email}</p>
  </article>
);
```

### Container Components

Handle data fetching, state, business logic:

```tsx
// routes/users/[userId]/index.tsx
import { useParams } from 'react-router-dom';
import { useUser } from '../hooks/useUser';
import { UserProfile } from '../components/UserProfile';

export const UserDetailPage = () => {
  const { userId } = useParams<{ userId: string }>();
  const { user, isLoading, error } = useUser(userId!);

  if (isLoading) return <Spinner />;
  if (error) return <ErrorMessage error={error} />;
  if (!user) return <NotFound />;

  return <UserProfile user={user} />;
};
```

### Compound Components

Related components that work together:

```tsx
// components/Tabs/index.tsx
import { createContext, useContext, useState } from 'react';

type TabsContextValue = {
  activeTab: string;
  setActiveTab: (tab: string) => void;
};

const TabsContext = createContext<TabsContextValue | null>(null);

export const Tabs = ({ defaultTab, children }: TabsProps) => {
  const [activeTab, setActiveTab] = useState(defaultTab);

  return (
    <TabsContext.Provider value={{ activeTab, setActiveTab }}>
      <div className={styles.tabs}>{children}</div>
    </TabsContext.Provider>
  );
};

export const TabList = ({ children }: { children: React.ReactNode }) => (
  <div role="tablist" className={styles.tabList}>
    {children}
  </div>
);

export const Tab = ({ id, children }: TabProps) => {
  const { activeTab, setActiveTab } = useContext(TabsContext)!;

  return (
    <button
      role="tab"
      aria-selected={activeTab === id}
      onClick={() => setActiveTab(id)}
      className={styles.tab}
    >
      {children}
    </button>
  );
};

export const TabPanel = ({ id, children }: TabPanelProps) => {
  const { activeTab } = useContext(TabsContext)!;

  if (activeTab !== id) return null;

  return (
    <div role="tabpanel" className={styles.panel}>
      {children}
    </div>
  );
};
```

Usage:

```tsx
<Tabs defaultTab="general">
  <TabList>
    <Tab id="general">General</Tab>
    <Tab id="security">Security</Tab>
  </TabList>
  <TabPanel id="general">General settings...</TabPanel>
  <TabPanel id="security">Security settings...</TabPanel>
</Tabs>
```

## Component File Structure

### Standard Component File

```tsx
// components/Button/index.tsx

// 1. Imports
import { forwardRef } from 'react';
import { clsx } from 'clsx';
import styles from './styles.module.css';

// 2. Types
type Props = {
  variant?: 'primary' | 'secondary' | 'ghost';
  size?: 'small' | 'medium' | 'large';
  isLoading?: boolean;
  children: React.ReactNode;
} & Omit<React.ButtonHTMLAttributes<HTMLButtonElement>, 'className'>;

// 3. Component
export const Button = forwardRef<HTMLButtonElement, Props>(
  ({ variant = 'primary', size = 'medium', isLoading, children, ...props }, ref) => (
    <button
      ref={ref}
      className={clsx(
        styles.button,
        styles[variant],
        styles[size],
        isLoading && styles.loading
      )}
      disabled={isLoading || props.disabled}
      {...props}
    >
      {isLoading ? <Spinner size="small" /> : children}
    </button>
  )
);

Button.displayName = 'Button';
```

### Component with Internal Components

```tsx
// components/DataTable/index.tsx

import styles from './styles.module.css';

// Types
type Column<T> = {
  key: keyof T;
  header: string;
  render?: (value: T[keyof T], row: T) => React.ReactNode;
};

type Props<T> = {
  data: T[];
  columns: Column<T>[];
  onRowClick?: (row: T) => void;
};

// Main component
export const DataTable = <T extends { id: string }>({
  data,
  columns,
  onRowClick,
}: Props<T>) => (
  <table className={styles.table}>
    <TableHeader columns={columns} />
    <TableBody data={data} columns={columns} onRowClick={onRowClick} />
  </table>
);

// Internal components
type TableHeaderProps<T> = {
  columns: Column<T>[];
};

const TableHeader = <T,>({ columns }: TableHeaderProps<T>) => (
  <thead>
    <tr>
      {columns.map((col) => (
        <th key={String(col.key)}>{col.header}</th>
      ))}
    </tr>
  </thead>
);

type TableBodyProps<T> = {
  data: T[];
  columns: Column<T>[];
  onRowClick?: (row: T) => void;
};

const TableBody = <T extends { id: string }>({
  data,
  columns,
  onRowClick,
}: TableBodyProps<T>) => (
  <tbody>
    {data.map((row) => (
      <tr key={row.id} onClick={() => onRowClick?.(row)}>
        {columns.map((col) => (
          <td key={String(col.key)}>
            {col.render ? col.render(row[col.key], row) : String(row[col.key])}
          </td>
        ))}
      </tr>
    ))}
  </tbody>
);
```

## Re-export Patterns

### Barrel Exports

For component groups:

```tsx
// components/primitives/index.ts
export { Button } from './Button';
export { Input } from './Input';
export { Select } from './Select';
export { Checkbox } from './Checkbox';
```

### Index File Pattern

Component directory always exports from index:

```tsx
// components/Modal/index.tsx
export { Modal } from './Modal';
export type { ModalProps } from './Modal';
```

### Avoid Deep Imports

```tsx
// Bad - importing internal file
import { Modal } from '@/components/Modal/Modal';

// Good - importing from index
import { Modal } from '@/components/Modal';
```

## Testing Organization

### Co-located Tests

```
Button/
├── index.tsx
├── styles.module.css
├── index.test.tsx         # Component tests
└── index.stories.tsx      # Storybook stories
```

### Test File Pattern

```tsx
// components/Button/index.test.tsx
import { render, screen, fireEvent } from '@testing-library/react';
import { Button } from './index';

describe('Button', () => {
  it('renders children', () => {
    render(<Button>Click me</Button>);
    expect(screen.getByRole('button')).toHaveTextContent('Click me');
  });

  it('calls onClick when clicked', () => {
    const handleClick = vi.fn();
    render(<Button onClick={handleClick}>Click</Button>);
    fireEvent.click(screen.getByRole('button'));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  it('disables button when isLoading', () => {
    render(<Button isLoading>Submit</Button>);
    expect(screen.getByRole('button')).toBeDisabled();
  });
});
```

## Style Organization

### CSS Modules Structure

```css
/* components/Card/styles.module.css */

/* Base styles */
.card {
  display: flex;
  flex-direction: column;
  padding: 16px;
  background-color: #ffffff;
  border: 1px solid #eeeeee;
  border-radius: 8px;
}

/* Variants */
.elevated {
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  border: none;
}

.outlined {
  border: 2px solid #dddddd;
}

/* States */
.interactive {
  cursor: pointer;
  transition: box-shadow 0.2s;
}

.interactive:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

/* Children */
.header {
  margin-bottom: 12px;
}

.body {
  flex: 1;
}

.footer {
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px solid #eeeeee;
}
```

### Using Styles

```tsx
import { clsx } from 'clsx';
import styles from './styles.module.css';

type Props = {
  variant?: 'default' | 'elevated' | 'outlined';
  interactive?: boolean;
  children: React.ReactNode;
};

export const Card = ({
  variant = 'default',
  interactive = false,
  children,
}: Props) => (
  <div
    className={clsx(
      styles.card,
      variant !== 'default' && styles[variant],
      interactive && styles.interactive
    )}
  >
    {children}
  </div>
);
```

## Component Documentation

### JSDoc Comments

```tsx
/**
 * A button component with multiple variants and sizes.
 *
 * @example
 * ```tsx
 * <Button variant="primary" size="large">
 *   Click me
 * </Button>
 * ```
 */
export const Button = ({ variant, size, children }: Props) => {
  // ...
};
```

### Props Documentation

```tsx
type Props = {
  /**
   * The visual style of the button.
   * @default 'primary'
   */
  variant?: 'primary' | 'secondary' | 'ghost';

  /**
   * The size of the button.
   * @default 'medium'
   */
  size?: 'small' | 'medium' | 'large';

  /**
   * Whether the button shows a loading spinner.
   * When true, the button is also disabled.
   */
  isLoading?: boolean;

  /**
   * The button's content.
   */
  children: React.ReactNode;
};
```

## Migration Patterns

### Extracting to Shared Component

1. Identify reusable component in feature
2. Create directory in `components/`
3. Move component and styles
4. Update imports in original location
5. Document component

### Splitting Large Components

1. Identify logical sections
2. Create sub-component directories
3. Extract sections to sub-components
4. Keep state in parent
5. Pass data via props
