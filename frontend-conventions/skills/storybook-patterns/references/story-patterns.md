# Storybook Story Patterns

## Complete Story Examples

### Button Component

```tsx
// components/Button/index.stories.tsx
import type { Meta, StoryObj } from '@storybook/react';
import { expect, within, userEvent } from '@storybook/test';
import { Button } from './index';

const meta = {
  title: 'Components/Button',
  component: Button,
  tags: ['autodocs'],
  parameters: {
    layout: 'centered',
    docs: {
      description: {
        component: 'A versatile button component with multiple variants, sizes, and states.',
      },
    },
  },
  argTypes: {
    variant: {
      control: 'select',
      options: ['primary', 'secondary', 'ghost', 'danger'],
      description: 'Visual style of the button',
      table: {
        type: { summary: 'string' },
        defaultValue: { summary: 'primary' },
      },
    },
    size: {
      control: 'radio',
      options: ['small', 'medium', 'large'],
      description: 'Size of the button',
      table: {
        type: { summary: 'string' },
        defaultValue: { summary: 'medium' },
      },
    },
    disabled: {
      control: 'boolean',
      description: 'Whether the button is disabled',
    },
    isLoading: {
      control: 'boolean',
      description: 'Whether the button shows a loading state',
    },
    onClick: { action: 'clicked' },
  },
} satisfies Meta<typeof Button>;

export default meta;
type Story = StoryObj<typeof meta>;

// Default story
export const Default: Story = {
  args: {
    children: 'Button',
    variant: 'primary',
    size: 'medium',
  },
};

// Variant stories
export const Primary: Story = {
  args: {
    ...Default.args,
    variant: 'primary',
    children: 'Primary Button',
  },
};

export const Secondary: Story = {
  args: {
    ...Default.args,
    variant: 'secondary',
    children: 'Secondary Button',
  },
};

export const Ghost: Story = {
  args: {
    ...Default.args,
    variant: 'ghost',
    children: 'Ghost Button',
  },
};

export const Danger: Story = {
  args: {
    ...Default.args,
    variant: 'danger',
    children: 'Delete',
  },
};

// Size stories
export const Small: Story = {
  args: {
    ...Default.args,
    size: 'small',
    children: 'Small',
  },
};

export const Large: Story = {
  args: {
    ...Default.args,
    size: 'large',
    children: 'Large Button',
  },
};

// State stories
export const Loading: Story = {
  args: {
    ...Default.args,
    isLoading: true,
    children: 'Loading...',
  },
};

export const Disabled: Story = {
  args: {
    ...Default.args,
    disabled: true,
    children: 'Disabled',
  },
};

// Composition story
export const AllVariants: Story = {
  render: () => (
    <div style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap' }}>
      <Button variant="primary">Primary</Button>
      <Button variant="secondary">Secondary</Button>
      <Button variant="ghost">Ghost</Button>
      <Button variant="danger">Danger</Button>
    </div>
  ),
};

// Interactive story with play function
export const ClickInteraction: Story = {
  args: Default.args,
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement);
    const button = canvas.getByRole('button');

    await userEvent.click(button);

    // Button should still be enabled after click
    await expect(button).toBeEnabled();
  },
};
```

### Form Component

