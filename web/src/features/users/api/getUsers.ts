import { api } from '@/config/api';

export interface UserListItem {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  role: string;
}

/** Resposta paginada do DRF (quando paginação global está ativa). */
interface PaginatedUsersResponse {
  results?: UserListItem[];
  count?: number;
}

/**
 * Lista usuários ativos (Gestor/Admin). Usado para dropdown de atribuição.
 * Endpoint: GET /api/users/ (pode retornar array ou { results } se paginado).
 */
export const getUsers = async (): Promise<UserListItem[]> => {
  const response = await api.get<UserListItem[] | PaginatedUsersResponse>('/users/');
  const data = response.data;
  if (Array.isArray(data)) return data;
  return (data as PaginatedUsersResponse).results ?? [];
};
