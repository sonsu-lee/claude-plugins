# Prop API Design

## Naming Conventions

Common prop names that MUST be consistent across all shared components:

| Prop | Type | Purpose | Convention |
|------|------|---------|------------|
| `size` | `'sm' \| 'md' \| 'lg'` | Component size | Always `sm/md/lg`, optionally `xs/xl` |
| `variant` | string union | Visual variant | Component-specific: `'solid' \| 'outline' \| 'ghost'` |
| `colorScheme` | string | Color theme | `'primary' \| 'danger' \| 'neutral'` etc. |
| `disabled` | boolean | Disabled state | Always `disabled`, never `isDisabled` |
| `className` | string | Custom CSS class | Always supported on root element |
| `children` | ReactNode | Primary content | Use for main content, not metadata |
| `as` / `asChild` | element type | Polymorphic render | Use when element type should be caller-controlled |

Pick ONE convention per prop name and use it everywhere. Inconsistency is worse than any specific choice.

```tsx
// CORRECT: consistent naming across components
<Button size="sm" variant="outline" disabled />
<Input size="sm" variant="outline" disabled />
<Badge size="sm" variant="outline" />

// WRONG: inconsistent naming
<Button size="small" kind="outline" isDisabled />
<Input inputSize="sm" variant="outline" disabled />
```

## Controlled vs Uncontrolled

Support both patterns. If `value` is provided, the component is controlled. If not, use internal state initialized from `defaultValue`.

```tsx
interface InputProps {
  value?: string;          // controlled
  defaultValue?: string;   // uncontrolled initial value
  onChange?: (value: string) => void;  // called in both modes
}

function Input({ value: controlledValue, defaultValue = '', onChange }: InputProps) {
  const [internalValue, setInternalValue] = React.useState(defaultValue);
  const isControlled = controlledValue !== undefined;
  const currentValue = isControlled ? controlledValue : internalValue;

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const next = e.target.value;
    if (!isControlled) setInternalValue(next);
    onChange?.(next);
  };

  return <input value={currentValue} onChange={handleChange} />;
}
```

Rule: if the component manages a value, always support both modes. Never force controlled-only. The consumer decides how to manage state.

## children vs Explicit Props

- `children` for primary content (what you would put between tags)
- Explicit props for metadata, secondary content, slots

```jsx
// children for primary content
<Button>Submit</Button>
<Alert>Something went wrong.</Alert>

// explicit props for metadata and secondary content
<Button icon={<ArrowIcon />} loading={true}>Submit</Button>
<Alert title="Error" action={<RetryButton />}>Something went wrong.</Alert>

// WRONG: using a prop for primary content
<Button label="Submit" />
<Alert message="Something went wrong." />
```

Exception: when the component renders the content in multiple places or needs to transform it, explicit props can be better.

```tsx
// Explicit prop justified: label is rendered in multiple places
<Tooltip content="Copy to clipboard">
  <Button>Copy</Button>
</Tooltip>
```

## Breaking Change Prevention

| Change | Safe? | Action |
|--------|-------|--------|
| Adding a new optional prop | SAFE | Ship it |
| Adding a new value to a union type | SAFE | May need UI handling |
| Changing a prop name | BREAKING | Deprecate old, support both, console.warn |
| Removing a prop | BREAKING | Deprecate first, remove in next major |
| Changing a prop type | BREAKING | Add new prop with new type, deprecate old |
| Changing default value | POTENTIALLY BREAKING | Evaluate impact, document in changelog |

Deprecation pattern:

```tsx
function Button({ variant, kind, ...props }: ButtonProps) {
  if (kind !== undefined) {
    if (process.env.NODE_ENV !== 'production') {
      console.warn('Button: `kind` is deprecated. Use `variant` instead.');
    }
    variant = variant ?? kind;
  }
  // use variant from here on
}
```

Keep deprecated props working for at least one major version. Remove them only in the next major release with a migration guide.

## Default Values

Most common usage should work with zero or minimal props:

