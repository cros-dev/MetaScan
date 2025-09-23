// Modelo unificado para Usuário
export interface User {
  id: number;
  first_name: string;
  last_name: string;
  email: string;
  role: 'admin' | 'manager' | 'auditor';
  is_active: boolean;
  created_at?: string;
  updated_at?: string;
}

// Modelo para criação de usuário
export interface CreateUserRequest {
  first_name: string;
  last_name: string;
  email: string;
  role: 'admin' | 'manager' | 'auditor';
  is_active?: boolean;
}

// Modelo para filtros de usuário
export interface UserFilters {
  role?: string;
  is_active?: boolean;
  search?: string;
}

// Modelo para resposta da API (com paginação)
export interface UserListResponse {
  results: User[];
  count: number;
}
