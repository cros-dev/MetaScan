/**
 * Interface para o perfil do usuário logado.
 */
export interface UserProfile {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  role: 'ADMIN' | 'MANAGER' | 'AUDITOR';
}
