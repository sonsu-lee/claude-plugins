# Application Structure Examples

## Complete Project Structure

Full structure for a medium-to-large React application:

```
project-root/
├── public/
│   ├── favicon.ico
│   └── index.html
├── src/
│   ├── api/
│   │   ├── client.ts
│   │   ├── endpoints.ts
│   │   ├── auth/
│   │   │   ├── index.ts
│   │   │   └── types.ts
│   │   ├── users/
│   │   │   ├── index.ts
│   │   │   └── types.ts
│   │   └── products/
│   │       ├── index.ts
│   │       └── types.ts
│   ├── components/
│   │   ├── Button/
│   │   │   ├── index.tsx
│   │   │   ├── styles.module.css
│   │   │   └── index.stories.tsx
│   │   ├── Input/
│   │   ├── Modal/
│   │   ├── Card/
│   │   ├── Table/
│   │   └── Layout/
│   │       ├── Header/
│   │       ├── Sidebar/
│   │       └── Footer/
│   ├── constants/
│   │   ├── routes.ts
│   │   ├── config.ts
│   │   └── errorMessages.ts
│   ├── hooks/
│   │   ├── useDebounce.ts
│   │   ├── useLocalStorage.ts
│   │   ├── useMediaQuery.ts
│   │   └── useClickOutside.ts
│   ├── layouts/
│   │   ├── MainLayout/
│   │   │   ├── index.tsx
│   │   │   └── styles.module.css
│   │   ├── AuthLayout/
│   │   └── DashboardLayout/
│   ├── routes/
│   │   ├── index.tsx
│   │   ├── dashboard/
│   │   ├── users/
│   │   ├── products/
│   │   ├── settings/
│   │   └── auth/
│   ├── states/
│   │   ├── authState.ts
│   │   ├── themeState.ts
│   │   └── index.ts
│   ├── styles/
│   │   ├── global.css
│   │   ├── variables.css
│   │   └── reset.css
│   ├── types/
│   │   ├── user.ts
│   │   ├── product.ts
│   │   ├── api.ts
│   │   └── common.ts
│   ├── utils/
│   │   ├── format.ts
│   │   ├── validation.ts
│   │   ├── storage.ts
│   │   └── date.ts
│   ├── App.tsx
│   └── main.tsx
├── .eslintrc.js
├── .prettierrc
├── tsconfig.json
├── vite.config.ts
└── package.json
```

## Feature Route Structure

### Dashboard Feature

```
routes/dashboard/
├── index.tsx                    # Dashboard page component
├── styles.module.css           # Page-level styles
├── components/
│   ├── StatCard/
│   │   ├── index.tsx
│   │   └── styles.module.css
│   ├── RecentActivity/
│   │   ├── index.tsx
│   │   └── styles.module.css
│   ├── QuickActions/
│   │   ├── index.tsx
│   │   └── styles.module.css
│   └── Charts/
│       ├── RevenueChart/
│       │   ├── index.tsx
│       │   └── styles.module.css
│       └── UserGrowthChart/
│           ├── index.tsx
│           └── styles.module.css
└── hooks/
    ├── useDashboardStats.ts
    └── useRecentActivity.ts
```

### Users Feature with CRUD

```
routes/users/
├── index.tsx                    # User list page
├── styles.module.css
├── [userId]/
│   ├── index.tsx               # User detail page
│   ├── edit.tsx                # User edit page
│   └── styles.module.css
├── new.tsx                      # Create user page
├── components/
│   ├── UserTable/
│   │   ├── index.tsx
│   │   ├── styles.module.css
│   │   └── UserTableRow/
│   │       ├── index.tsx
│   │       └── styles.module.css
│   ├── UserForm/
│   │   ├── index.tsx
│   │   └── styles.module.css
│   ├── UserCard/
│   │   ├── index.tsx
│   │   └── styles.module.css
│   └── UserFilters/
│       ├── index.tsx
│       └── styles.module.css
├── hooks/
│   ├── useUsers.ts
│   ├── useUser.ts
│   └── useUserMutations.ts
└── types.ts                     # Feature-specific types
```

