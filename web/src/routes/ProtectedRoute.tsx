import { Navigate, Outlet, useLocation } from 'react-router-dom';

/**
 * Componente de proteção de rotas.
 * Verifica se o token existe no localStorage.
 * Se não existir, redireciona para o login salvando a localização tentada.
 */
export const ProtectedRoute = () => {
  const token = localStorage.getItem('metascan_token');
  const location = useLocation();

  if (!token) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  return <Outlet />;
};
