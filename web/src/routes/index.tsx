/**
 * Definição das rotas da aplicação.
 */
import { createBrowserRouter, Navigate } from 'react-router-dom';
import { LoginPage } from '@/features/auth/pages/LoginPage';

export const router = createBrowserRouter([
  {
    path: '/',
    element: <div>Dashboard (Em breve) - <a href="/login">Ir para Login</a></div>,
  },
  {
    path: '/login',
    element: <LoginPage />,
  },
  {
    path: '*',
    element: <Navigate to="/" replace />,
  },
]);
