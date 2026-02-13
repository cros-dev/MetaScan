/**
 * Resposta da API de autenticação JWT.
 */
export interface AuthResponse {
  access: string;
  refresh: string;
}

/**
 * Representação do usuário no sistema.
 */
export interface User {
  id: number;
  username: string;
  email: string;
  role: 'ADMIN' | 'MANAGER' | 'AUDITOR';
}
