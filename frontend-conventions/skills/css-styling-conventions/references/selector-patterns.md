# CSS Selector Patterns

## Naming Conventions

### camelCase for Class Names

```css
/* Good */
.buttonPrimary { }
.cardHeader { }
.userAvatar { }
.navigationMenu { }

/* Bad - kebab-case */
.button-primary { }
.card-header { }
.user-avatar { }
.navigation-menu { }
```

### Benefits in React/JSX

```tsx
// camelCase - clean property access
<div className={styles.cardHeader}>...</div>
<div className={clsx(styles.button, styles.buttonPrimary)}>...</div>

// kebab-case - requires bracket notation
<div className={styles['card-header']}>...</div>
<div className={clsx(styles['button'], styles['button-primary'])}>...</div>
```

## Specificity Management

### Keep Specificity Low

```css
/* Bad - high specificity, hard to override */
div.container article.post p.content {
  color: #333;
}

/* Good - single class */
.postContent {
  color: #333;
}
```

### Specificity Hierarchy

| Selector | Specificity |
|----------|-------------|
| `*` | 0 |
| `element` | 1 |
| `.class` | 10 |
| `[attribute]` | 10 |
| `#id` | 100 |
| `inline style` | 1000 |
| `!important` | ∞ |

### Avoid ID Selectors

```css
/* Bad - ID selector */
#mainHeader {
  background: #fff;
}

/* Good - class selector */
.mainHeader {
  background: #fff;
}
```

## Nesting Patterns

### Flat Structure (Default)

```css
/* Good - flat, independent selectors */
.card { }
.cardHeader { }
.cardTitle { }
.cardBody { }
.cardFooter { }
```

### When to Nest: Modifiers

```css
.button {
  padding: 8px 16px;
  background-color: #0066cc;
  color: white;

  /* Pseudo-classes */
  &:hover {
    background-color: #0052a3;
  }

  &:focus-visible {
    outline: 2px solid #0066cc;
    outline-offset: 2px;
  }

  &:active {
    background-color: #003d7a;
  }

  &:disabled {
    background-color: #cccccc;
    cursor: not-allowed;
  }

  /* Modifier classes */
  &.large {
    padding: 12px 24px;
    font-size: 18px;
  }

  &.secondary {
    background-color: #666666;
  }
}
```

### When to Nest: Strict HTML Relationships

Tables, lists, and other elements with strict parent-child requirements:

```css
/* Tables */
.dataTable {
  width: 100%;
  border-collapse: collapse;

  > thead {
    background-color: #f5f5f5;

    > tr > th {
      padding: 12px;
      text-align: left;
      font-weight: 600;
    }
  }

  > tbody > tr {
    border-bottom: 1px solid #ddd;

    > td {
      padding: 12px;
    }

    &:hover {
      background-color: #fafafa;
    }
  }
}

/* Lists */
.navigationList {
  display: flex;
  gap: 16px;

  > li {
    list-style: none;
  }
}

/* Definition lists */
.definitionList {
  > div {
    display: flex;
    padding: 8px 0;
    border-bottom: 1px solid #eee;

    > dt {
      width: 120px;
      font-weight: 500;
    }

    > dd {
      flex: 1;
    }
  }
}
```

### When NOT to Nest

```css
/* Bad - mirrors markup structure */
.page {
  .header {
    .logo { }
    .nav {
      .navItem {
        .navLink { }
      }
    }
  }
  .main {
    .sidebar { }
    .content { }
  }
}

/* Good - flat structure */
.page { }
.header { }
.logo { }
.nav { }
.navItem { }
.navLink { }
.main { }
.sidebar { }
.content { }
```

## Pseudo-Classes and Pseudo-Elements

### Use Pseudo-Classes for States

```css
.input {
  border: 1px solid #ddd;

  &:hover {
    border-color: #999;
  }

  &:focus {
    border-color: #0066cc;
    box-shadow: 0 0 0 3px rgba(0, 102, 204, 0.2);
  }

  &:disabled {
    background-color: #f5f5f5;
    cursor: not-allowed;
  }

  &::placeholder {
    color: #999;
  }
}
```

### Use ARIA Attributes for Semantic States

```css
/* Prefer ARIA over custom classes for state */
.button {
  /* Instead of .button.disabled */
  &:disabled {
    opacity: 0.5;
  }
}

.input {
  /* Instead of .input.invalid */
  &[aria-invalid="true"] {
    border-color: #cc0000;
  }
}

.accordion {
  .accordionIcon {
    transition: transform 0.2s;
  }

  /* Instead of .accordion.open */
  &[aria-expanded="true"] .accordionIcon {
    transform: rotate(180deg);
  }
}

.menu {
  display: none;

  /* Instead of .menu.visible */
  &[aria-hidden="false"] {
    display: block;
  }
}
```

## Parent-Child Dependencies

### Problem: Parent Styling Children

```css
/* Bad - parent controls child styles */
.parent {
  &:hover {
    .child {
      color: blue;
    }
  }
}
```

### Solution: Child Controls Its Own Styles

```css
/* Good - child controls its own styles based on parent */
.child {
  color: black;

  &:is(.parent:hover *) {
    color: blue;
  }
}
```

### :is() vs :where()

- `:is()` - Takes specificity of its most specific argument
- `:where()` - Always zero specificity

```css
/* :is() - higher specificity */
.child:is(.parent:hover *) {
  color: blue;  /* Same specificity as .parent:hover .child */
}

/* :where() - zero added specificity */
.child:where(.parent:hover *) {
  color: blue;  /* Same specificity as just .child */
}
```

## BEM Concepts in CSS Modules

### Block

```css
.card { }
.button { }
.modal { }
```

### Element

```css
.cardHeader { }
.cardBody { }
.cardFooter { }

.buttonIcon { }
.buttonText { }

.modalHeader { }
.modalContent { }
.modalFooter { }
```

### Modifier

```css
/* Using nested class modifier */
.button {
  &.primary { }
  &.secondary { }
  &.large { }
  &.small { }
}

/* Or using combined class names */
.buttonPrimary { }
.buttonSecondary { }
.buttonLarge { }
.buttonSmall { }
```

## Global vs Local Selectors

### CSS Modules Scope

```css
/* Local by default in CSS Modules */
.button {
  background: blue;
}

/* Global when needed */
:global(.external-class) {
  margin: 0;
}

/* Mix of local and global */
.container :global(.third-party-widget) {
  padding: 16px;
}
```

### Keyframe Naming

```css
/* Keyframes are local in CSS Modules */
.animatedElement {
  animation: fadeIn 0.3s ease-in;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}
```

## Selector Performance

### Selectors Read Right-to-Left

Browser reads `div.container article p` as:
1. Find all `p` elements
2. Filter to those inside `article`
3. Filter to those inside `div.container`

### Performance Tips

```css
/* Good - simple class selector */
.articleParagraph { }

/* Avoid - complex descendant */
div.container article.post p.content { }

/* Avoid - universal with descendant */
.container * { }
```

## Common Patterns

### Component Root

```css
.component {
  /* Layout */
  display: flex;
  flex-direction: column;

  /* Spacing */
  gap: 16px;
  padding: 16px;

  /* Visual */
  background: white;
  border-radius: 8px;
}
```

### Utility Modifier

```css
.visually-hidden {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}
```

### State Classes (When ARIA Doesn't Apply)

```css
.loading {
  position: relative;
  pointer-events: none;

  &::after {
    content: '';
    position: absolute;
    inset: 0;
    background: rgba(255, 255, 255, 0.8);
  }
}
```
