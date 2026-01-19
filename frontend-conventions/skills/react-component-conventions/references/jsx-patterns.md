# JSX Patterns

## Semantic HTML

### Why Semantic HTML Matters

- **Accessibility** - Screen readers understand page structure
- **SEO** - Search engines understand content hierarchy
- **Maintainability** - Clear intent in code
- **Developer Experience** - Self-documenting markup

### Common Semantic Elements

```tsx
// Document structure
<header>...</header>
<nav>...</nav>
<main>...</main>
<footer>...</footer>
<aside>...</aside>

// Content sections
<article>...</article>
<section>...</section>

// Text content
<h1>...<h6>
<p>...</p>
<blockquote>...</blockquote>
<figure><figcaption>...</figcaption></figure>

// Lists
<ul><li>...</li></ul>
<ol><li>...</li></ol>
<dl><dt>...</dt><dd>...</dd></dl>

// Interactive
<button>...</button>
<a href="...">...</a>
<form>...</form>
<input />
<select>...</select>
<textarea>...</textarea>

// Tables
<table>
  <thead><tr><th>...</th></tr></thead>
  <tbody><tr><td>...</td></tr></tbody>
</table>
```

### Choosing Elements

| Content Type | Element |
|-------------|---------|
| Main page navigation | `<nav>` |
| Page header with logo/title | `<header>` |
| Primary content | `<main>` |
| Standalone content (blog post) | `<article>` |
| Related content group | `<section>` |
| Sidebar content | `<aside>` |
| Page footer | `<footer>` |
| Clickable action | `<button>` |
| Navigation/link | `<a>` |

### Anti-Pattern: Div Soup

```tsx
// Bad - everything is a div
<div className="header">
  <div className="logo">Logo</div>
  <div className="nav">
    <div className="nav-item" onClick={handleHome}>Home</div>
    <div className="nav-item" onClick={handleAbout}>About</div>
  </div>
</div>

// Good - semantic elements
<header className="header">
  <h1 className="logo">Logo</h1>
  <nav className="nav">
    <a href="/" className="nav-item">Home</a>
    <a href="/about" className="nav-item">About</a>
  </nav>
</header>
```

## Clickable Elements

### Element Selection Rules

| Action | Element | Reason |
|--------|---------|--------|
| Navigate to page | `<a>` or `<Link>` | Right-click, ctrl+click support |
| Input field label | `<label>` | Associates with input, clickable |
| Form submission | `<button type="submit">` | Form submission semantics |
| Toggle/action | `<button type="button">` | Button semantics, keyboard support |

### Never Add onClick to Non-Interactive Elements

```tsx
// Bad - div is not interactive
<div onClick={handleClick} className="card">
  Click me
</div>

// Good - use button
<button onClick={handleClick} className="card">
  Click me
</button>

// If styling is an issue, reset button styles
<button
  onClick={handleClick}
  className="card"
  style={{ border: 'none', background: 'none', padding: 0 }}
>
  Click me
</button>
```

### Why Native Elements

Native clickable elements provide:
- Keyboard navigation (Tab, Enter, Space)
- Focus management
- Disabled state handling
- Accessible name
- Touch event handling
- Right-click menu (for links)

## Conditional Rendering

### Use Ternary, Not &&

```tsx
// Bad - can render '0', '', or other falsy values
{items.length && <ItemList items={items} />}
{message && <Message text={message} />}
{count && <Counter value={count} />}

// Good - explicit both branches
{items.length > 0 ? <ItemList items={items} /> : null}
{message ? <Message text={message} /> : null}
{count > 0 ? <Counter value={count} /> : null}
```

### Why This Happens

```tsx
const count = 0;

// && returns the first falsy value
{count && <span>Count: {count}</span>}
// Renders: 0

// Ternary is explicit
{count > 0 ? <span>Count: {count}</span> : null}
// Renders: nothing
```

### Return null for Empty

```tsx
// Good - null means "render nothing"
if (!user) {
  return null;
}

// Avoid - undefined is ambiguous
if (!user) {
  return undefined;
}

// Avoid - empty fragment has overhead
if (!user) {
  return <></>;
}
```

### Multiple Conditions

```tsx
// Complex conditions - extract to variable
const shouldShowBanner = isAuthenticated && hasPermission && !isDismissed;

return (
  <div>
    {shouldShowBanner ? <Banner /> : null}
  </div>
);

// Or use early return
if (!isAuthenticated) return <LoginPrompt />;
if (!hasPermission) return <AccessDenied />;
if (isDismissed) return null;

return <Banner />;
```

## Event Handlers

### Define as Variables

```tsx
// Bad - inline handler
<button onClick={(e) => {
  e.preventDefault();
  setCount(c => c + 1);
  trackClick('increment');
}}>
  Increment
</button>

// Good - named handler
const handleIncrement = (e: React.MouseEvent) => {
  e.preventDefault();
  setCount(c => c + 1);
  trackClick('increment');
};

<button onClick={handleIncrement}>
  Increment
</button>
```