```jsx
// These should all render something useful with no extra props
<Button>Submit</Button>        // → primary, medium-sized button
<Input />                      // → text input, no value, ready to type
<Badge>New</Badge>             // → default color, default size
<Modal open={open}>Content</Modal>  // → centered, default width
```

Defaults represent the "80% case" — the most common way the component is used. If your defaults require overrides in most usages, the defaults are wrong.

```tsx
// CORRECT: sensible defaults, override only when needed
interface ButtonProps {
  size?: 'sm' | 'md' | 'lg';       // default: 'md'
  variant?: 'solid' | 'outline' | 'ghost';  // default: 'solid'
  type?: 'button' | 'submit' | 'reset';     // default: 'button' (not 'submit'!)
}
```

## Ref Forwarding

Always forward ref to the root DOM element:

```tsx
const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ children, variant = 'solid', size = 'md', ...props }, ref) => (
    <button
      ref={ref}
      className={clsx('btn', `btn-${variant}`, `btn-${size}`)}
      {...props}
    >
      {children}
    </button>
  )
);
Button.displayName = 'Button';
```

This enables: DOM measurement, focus management, third-party library integration (e.g., tooltips, popovers, drag-and-drop).

Never skip `displayName` — it is required for readable React DevTools output and useful error messages.

## Event Handlers

- Follow React conventions: `onClick`, `onChange`, `onBlur`, `onFocus`
- Always pass the original event as first argument
- Add component-specific data as second argument if needed

```tsx
// Simple: standard event forwarding
<Button onClick={(e) => console.log(e)} />

// Extended: component-specific data as second argument
interface SelectProps {
  onChange?: (event: React.SyntheticEvent, data: { value: string; label: string }) => void;
}

function Select({ onChange, options }: SelectProps) {
  const handleChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const selected = options.find(o => o.value === e.target.value);
    onChange?.(e, { value: selected.value, label: selected.label });
  };
  return <select onChange={handleChange}>...</select>;
}
```

Never swallow events. If the component handles an event internally, still allow the caller's handler to fire:

```tsx
// CORRECT: internal handling + caller's handler
function Input({ onChange, onFocus, ...props }: InputProps) {
  const handleFocus = (e: React.FocusEvent<HTMLInputElement>) => {
    setFocused(true);   // internal
    onFocus?.(e);       // caller's handler still fires
  };
  return <input onFocus={handleFocus} {...props} />;
}
```

## Polymorphic `as` / `asChild` Pattern

### `as` prop — renders as a different element type

```jsx
<Button as="a" href="/link">Navigate</Button>
<Text as="label" htmlFor="email">Email</Text>
<Box as="section">Content</Box>
```

### `asChild` prop (Radix pattern) — merges behavior onto child element

```jsx
<Button asChild>
  <a href="/link">Navigate</a>
</Button>

<Tooltip>
  <TooltipTrigger asChild>
    <IconButton><InfoIcon /></IconButton>
  </TooltipTrigger>
  <TooltipContent>More info</TooltipContent>
</Tooltip>
```

### When to use

- Component needs to render as different HTML elements (button → a, div → section)
- Wrapper would add unwanted DOM nesting
- Consumer needs full control over the rendered element

### Prefer `asChild` over `as`

`asChild` is more type-safe and composable. With `as`, TypeScript cannot easily infer which props are valid for the target element. With `asChild`, the child element carries its own type information.

```tsx
// as: type safety is hard — does Button accept href?
<Button as="a" href="/link">Navigate</Button>

// asChild: type safety is natural — <a> accepts href
<Button asChild>
  <a href="/link">Navigate</a>
</Button>
```

### Implementation sketch for `asChild`

```tsx
import { Slot } from '@radix-ui/react-slot';

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ asChild, children, className, variant = 'solid', ...props }, ref) => {
    const Component = asChild ? Slot : 'button';
    return (
      <Component
        ref={ref}
        className={clsx('btn', `btn-${variant}`, className)}
        {...props}
      >
        {children}
      </Component>
    );
  }
);
```
