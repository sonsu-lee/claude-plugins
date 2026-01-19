# CSS Property Ordering

## RECESS Order Overview

RECESS (created by Bootstrap) provides a logical property ordering system that groups related properties together for maintainability.

## Property Categories

### 1. Positioning

Controls element placement in the document flow:

```css
.element {
  position: relative;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
  z-index: 1;
}
```

**Order within category:**
1. `position`
2. `top`
3. `right`
4. `bottom`
5. `left`
6. `z-index`

### 2. Display & Box Model

Controls layout behavior and dimensions:

```css
.element {
  /* Display */
  display: flex;
  flex-direction: column;
  flex-wrap: wrap;
  flex-grow: 1;
  flex-shrink: 0;
  flex-basis: auto;
  justify-content: center;
  align-items: center;
  align-content: stretch;
  gap: 16px;
  order: 1;

  /* Grid (if using grid) */
  grid-template-columns: 1fr 1fr;
  grid-template-rows: auto;
  grid-template-areas: "header header";
  grid-area: main;
  grid-column: 1 / 3;
  grid-row: 1;

  /* Box Model */
  width: 100%;
  min-width: 0;
  max-width: 100%;
  height: auto;
  min-height: 100px;
  max-height: 500px;
  margin: 16px;
  padding: 16px;
  box-sizing: border-box;
  overflow: hidden;
  overflow-x: auto;
  overflow-y: scroll;
}
```

**Order within category:**

Display properties:
1. `display`
2. `flex` / `flex-direction` / `flex-wrap` / `flex-flow`
3. `flex-grow` / `flex-shrink` / `flex-basis`
4. `justify-content` / `align-items` / `align-content`
5. `gap` / `row-gap` / `column-gap`
6. `order`

Grid properties:
1. `grid` / `grid-template` / `grid-template-columns` / `grid-template-rows`
2. `grid-template-areas` / `grid-area`
3. `grid-column` / `grid-row`

Box model:
1. `width` / `min-width` / `max-width`
2. `height` / `min-height` / `max-height`
3. `margin` (and sides)
4. `padding` (and sides)
5. `box-sizing`
6. `overflow` / `overflow-x` / `overflow-y`

### 3. Typography

Controls text appearance:

```css
.element {
  font-family: 'Inter', sans-serif;
  font-size: 16px;
  font-weight: 400;
  font-style: normal;
  font-variant: normal;
  line-height: 1.5;
  letter-spacing: 0.01em;
  text-align: left;
  text-decoration: none;
  text-transform: uppercase;
  text-overflow: ellipsis;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
  white-space: nowrap;
  word-break: break-word;
  word-wrap: break-word;
  color: #333333;
}
```

**Order within category:**
1. `font-family`
2. `font-size`
3. `font-weight`
4. `font-style`
5. `font-variant`
6. `line-height`
7. `letter-spacing`
8. `text-align`
9. `text-decoration`
10. `text-transform`
11. `text-overflow`
12. `text-shadow`
13. `white-space`
14. `word-break` / `word-wrap`
15. `color`

### 4. Visual

Controls appearance and decoration:

```css
.element {
  background: linear-gradient(to bottom, #fff, #f5f5f5);
  background-color: #ffffff;
  background-image: url('image.png');
  background-position: center;
  background-repeat: no-repeat;
  background-size: cover;
  border: 1px solid #dddddd;
  border-width: 1px;
  border-style: solid;
  border-color: #dddddd;
  border-radius: 8px;
  border-top-left-radius: 8px;
  outline: none;
  outline-offset: 2px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  opacity: 1;
  visibility: visible;
  cursor: pointer;
  pointer-events: auto;
  user-select: none;
}
```

**Order within category:**
1. `background` (shorthand and individual properties)
2. `border` (shorthand and individual properties)
3. `border-radius`
4. `outline` / `outline-offset`
5. `box-shadow`
6. `opacity`
7. `visibility`
8. `cursor`
9. `pointer-events`
10. `user-select`

### 5. Animation & Transform

Controls motion and transformation:

```css
.element {
  transform: translateX(10px) rotate(45deg);
  transform-origin: center;
  transition: all 0.2s ease-in-out;
  transition-property: opacity, transform;
  transition-duration: 0.2s;
  transition-timing-function: ease-in-out;
  transition-delay: 0s;
  animation: fadeIn 0.3s ease-in forwards;
  animation-name: fadeIn;
  animation-duration: 0.3s;
  animation-timing-function: ease-in;
  animation-delay: 0s;
  animation-iteration-count: 1;
  animation-direction: normal;
  animation-fill-mode: forwards;
  animation-play-state: running;
  will-change: transform;
}
```

