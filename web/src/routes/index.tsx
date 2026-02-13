/**
 * Definição das rotas da aplicação.
 */
import { createBrowserRouter } from 'react-router-dom';

export const router = createBrowserRouter([
  {
    path: '/',
    element: <div>Dashboard (Em breve)</div>,
  },
  {
    path: '/login',
    element: <div>Login (Em breve)</div>,
  },
  {
    path: '*',
    element: <div>404 - Not Found</div>,
  },
]);
