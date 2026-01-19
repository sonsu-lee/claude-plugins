---
name: Storybook Patterns
description: This skill should be used when the user asks to "write story", "add storybook", "create stories", "document component", "add play function", or when writing Storybook stories for React components. Provides guidance on story structure, args, play functions, and documentation.
---

# Storybook Patterns

## Overview

This skill provides Storybook conventions for React component documentation and testing. Focus is on consistent story structure, proper args configuration, and interactive testing with play functions.

## Prerequisites

- Storybook 7+ with React
- TypeScript support
- Component Story Format (CSF) 3.0

## Story File Structure

### Basic Story File

```tsx
// components/Button/index.stories.tsx
import type { Meta, StoryObj } from '@storybook/react';
import { Button } from './index';

const meta = {
  title: 'Components/Button',
  component: Button,
  tags: ['autodocs'],
  argTypes: {
    variant: {
      control: 'select',
      options: ['primary', 'secondary', 'ghost'],
    },
    size: {
      control: 'radio',
      options: ['small', 'medium', 'large'],
    },
    onClick: { action: 'clicked' },
  },
} satisfies Meta<typeof Button>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {
    children: 'Button',
  },
};

export const Primary: Story = {
  args: {
    variant: 'primary',
    children: 'Primary Button',
  },
};

export const Secondary: Story = {
  args: {
    variant: 'secondary',
    children: 'Secondary Button',
  },
};
```

### File Location

```
ComponentName/
├── index.tsx
├── styles.module.css
└── index.stories.tsx   # Co-located with component
```

## Meta Configuration

### Required Fields

```tsx
const meta = {
  title: 'Category/ComponentName',  // Navigation path
  component: Button,                 // Component to document
} satisfies Meta<typeof Button>;
```

### Common Optional Fields

```tsx
const meta = {
  title: 'Components/Button',
  component: Button,
  tags: ['autodocs'],              // Auto-generate docs
  parameters: {
    layout: 'centered',            // 'centered' | 'fullscreen' | 'padded'
    docs: {
      description: {
        component: 'A button component with multiple variants.',
      },
    },
  },
  decorators: [
    (Story) => (
      <div style={{ padding: '1rem' }}>
        <Story />
      </div>
    ),
  ],
  argTypes: {
    // Control configurations
  },
} satisfies Meta<typeof Button>;
```

### Title Organization

```tsx
// Organize by category
'Components/Button'           // UI primitives
'Components/Forms/Input'      // Form elements
'Components/Feedback/Modal'   // Feedback elements
'Layouts/MainLayout'          // Layout components
'Features/UserProfile'        // Feature components
```

## Args Configuration

### ArgTypes Control

```tsx
argTypes: {
  // Select dropdown
  variant: {
    control: 'select',
    options: ['primary', 'secondary', 'ghost'],
    description: 'Visual style of the button',
    table: {
      defaultValue: { summary: 'primary' },
    },
  },

  // Radio buttons
  size: {
    control: 'radio',
    options: ['small', 'medium', 'large'],
  },

  // Boolean toggle
  disabled: {
    control: 'boolean',
  },

  // Number input
  count: {
    control: { type: 'number', min: 0, max: 100, step: 1 },
  },

  // Color picker
  color: {
    control: 'color',
  },

  // Text input
  label: {
    control: 'text',
  },

  // Object editor
  user: {
    control: 'object',
  },

  // Action logging
  onClick: { action: 'clicked' },
  onSubmit: { action: 'submitted' },
}
```

### Hiding Args

```tsx
argTypes: {
  // Hide from controls
  internalProp: {
    table: { disable: true },
  },

  // Hide from docs table
  className: {
    table: { disable: true },
  },
}
```

## Story Patterns

### Default Story

Always include a default story:

```tsx
export const Default: Story = {
  args: {
    children: 'Button',
  },
};
```

### Variant Stories

```tsx
export const Primary: Story = {
  args: {
    ...Default.args,
    variant: 'primary',
  },
};

export const Secondary: Story = {
  args: {
    ...Default.args,
    variant: 'secondary',
  },
};

export const Ghost: Story = {
  args: {
    ...Default.args,
    variant: 'ghost',
  },
};
```

### State Stories

```tsx
export const Loading: Story = {
  args: {
    ...Default.args,
    isLoading: true,
  },
};

export const Disabled: Story = {
  args: {
    ...Default.args,
    disabled: true,
  },
};

export const WithIcon: Story = {
  args: {
    ...Default.args,
    icon: <IconPlus />,
  },
};
```

### Composition Stories

```tsx
export const AllVariants: Story = {
  render: () => (
    <div style={{ display: 'flex', gap: '1rem' }}>
      <Button variant="primary">Primary</Button>
      <Button variant="secondary">Secondary</Button>
      <Button variant="ghost">Ghost</Button>
    </div>
  ),
};

export const AllSizes: Story = {
  render: () => (
    <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
      <Button size="small">Small</Button>
      <Button size="medium">Medium</Button>
      <Button size="large">Large</Button>
    </div>
  ),
};
```

## Play Functions

### Basic Interaction Testing

