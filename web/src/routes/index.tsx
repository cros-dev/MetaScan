import { createBrowserRouter, Navigate } from 'react-router-dom';
import { LoginPage } from '@/features/auth/pages/LoginPage';
import { DashboardPage } from '@/features/dashboard/pages/DashboardPage';
import { CavaletesPage } from '@/features/inventory/pages/CavaletesPage';
import { HistoryPage } from '@/features/inventory/pages/HistoryPage';
import { ProtectedRoute } from './ProtectedRoute';
import { Layout } from '@/components/Layout/Layout';

/**
 * Definição das rotas da aplicação.
 * Organizada em rotas públicas (Login) e privadas (Dashboard).
 */
export const router = createBrowserRouter([
  {
    path: '/login',
    element: <LoginPage />,
  },
  {
    path: '/',
    element: <ProtectedRoute />,
    children: [
      {
        element: <Layout />,
        children: [
          {
            index: true,
            element: <DashboardPage />,
          },
          {
            path: 'inventory/cavaletes',
            element: <CavaletesPage />,
          },
          {
            path: 'inventory/history',
            element: <HistoryPage />,
          },
        ],
      },
    ],
  },
  {
    path: '*',
    element: <Navigate to="/" replace />,
  },
]);
