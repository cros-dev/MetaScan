import { api } from '@/config/api';
import type { UserProfile } from '../types';

/**
 * Busca o perfil do usuário logado.
 * Endpoint: GET /api/users/profile/
 */
export const getProfile = async (): Promise<UserProfile> => {
  const response = await api.get<UserProfile>('/users/profile/');
  return response.data;
};