```tsx
import { expect, within, userEvent } from '@storybook/test';

export const ClickTest: Story = {
  args: {
    children: 'Click me',
  },
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement);
    const button = canvas.getByRole('button');

    await userEvent.click(button);
  },
};
```

### Form Testing

```tsx
export const FormSubmit: Story = {
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement);

    // Fill form
    await userEvent.type(
      canvas.getByLabelText('Email'),
      'test@example.com'
    );
    await userEvent.type(
      canvas.getByLabelText('Password'),
      'password123'
    );

    // Submit
    await userEvent.click(canvas.getByRole('button', { name: 'Login' }));

    // Assert
    await expect(canvas.getByText('Welcome')).toBeInTheDocument();
  },
};
```

### Async Assertions

```tsx
export const AsyncLoad: Story = {
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement);

    // Wait for loading to complete
    await expect(
      canvas.findByRole('heading', { name: 'Data Loaded' })
    ).resolves.toBeInTheDocument();

    // Assert content
    await expect(canvas.getByText('Item 1')).toBeInTheDocument();
  },
};
```

## Decorators

### Component Decorators

```tsx
const meta = {
  decorators: [
    // Wrapper decorator
    (Story) => (
      <div className="story-wrapper">
        <Story />
      </div>
    ),
  ],
} satisfies Meta<typeof Component>;
```

### Provider Decorators

```tsx
import { ThemeProvider } from '@/states/themeState';

const meta = {
  decorators: [
    (Story) => (
      <ThemeProvider>
        <Story />
      </ThemeProvider>
    ),
  ],
} satisfies Meta<typeof ThemedComponent>;
```

### Router Decorators

```tsx
import { MemoryRouter } from 'react-router-dom';

const meta = {
  decorators: [
    (Story) => (
      <MemoryRouter initialEntries={['/']}>
        <Story />
      </MemoryRouter>
    ),
  ],
} satisfies Meta<typeof NavigationComponent>;
```

## Parameters

### Layout Parameters

```tsx
parameters: {
  layout: 'centered',  // Center component
}

parameters: {
  layout: 'fullscreen',  // Full viewport
}

parameters: {
  layout: 'padded',  // Default padding
}
```

### Background Parameters

```tsx
parameters: {
  backgrounds: {
    default: 'dark',
    values: [
      { name: 'light', value: '#ffffff' },
      { name: 'dark', value: '#333333' },
    ],
  },
}
```

### Viewport Parameters

```tsx
parameters: {
  viewport: {
    defaultViewport: 'mobile1',
  },
}
```

## Documentation

### Component Description

```tsx
const meta = {
  parameters: {
    docs: {
      description: {
        component: `
A versatile button component that supports multiple variants and sizes.

## Usage

\`\`\`tsx
<Button variant="primary" size="medium">
  Click me
</Button>
\`\`\`
        `,
      },
    },
  },
} satisfies Meta<typeof Button>;
```

### Story Description

```tsx
export const WithIcon: Story = {
  parameters: {
    docs: {
      description: {
        story: 'Button with an icon on the left side.',
      },
    },
  },
  args: {
    icon: <IconPlus />,
    children: 'Add Item',
  },
};
```

## MSW Integration

### API Mocking in Stories

```tsx
import { http, HttpResponse } from 'msw';

export const WithData: Story = {
  parameters: {
    msw: {
      handlers: [
        http.get('/api/users', () => {
          return HttpResponse.json([
            { id: '1', name: 'John Doe' },
            { id: '2', name: 'Jane Doe' },
          ]);
        }),
      ],
    },
  },
};

export const WithError: Story = {
  parameters: {
    msw: {
      handlers: [
        http.get('/api/users', () => {
          return HttpResponse.json(
            { error: 'Server error' },
            { status: 500 }
          );
        }),
      ],
    },
  },
};
```

## Story Organization

### Naming Conventions

```tsx
// Default state
export const Default: Story = {};

// Variants (by prop value)
export const Primary: Story = {};
export const Secondary: Story = {};

// States
export const Loading: Story = {};
export const Disabled: Story = {};
export const Error: Story = {};

// Combinations
export const PrimarySmall: Story = {};
export const SecondaryLarge: Story = {};

// Compositions
export const AllVariants: Story = {};
export const FormExample: Story = {};
```

### Story Order

```tsx
const meta = {
  parameters: {
    docs: {
      // Control story order in docs
      stories: {
        order: ['Default', 'Primary', 'Secondary', '*'],
      },
    },
  },
} satisfies Meta<typeof Button>;
```

## Quick Reference

**File Structure:**
- Co-locate with component: `Component/index.stories.tsx`
- Use CSF 3.0 format
- Export meta as default

**Meta:**
- Required: `title`, `component`
- Recommended: `tags: ['autodocs']`
- Configure: `argTypes`, `parameters`, `decorators`

**Stories:**
- Always include `Default`
- Use `args` for props
- Use `render` for custom rendering
- Use `play` for interactions

**Decorators:**
- Wrap with providers
- Add layout styling
- Handle routing

For detailed story patterns, see `references/story-patterns.md`.