```tsx
// components/LoginForm/index.stories.tsx
import type { Meta, StoryObj } from '@storybook/react';
import { expect, within, userEvent, waitFor } from '@storybook/test';
import { http, HttpResponse } from 'msw';
import { LoginForm } from './index';

const meta = {
  title: 'Components/Forms/LoginForm',
  component: LoginForm,
  tags: ['autodocs'],
  parameters: {
    layout: 'centered',
    docs: {
      description: {
        component: 'A login form with email and password fields.',
      },
    },
  },
  decorators: [
    (Story) => (
      <div style={{ width: '400px' }}>
        <Story />
      </div>
    ),
  ],
  argTypes: {
    onSubmit: { action: 'submitted' },
    onForgotPassword: { action: 'forgot-password' },
  },
} satisfies Meta<typeof LoginForm>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {};

export const WithError: Story = {
  args: {
    error: 'Invalid email or password',
  },
};

export const FilledForm: Story = {
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement);

    await userEvent.type(
      canvas.getByLabelText('Email'),
      'user@example.com'
    );
    await userEvent.type(
      canvas.getByLabelText('Password'),
      'password123'
    );
  },
};

export const SubmitForm: Story = {
  parameters: {
    msw: {
      handlers: [
        http.post('/api/login', async ({ request }) => {
          const body = await request.json();
          if (body.email === 'user@example.com') {
            return HttpResponse.json({ token: 'abc123' });
          }
          return HttpResponse.json(
            { error: 'Invalid credentials' },
            { status: 401 }
          );
        }),
      ],
    },
  },
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement);

    // Fill form
    await userEvent.type(
      canvas.getByLabelText('Email'),
      'user@example.com'
    );
    await userEvent.type(
      canvas.getByLabelText('Password'),
      'password123'
    );

    // Submit
    await userEvent.click(
      canvas.getByRole('button', { name: 'Login' })
    );

    // Wait for success
    await waitFor(() => {
      expect(canvas.queryByRole('alert')).not.toBeInTheDocument();
    });
  },
};

export const ValidationError: Story = {
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement);

    // Submit without filling
    await userEvent.click(
      canvas.getByRole('button', { name: 'Login' })
    );

    // Check for validation errors
    await expect(
      canvas.getByText('Email is required')
    ).toBeInTheDocument();
    await expect(
      canvas.getByText('Password is required')
    ).toBeInTheDocument();
  },
};
```

### Card Component

```tsx
// components/Card/index.stories.tsx
import type { Meta, StoryObj } from '@storybook/react';
import { Card, CardHeader, CardBody, CardFooter } from './index';
import { Button } from '../Button';

const meta = {
  title: 'Components/Card',
  component: Card,
  tags: ['autodocs'],
  parameters: {
    layout: 'centered',
  },
  argTypes: {
    variant: {
      control: 'select',
      options: ['default', 'elevated', 'outlined'],
    },
    interactive: {
      control: 'boolean',
    },
  },
  decorators: [
    (Story) => (
      <div style={{ width: '400px' }}>
        <Story />
      </div>
    ),
  ],
} satisfies Meta<typeof Card>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {
    children: (
      <>
        <CardHeader>
          <h3>Card Title</h3>
        </CardHeader>
        <CardBody>
          <p>Card content goes here. This is a simple card example.</p>
        </CardBody>
        <CardFooter>
          <Button variant="primary">Action</Button>
        </CardFooter>
      </>
    ),
  },
};

export const Elevated: Story = {
  args: {
    ...Default.args,
    variant: 'elevated',
  },
};

export const Outlined: Story = {
  args: {
    ...Default.args,
    variant: 'outlined',
  },
};

export const Interactive: Story = {
  args: {
    ...Default.args,
    interactive: true,
  },
  parameters: {
    docs: {
      description: {
        story: 'Interactive cards have hover effects and are clickable.',
      },
    },
  },
};

export const WithImage: Story = {
  render: () => (
    <Card>
      <img
        src="https://via.placeholder.com/400x200"
        alt="Placeholder"
        style={{ width: '100%', height: '200px', objectFit: 'cover' }}
      />
      <CardBody>
        <h3>Image Card</h3>
        <p>A card with an image header.</p>
      </CardBody>
    </Card>
  ),
};
```

### Modal Component

