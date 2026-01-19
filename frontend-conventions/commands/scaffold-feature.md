---
name: scaffold-feature
description: Create a complete feature structure in routes
arguments:
  - name: feature-name
    description: Feature name in kebab-case (e.g., user-management)
    required: true
  - name: --with-crud
    description: Include CRUD pages (list, detail, create, edit)
    required: false
  - name: --with-api
    description: Include API client and hooks
    required: false
---

# Scaffold Feature

Create a complete feature structure following the routes-based architecture.

## Process

1. **Validate name**: Ensure feature name is in kebab-case
2. **Create structure**: Generate feature directory with all required subdirectories
3. **Generate files**: Create base files for the feature
4. **Report structure**: Display created directory structure

## Feature Structure

Basic feature:
```
src/routes/[feature-name]/
├── components/           # Feature-specific components
├── hooks/               # Feature-specific hooks
├── types.ts             # Feature types
└── index.tsx            # Main page/entry
```

With `--with-crud`:
```
src/routes/[feature-name]/
├── components/
├── hooks/
├── types.ts
├── index.tsx            # List page
├── [id]/
│   └── index.tsx        # Detail page
├── create/
│   └── index.tsx        # Create page
└── [id]/edit/
    └── index.tsx        # Edit page
```

With `--with-api`:
```
src/api/[feature-name].ts  # API client functions
```
Plus hooks in `src/routes/[feature-name]/hooks/`:
- `useFeatures.ts` - List query hook
- `useFeature.ts` - Single item query hook
- `useCreateFeature.ts` - Create mutation hook
- `useUpdateFeature.ts` - Update mutation hook
- `useDeleteFeature.ts` - Delete mutation hook

## Generated Files

### types.ts
```tsx
export type FeatureName = {
  id: string;
  // Add properties
};

export type CreateFeatureNameInput = Omit<FeatureName, 'id'>;
export type UpdateFeatureNameInput = Partial<CreateFeatureNameInput>;
```

### index.tsx (List Page)
```tsx
export const FeatureNamePage = () => {
  return (
    <div>
      <h1>Feature Name</h1>
      {/* List content */}
    </div>
  );
};
```

## Examples

```
/scaffold-feature user-management
```
Creates basic user-management feature structure.

```
/scaffold-feature products --with-crud
```
Creates products feature with CRUD pages.

```
/scaffold-feature orders --with-crud --with-api
```
Creates orders feature with CRUD pages, API client, and React Query hooks.

## Conventions Applied

- kebab-case for directory names
- PascalCase for component names
- Routes use directory-based routing patterns
- Types defined per feature
- Hooks co-located with feature
- API clients in central `src/api/` directory