### Acceptable Inline Cases

Simple, single-expression handlers are acceptable:

```tsx
// Acceptable - simple setter
<button onClick={() => setIsOpen(true)}>Open</button>

// Acceptable - simple toggle
<button onClick={() => setIsOpen(prev => !prev)}>Toggle</button>
```

### Handler Naming

```tsx
// Props use 'on' prefix
type Props = {
  onClick: () => void;
  onSubmit: (data: FormData) => void;
  onChange: (value: string) => void;
};

// Internal handlers use 'handle' prefix
const handleClick = () => { ... };
const handleSubmit = (data: FormData) => { ... };
const handleChange = (e: ChangeEvent) => { ... };
```

## Navigation

### Use Link Components

```tsx
// Bad - programmatic navigation for links
<div onClick={() => navigate('/dashboard')}>
  Go to Dashboard
</div>

// Good - proper link
<Link to="/dashboard">
  Go to Dashboard
</Link>

// External links
<a href="https://example.com" target="_blank" rel="noopener noreferrer">
  External Site
</a>
```

### Why Links Matter

Links provide:
- Right-click → Open in new tab
- Ctrl/Cmd+click → Open in new tab
- Middle-click → Open in new tab
- URL preview on hover
- History API integration
- Screen reader announcement

## Decorative vs Content

### CSS for Decorative Elements

```tsx
// Bad - decorative text in JSX
<span>※ Important note here</span>
<span>【 Section Title 】</span>

// Good - use CSS pseudo-elements
.note::before {
  content: '※ ';
}
<span className="note">Important note here</span>

.sectionTitle::before {
  content: '【 ';
}
.sectionTitle::after {
  content: ' 】';
}
<span className="sectionTitle">Section Title</span>
```

### When to Use Decorative Classes

- Prefix/suffix symbols (※, •, →)
- Quotation marks for styling
- Icons that don't convey meaning
- Purely visual separators

## Lists

### Key Prop

```tsx
// Good - unique, stable key
{items.map(item => (
  <ListItem key={item.id} item={item} />
))}

// Bad - index as key (causes issues with reordering)
{items.map((item, index) => (
  <ListItem key={index} item={item} />
))}
```

### When Index Key is OK

Only when:
- List is static (never reordered)
- Items have no stable IDs
- List is never filtered

```tsx
// Acceptable - static list
const menuItems = ['Home', 'About', 'Contact'];
{menuItems.map((item, index) => (
  <MenuItem key={index}>{item}</MenuItem>
))}
```

## Fragments

### When to Use

```tsx
// When returning multiple elements
return (
  <>
    <Header />
    <Main />
    <Footer />
  </>
);

// In loops/maps
{items.map(item => (
  <Fragment key={item.id}>
    <dt>{item.term}</dt>
    <dd>{item.definition}</dd>
  </Fragment>
))}
```

### Fragment with Key

```tsx
import { Fragment } from 'react';

// When key is needed, use Fragment not <>
{groups.map(group => (
  <Fragment key={group.id}>
    <GroupHeader group={group} />
    <GroupContent group={group} />
  </Fragment>
))}
```

## Forms

### Label Association

```tsx
// Good - htmlFor links to input
<label htmlFor="email">Email</label>
<input id="email" type="email" />

// Good - wrapping label (no htmlFor needed)
<label>
  Email
  <input type="email" />
</label>
```

### Controlled Inputs

```tsx
// Controlled input
const [email, setEmail] = useState('');

<input
  type="email"
  value={email}
  onChange={(e) => setEmail(e.target.value)}
/>
```

### Form Submission

```tsx
const handleSubmit = (e: React.FormEvent) => {
  e.preventDefault();
  // Handle submission
};

<form onSubmit={handleSubmit}>
  <input type="email" required />
  <button type="submit">Submit</button>
</form>
```

## Accessibility

### ARIA When Needed

Use WAI-ARIA when HTML semantics are insufficient:

```tsx
// Custom component needs ARIA
<div
  role="button"
  aria-pressed={isPressed}
  tabIndex={0}
  onKeyDown={handleKeyDown}
  onClick={handleClick}
>
  Toggle
</div>

// But prefer native element
<button
  aria-pressed={isPressed}
  onClick={handleClick}
>
  Toggle
</button>
```

### Common ARIA Patterns

```tsx
// Loading state
<button aria-busy={isLoading} disabled={isLoading}>
  {isLoading ? 'Saving...' : 'Save'}
</button>

// Expanded/collapsed
<button aria-expanded={isOpen} onClick={toggleMenu}>
  Menu
</button>

// Invalid input
<input
  aria-invalid={hasError}
  aria-describedby="email-error"
/>
{hasError && <span id="email-error">Invalid email</span>}

// Live region for updates
<div aria-live="polite">
  {statusMessage}
</div>
```

### Focus Management

```tsx
// Auto-focus on mount
const inputRef = useRef<HTMLInputElement>(null);

useEffect(() => {
  inputRef.current?.focus();
}, []);

<input ref={inputRef} />
```