### Settings Feature with Sub-routes

```
routes/settings/
├── index.tsx                    # Settings landing/redirect
├── layout.tsx                   # Settings layout with navigation
├── styles.module.css
├── profile/
│   ├── index.tsx
│   └── styles.module.css
├── account/
│   ├── index.tsx
│   ├── styles.module.css
│   └── components/
│       ├── PasswordChange/
│       └── EmailChange/
├── notifications/
│   ├── index.tsx
│   └── styles.module.css
├── billing/
│   ├── index.tsx
│   ├── styles.module.css
│   └── components/
│       ├── PaymentMethods/
│       ├── BillingHistory/
│       └── PlanSelector/
└── components/
    └── SettingsNav/
        ├── index.tsx
        └── styles.module.css
```

### Auth Feature

```
routes/auth/
├── login/
│   ├── index.tsx
│   └── styles.module.css
├── register/
│   ├── index.tsx
│   └── styles.module.css
├── forgot-password/
│   ├── index.tsx
│   └── styles.module.css
├── reset-password/
│   ├── index.tsx
│   └── styles.module.css
├── components/
│   ├── AuthForm/
│   │   ├── index.tsx
│   │   └── styles.module.css
│   ├── SocialLogin/
│   │   ├── index.tsx
│   │   └── styles.module.css
│   └── AuthGuard/
│       └── index.tsx
└── hooks/
    ├── useLogin.ts
    └── useRegister.ts
```

## API Structure Examples

### Complete API Setup

```
api/
├── client.ts                    # HTTP client configuration
├── endpoints.ts                 # Endpoint constants
├── interceptors.ts             # Request/response interceptors
├── auth/
│   ├── index.ts
│   └── types.ts
├── users/
│   ├── index.ts
│   └── types.ts
├── products/
│   ├── index.ts
│   └── types.ts
└── orders/
    ├── index.ts
    └── types.ts
```

### API Client Implementation

```tsx
// api/client.ts
import axios from 'axios';

export const client = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add auth token to requests
client.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle errors globally
client.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized
      localStorage.removeItem('token');
      window.location.href = '/auth/login';
    }
    return Promise.reject(error);
  }
);
```

### Resource API Implementation

```tsx
// api/users/index.ts
import { client } from '../client';
import type { User, CreateUserInput, UpdateUserInput, UsersResponse } from './types';

export const usersApi = {
  getAll: async (params?: { page?: number; limit?: number }) => {
    const response = await client.get<UsersResponse>('/users', { params });
    return response.data;
  },

  getById: async (id: string) => {
    const response = await client.get<User>(`/users/${id}`);
    return response.data;
  },

  create: async (data: CreateUserInput) => {
    const response = await client.post<User>('/users', data);
    return response.data;
  },

  update: async (id: string, data: UpdateUserInput) => {
    const response = await client.patch<User>(`/users/${id}`, data);
    return response.data;
  },

  delete: async (id: string) => {
    await client.delete(`/users/${id}`);
  },
};
```

### API Types

```tsx
// api/users/types.ts
export type User = {
  id: string;
  email: string;
  name: string;
  role: 'admin' | 'user';
  createdAt: string;
  updatedAt: string;
};

export type CreateUserInput = {
  email: string;
  name: string;
  password: string;
  role?: 'admin' | 'user';
};

export type UpdateUserInput = Partial<Omit<CreateUserInput, 'password'>>;

export type UsersResponse = {
  data: User[];
  total: number;
  page: number;
  limit: number;
};
```

## State Management Structure

### Constate State Files

```
states/
├── authState.ts
├── themeState.ts
├── notificationState.ts
└── index.ts
```

### Auth State Implementation