```tsx
// components/Modal/index.stories.tsx
import type { Meta, StoryObj } from '@storybook/react';
import { useState } from 'react';
import { within, userEvent, expect } from '@storybook/test';
import { Modal, ModalHeader, ModalBody, ModalFooter } from './index';
import { Button } from '../Button';

const meta = {
  title: 'Components/Feedback/Modal',
  component: Modal,
  tags: ['autodocs'],
  parameters: {
    layout: 'fullscreen',
    docs: {
      description: {
        component: 'A modal dialog with header, body, and footer sections.',
      },
    },
  },
  argTypes: {
    isOpen: { control: 'boolean' },
    size: {
      control: 'select',
      options: ['small', 'medium', 'large'],
    },
    onClose: { action: 'closed' },
  },
} satisfies Meta<typeof Modal>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {
    isOpen: true,
    size: 'medium',
    children: (
      <>
        <ModalHeader>Modal Title</ModalHeader>
        <ModalBody>
          <p>This is the modal content. You can put any content here.</p>
        </ModalBody>
        <ModalFooter>
          <Button variant="secondary">Cancel</Button>
          <Button variant="primary">Confirm</Button>
        </ModalFooter>
      </>
    ),
  },
};

export const Small: Story = {
  args: {
    ...Default.args,
    size: 'small',
  },
};

export const Large: Story = {
  args: {
    ...Default.args,
    size: 'large',
  },
};

// Interactive example with trigger button
export const WithTrigger: Story = {
  render: function Render() {
    const [isOpen, setIsOpen] = useState(false);

    return (
      <div style={{ padding: '2rem' }}>
        <Button onClick={() => setIsOpen(true)}>Open Modal</Button>
        <Modal isOpen={isOpen} onClose={() => setIsOpen(false)}>
          <ModalHeader>Confirmation</ModalHeader>
          <ModalBody>
            <p>Are you sure you want to proceed?</p>
          </ModalBody>
          <ModalFooter>
            <Button variant="secondary" onClick={() => setIsOpen(false)}>
              Cancel
            </Button>
            <Button variant="primary" onClick={() => setIsOpen(false)}>
              Confirm
            </Button>
          </ModalFooter>
        </Modal>
      </div>
    );
  },
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement);

    // Open modal
    await userEvent.click(canvas.getByRole('button', { name: 'Open Modal' }));

    // Modal should be visible
    await expect(canvas.getByRole('dialog')).toBeInTheDocument();
    await expect(canvas.getByText('Confirmation')).toBeInTheDocument();

    // Close modal
    await userEvent.click(canvas.getByRole('button', { name: 'Cancel' }));

    // Modal should be closed
    await expect(canvas.queryByRole('dialog')).not.toBeInTheDocument();
  },
};
```

### Data Table Component

```tsx
// components/DataTable/index.stories.tsx
import type { Meta, StoryObj } from '@storybook/react';
import { http, HttpResponse } from 'msw';
import { DataTable } from './index';

const mockUsers = [
  { id: '1', name: 'John Doe', email: 'john@example.com', role: 'Admin' },
  { id: '2', name: 'Jane Smith', email: 'jane@example.com', role: 'User' },
  { id: '3', name: 'Bob Johnson', email: 'bob@example.com', role: 'User' },
];

const columns = [
  { key: 'name' as const, header: 'Name' },
  { key: 'email' as const, header: 'Email' },
  { key: 'role' as const, header: 'Role' },
];

const meta = {
  title: 'Components/Data/DataTable',
  component: DataTable,
  tags: ['autodocs'],
  parameters: {
    layout: 'padded',
  },
  argTypes: {
    onRowClick: { action: 'row-clicked' },
  },
} satisfies Meta<typeof DataTable>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {
    data: mockUsers,
    columns,
  },
};

export const Empty: Story = {
  args: {
    data: [],
    columns,
  },
};

export const Loading: Story = {
  args: {
    data: [],
    columns,
    isLoading: true,
  },
};

export const WithCustomRender: Story = {
  args: {
    data: mockUsers,
    columns: [
      ...columns,
      {
        key: 'actions' as never,
        header: 'Actions',
        render: () => <button>Edit</button>,
      },
    ],
  },
};

export const WithAsyncData: Story = {
  parameters: {
    msw: {
      handlers: [
        http.get('/api/users', async () => {
          await new Promise(r => setTimeout(r, 1000));
          return HttpResponse.json(mockUsers);
        }),
      ],
    },
  },
  render: () => {
    // Component that fetches data
    return <AsyncDataTable />;
  },
};
```

## Play Function Patterns

### Form Validation

