# Composition: Extend vs Separate

## Decision Framework: Extend or Separate?

### Extend (add variant to existing) when:

- Same semantic purpose (Button with icon is still a Button)
- Shared core behavior, visual variation only
- Consumer expects to find it in the same component
- Example: `<Button variant="outline">` not `<OutlineButton>`

### Separate when:

- Different semantic purpose (Button vs Link, even if visually similar)
- Different DOM element / accessibility role
- Behavior fundamentally changes (not just visual)
- Would require a boolean prop that changes core behavior (`isLink` on Button → separate)
- Example: `<Button>` and `<LinkButton>` (wraps an anchor tag)

### Shared base + specialized wrappers when:

- Several components share visual base but differ in behavior
- Example: BaseInput → TextInput, NumberInput, SearchInput

```tsx
// Shared base handles styling, focus, error states
function BaseInput({ className, ...props }: BaseInputProps) {
  return <input className={clsx('input-base', className)} {...props} />;
}

// Specialized wrappers add behavior
function NumberInput({ min, max, step, ...props }: NumberInputProps) {
  return <BaseInput type="number" min={min} max={max} step={step} {...props} />;
}

function SearchInput({ onSearch, ...props }: SearchInputProps) {
  return (
    <div className="search-input-wrapper">
      <BaseInput type="search" {...props} />
      <SearchIcon />
    </div>
  );
}
```

## Composition Patterns

Use the pattern highest on this list that meets the need. Move down only when the simpler option cannot work.

### 1. children — Simple content projection

Use for primary content of the component. Most common pattern, start here.

```jsx
<Button>Submit</Button>
<Card><CardContent>...</CardContent></Card>
```

### 2. Compound components — Multi-part tightly coupled UI

Use when the component has 3+ semantic sections that must work together. The parent manages shared state; children consume it via context.

```jsx
<Tabs>
  <TabList>
    <Tab>One</Tab>
    <Tab>Two</Tab>
  </TabList>
  <TabPanel>Content 1</TabPanel>
  <TabPanel>Content 2</TabPanel>
</Tabs>
```

When to use: Tabs, Accordion, Menu, Select, Dialog (header/body/footer)

```tsx
// Implementation skeleton
const TabsContext = React.createContext<TabsContextValue | null>(null);

function Tabs({ children, defaultIndex = 0 }: TabsProps) {
  const [activeIndex, setActiveIndex] = React.useState(defaultIndex);
  return (
    <TabsContext.Provider value={{ activeIndex, setActiveIndex }}>
      <div role="tablist">{children}</div>
    </TabsContext.Provider>
  );
}

function Tab({ children, index }: TabProps) {
  const { activeIndex, setActiveIndex } = useTabsContext();
  return (
    <button
      role="tab"
      aria-selected={activeIndex === index}
      onClick={() => setActiveIndex(index)}
    >
      {children}
    </button>
  );
}
```

### 3. Render props / slots — Caller-controlled rendering

Use when one section of the component needs full customization that cannot be achieved with children alone.

```jsx
<Autocomplete
  renderOption={(option) => (
    <div className="option">
      <Avatar src={option.avatar} />
      <span>{option.label}</span>
    </div>
  )}
/>

<Table
  columns={columns}
  renderCell={(column, row) => {
    if (column.key === 'status') return <StatusBadge status={row.status} />;
    return row[column.key];
  }}
/>
```

### 4. Higher-order components — Cross-cutting concerns only

Prefer hooks or composition over HOCs in modern React. Rarely appropriate for UI kit components. If you reach for an HOC, consider whether a hook or wrapper component would work instead.

## Separation Signals

Watch for these signs that a component needs splitting:

- Component has 2+ distinct responsibilities → split
- A prop is a boolean that changes fundamental behavior → two components
- Too many conditional branches based on a `type` or `mode` prop → separate components with shared base
- File is > 300 lines → likely needs splitting
- Props have mutually exclusive groups (some only apply when mode="X") → separate

```tsx
// WRONG: boolean prop that changes fundamental behavior
<Input isTextArea />  // completely different DOM element, different API

// CORRECT: separate components
<Input />
<TextArea />

// WRONG: mode prop with mutually exclusive prop groups
<Picker mode="date" showTimeZone />    // showTimeZone only applies to mode="time"
<Picker mode="time" dateFormat="..." /> // dateFormat only applies to mode="date"

// CORRECT: separate components with shared base
<DatePicker dateFormat="..." />
<TimePicker showTimeZone />
```

## Shared vs Domain Component Boundary

### UI kit = visual primitives

Button, Input, Modal, Card, Table, Select, Tooltip, Badge, Avatar.

- NO business logic
- NO API calls
- NO specific data shapes
- NO application-specific context/state

```tsx
// CORRECT: generic, reusable
function Avatar({ src, alt, size = 'md', fallback }: AvatarProps) {
  return (
    <span className={clsx('avatar', `avatar-${size}`)}>
      {src ? <img src={src} alt={alt} /> : <span>{fallback}</span>}
    </span>
  );
}
```

### Domain components = business context

UserAvatar, OrderTable, PaymentForm. CAN depend on ui-kit. CAN contain business logic.

```tsx
// CORRECT: domain component uses ui-kit primitives
function UserAvatar({ userId }: { userId: string }) {
  const user = useUser(userId);
  return (
    <Avatar
      src={user.avatarUrl}
      alt={user.name}
      fallback={user.initials}
    />
  );
}
```

### Boundary rules

- Never put domain logic inside a ui-kit component. If a component needs fetch/state/context from a specific feature, it belongs at the domain level.
- A component can start as domain-specific and be promoted to shared if it becomes generic enough. Strip all domain assumptions before promoting.
- If two teams need the same component but with different data, that is a ui-kit component with a generic API. If only one team uses it with one data shape, it is a domain component.