**Order within category:**
1. `transform`
2. `transform-origin`
3. `transition` (shorthand and individual properties)
4. `animation` (shorthand and individual properties)
5. `will-change`

## Complete Order Reference

Full property order for reference:

```css
.element {
  /* 1. Positioning */
  position: relative;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
  z-index: 1;

  /* 2. Display & Box Model */
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 16px;
  width: 100%;
  height: auto;
  margin: 0;
  padding: 16px;

  /* 3. Typography */
  font-family: 'Inter', sans-serif;
  font-size: 16px;
  font-weight: 400;
  line-height: 1.5;
  color: #333333;

  /* 4. Visual */
  background-color: #ffffff;
  border: 1px solid #dddddd;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  opacity: 1;

  /* 5. Animation */
  transition: opacity 0.2s ease-in-out;
}
```

## Stylelint Configuration

Enforce RECESS order automatically:

```json
{
  "extends": [
    "stylelint-config-standard",
    "stylelint-config-recess-order"
  ]
}
```

Install dependencies:

```bash
npm install -D stylelint stylelint-config-standard stylelint-config-recess-order
```

## Common Patterns

### Card Component

```css
.card {
  /* Positioning */
  position: relative;

  /* Display & Box Model */
  display: flex;
  flex-direction: column;
  width: 100%;
  max-width: 400px;
  padding: 24px;

  /* Typography */
  font-size: 14px;
  color: #333333;

  /* Visual */
  background-color: #ffffff;
  border: 1px solid #eeeeee;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);

  /* Animation */
  transition: box-shadow 0.2s ease-in-out;
}
```

### Button Component

```css
.button {
  /* Display & Box Model */
  display: inline-flex;
  justify-content: center;
  align-items: center;
  gap: 8px;
  min-width: 100px;
  height: 40px;
  padding: 0 16px;

  /* Typography */
  font-family: inherit;
  font-size: 14px;
  font-weight: 500;
  line-height: 1;
  text-decoration: none;
  color: #ffffff;

  /* Visual */
  background-color: #0066cc;
  border: none;
  border-radius: 6px;
  cursor: pointer;

  /* Animation */
  transition: background-color 0.15s ease-in-out;
}
```

### Form Input

```css
.input {
  /* Display & Box Model */
  display: block;
  width: 100%;
  height: 44px;
  padding: 0 12px;

  /* Typography */
  font-family: inherit;
  font-size: 16px;
  line-height: 44px;
  color: #333333;

  /* Visual */
  background-color: #ffffff;
  border: 1px solid #dddddd;
  border-radius: 6px;

  /* Animation */
  transition: border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
}
```

## Shorthand vs Longhand

### Use Shorthand For

Box model properties when setting multiple values:

```css
/* Good - shorthand */
.element {
  margin: 16px 24px;
  padding: 8px 16px 8px 16px;
}

/* Verbose - avoid */
.element {
  margin-top: 16px;
  margin-right: 24px;
  margin-bottom: 16px;
  margin-left: 24px;
}
```

### Use Longhand For

When setting only one side:

```css
/* Good - single side */
.element {
  margin-bottom: 16px;
}

/* Unnecessary - shorthand for one value */
.element {
  margin: 0 0 16px 0;
}
```

Complex properties where shorthand hides values:

```css
/* Good - explicit values */
.element {
  background-color: #ffffff;
  background-image: url('bg.png');
  background-position: center top;
  background-repeat: no-repeat;
  background-size: cover;
}

/* Avoid - values hidden in shorthand */
.element {
  background: #ffffff url('bg.png') center top / cover no-repeat;
}
```

## Transition Property Specificity

Always specify explicit transition properties:

```css
/* Bad - transitions everything */
.card {
  transition: 0.2s;
}

/* Bad - 'all' can cause unexpected transitions */
.card {
  transition: all 0.2s;
}

/* Good - explicit property */
.card {
  transition: box-shadow 0.2s ease-in-out;
}

/* Good - multiple properties */
.card {
  transition:
    box-shadow 0.2s ease-in-out,
    transform 0.2s ease-in-out;
}
```

## Why Order Matters

1. **Predictability** - Developers know where to find properties
2. **Merge conflicts** - Reduced when teams follow same order
3. **Code review** - Easier to spot missing or duplicate properties
4. **Maintenance** - Faster to update related properties together
5. **Mental model** - Matches how CSS cascade works conceptually