```tsx
export const FormValidation: Story = {
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement);

    // Submit empty form
    await userEvent.click(
      canvas.getByRole('button', { name: 'Submit' })
    );

    // Check validation messages
    await expect(
      canvas.getByText('This field is required')
    ).toBeInTheDocument();

    // Fill field and resubmit
    await userEvent.type(
      canvas.getByLabelText('Name'),
      'John Doe'
    );

    await userEvent.click(
      canvas.getByRole('button', { name: 'Submit' })
    );

    // Validation should pass
    await expect(
      canvas.queryByText('This field is required')
    ).not.toBeInTheDocument();
  },
};
```

### Async Operations

```tsx
export const AsyncOperation: Story = {
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement);

    // Trigger async action
    await userEvent.click(
      canvas.getByRole('button', { name: 'Load Data' })
    );

    // Wait for loading indicator
    await expect(canvas.getByRole('status')).toBeInTheDocument();

    // Wait for data to load
    await waitFor(
      () => {
        expect(canvas.queryByRole('status')).not.toBeInTheDocument();
      },
      { timeout: 5000 }
    );

    // Verify data is displayed
    await expect(canvas.getByText('Data Loaded')).toBeInTheDocument();
  },
};
```

### Keyboard Navigation

```tsx
export const KeyboardNavigation: Story = {
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement);

    // Focus first input
    await userEvent.click(canvas.getByLabelText('Email'));

    // Tab to next field
    await userEvent.tab();
    expect(canvas.getByLabelText('Password')).toHaveFocus();

    // Tab to button
    await userEvent.tab();
    expect(canvas.getByRole('button', { name: 'Submit' })).toHaveFocus();

    // Press Enter to submit
    await userEvent.keyboard('{Enter}');
  },
};
```

## Decorator Patterns

### Theme Decorator

```tsx
const meta = {
  decorators: [
    (Story, context) => {
      const theme = context.globals.theme || 'light';
      return (
        <ThemeProvider theme={theme}>
          <div data-theme={theme}>
            <Story />
          </div>
        </ThemeProvider>
      );
    },
  ],
} satisfies Meta<typeof Component>;
```

### Query Client Decorator

```tsx
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: false,
      staleTime: Infinity,
    },
  },
});

const meta = {
  decorators: [
    (Story) => (
      <QueryClientProvider client={queryClient}>
        <Story />
      </QueryClientProvider>
    ),
  ],
} satisfies Meta<typeof Component>;
```

### Combined Decorators

```tsx
const meta = {
  decorators: [
    // Router
    (Story) => (
      <MemoryRouter>
        <Story />
      </MemoryRouter>
    ),
    // Theme
    (Story) => (
      <ThemeProvider>
        <Story />
      </ThemeProvider>
    ),
    // Layout wrapper
    (Story) => (
      <div style={{ padding: '2rem' }}>
        <Story />
      </div>
    ),
  ],
} satisfies Meta<typeof Component>;
```

## Documentation Patterns

### Detailed Component Docs

```tsx
const meta = {
  parameters: {
    docs: {
      description: {
        component: `
## Button Component

A versatile button component that supports multiple variants and sizes.

### Features

- Multiple visual variants (primary, secondary, ghost)
- Three sizes (small, medium, large)
- Loading state with spinner
- Disabled state
- Icon support

### Accessibility

- Uses native \`<button>\` element
- Supports keyboard navigation
- Includes proper ARIA attributes
- Focus states for keyboard users

### Usage

\`\`\`tsx
import { Button } from '@/components/Button';

<Button variant="primary" size="medium" onClick={handleClick}>
  Click me
</Button>
\`\`\`
        `,
      },
    },
  },
} satisfies Meta<typeof Button>;
```

### Story Documentation

```tsx
export const WithIcon: Story = {
  parameters: {
    docs: {
      description: {
        story: `
Buttons can include icons for additional visual context.

Icons should be placed before the text for left-to-right reading flow.
Use consistent icon sizing across button sizes.
        `,
      },
    },
  },
  args: {
    icon: <IconPlus />,
    children: 'Add Item',
  },
};
```
