# Frontend Conventions Plugin

React/TypeScript/CSS frontend development conventions focusing on **code style and structure**.

This plugin complements `vercel-react-best-practices` (performance optimization) by focusing on coding conventions and patterns.

## Skills

| Skill | Description |
|-------|-------------|
| **typescript-conventions** | Naming patterns, type system patterns, prohibited patterns (enum, default export, namespace, any, interface) |
| **react-component-conventions** | Component structure, props patterns, hooks patterns, JSX patterns |
| **css-styling-conventions** | Selector patterns, property ordering (RECESS), layout patterns, accessibility |
| **project-structure** | Application structure, component organization |
| **testing-patterns** | Vitest, React Testing Library, MSW patterns |
| **state-management** | Constate patterns, React Context usage |
| **storybook-patterns** | Story writing patterns, component documentation |

## Agents

| Agent | Trigger | Description |
|-------|---------|-------------|
| **code-reviewer** | "review code", "check conventions" | Reviews code for convention violations |
| **component-scaffolder** | "create component", "scaffold component" | Generates convention-compliant components |

## Commands

| Command | Description |
|---------|-------------|
| `/frontend-review [path]` | Review code for convention compliance |
| `/create-component [Name] [path] [--with-stories]` | Scaffold a new component |
| `/scaffold-feature [feature-name] [app-name]` | Generate feature structure |

## Role Division with vercel-react-best-practices

| Area | frontend-conventions | vercel-react-best-practices |
|------|---------------------|----------------------------|
| Naming | TypeScript/CSS naming | - |
| Types | Type system patterns | - |
| Structure | Component/project structure | - |
| Props | Naming, patterns | - |
| Hooks | Dependency array rules | Re-render optimization |
| Bundle | - | Dynamic imports, barrel files |
| Async | - | Waterfall prevention |
| Performance | - | Rendering optimization |

## Installation

### From GitHub

```bash
claude /install-plugin https://github.com/sonsu/claude-plugins/tree/main/frontend-conventions
```

### Local Development

```bash
claude --plugin-dir /path/to/frontend-conventions
```

## License

MIT