```tsx
// states/authState.ts
import { useState, useCallback, useEffect } from 'react';
import constate from 'constate';
import { authApi } from '@/api/auth';
import type { User } from '@/types/user';

type AuthState = {
  user: User | null;
  isLoading: boolean;
  isAuthenticated: boolean;
};

function useAuthState() {
  const [state, setState] = useState<AuthState>({
    user: null,
    isLoading: true,
    isAuthenticated: false,
  });

  const login = useCallback(async (email: string, password: string) => {
    const { user, token } = await authApi.login({ email, password });
    localStorage.setItem('token', token);
    setState({ user, isLoading: false, isAuthenticated: true });
  }, []);

  const logout = useCallback(() => {
    localStorage.removeItem('token');
    setState({ user: null, isLoading: false, isAuthenticated: false });
  }, []);

  const checkAuth = useCallback(async () => {
    try {
      const user = await authApi.me();
      setState({ user, isLoading: false, isAuthenticated: true });
    } catch {
      setState({ user: null, isLoading: false, isAuthenticated: false });
    }
  }, []);

  useEffect(() => {
    checkAuth();
  }, [checkAuth]);

  return {
    ...state,
    login,
    logout,
    checkAuth,
  };
}

export const [AuthProvider, useAuth] = constate(useAuthState);
```

### Provider Setup

```tsx
// App.tsx
import { AuthProvider } from '@/states/authState';
import { ThemeProvider } from '@/states/themeState';
import { NotificationProvider } from '@/states/notificationState';
import { Router } from './routes';

export const App = () => (
  <AuthProvider>
    <ThemeProvider>
      <NotificationProvider>
        <Router />
      </NotificationProvider>
    </ThemeProvider>
  </AuthProvider>
);
```

## Layout Structure

### Main Layout

```tsx
// layouts/MainLayout/index.tsx
import { Outlet } from 'react-router-dom';
import { Header } from '@/components/Layout/Header';
import { Sidebar } from '@/components/Layout/Sidebar';
import { Footer } from '@/components/Layout/Footer';
import styles from './styles.module.css';

export const MainLayout = () => (
  <div className={styles.layout}>
    <Header />
    <div className={styles.body}>
      <Sidebar />
      <main className={styles.main}>
        <Outlet />
      </main>
    </div>
    <Footer />
  </div>
);
```

### Auth Layout

```tsx
// layouts/AuthLayout/index.tsx
import { Outlet, Navigate } from 'react-router-dom';
import { useAuth } from '@/states/authState';
import styles from './styles.module.css';

export const AuthLayout = () => {
  const { isAuthenticated, isLoading } = useAuth();

  if (isLoading) {
    return <div>Loading...</div>;
  }

  if (isAuthenticated) {
    return <Navigate to="/dashboard" replace />;
  }

  return (
    <div className={styles.layout}>
      <div className={styles.container}>
        <Outlet />
      </div>
    </div>
  );
};
```

## Route Configuration

### Router Setup

```tsx
// routes/index.tsx
import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import { MainLayout } from '@/layouts/MainLayout';
import { AuthLayout } from '@/layouts/AuthLayout';
import { AuthGuard } from './auth/components/AuthGuard';

const router = createBrowserRouter([
  {
    path: '/auth',
    element: <AuthLayout />,
    children: [
      { path: 'login', lazy: () => import('./auth/login') },
      { path: 'register', lazy: () => import('./auth/register') },
    ],
  },
  {
    path: '/',
    element: <AuthGuard><MainLayout /></AuthGuard>,
    children: [
      { index: true, lazy: () => import('./dashboard') },
      { path: 'users', lazy: () => import('./users') },
      { path: 'users/:userId', lazy: () => import('./users/[userId]') },
      { path: 'settings/*', lazy: () => import('./settings') },
    ],
  },
]);

export const Router = () => <RouterProvider router={router} />;
```

## Minimal Project Structure

For smaller projects or MVPs:

```
src/
├── components/
│   ├── Button/
│   ├── Input/
│   └── Modal/
├── pages/
│   ├── Home/
│   ├── About/
│   └── Contact/
├── hooks/
│   └── useApi.ts
├── utils/
│   └── api.ts
├── types/
│   └── index.ts
├── styles/
│   └── global.css
├── App.tsx
└── main.tsx
```

This structure works for:
- Small applications (< 10 pages)
- Prototypes and MVPs
- Learning projects

Scale up to the full structure when:
- Adding more features
- Multiple developers join
- Complex state management needed
- API layer grows
