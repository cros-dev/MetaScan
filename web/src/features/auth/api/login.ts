import { z } from 'zod';
import { api } from '@/config/api';
import type { AuthResponse } from '../types';

/**
 * Schema de validação para o formulário de login.
 */
export const loginSchema = z.object({
  username: z.string().min(1, 'Usuário é obrigatório'),
  password: z.string().min(1, 'Senha é obrigatória'),
});

export type LoginCredentials = z.infer<typeof loginSchema>;

/**
 * Realiza o login do usuário via API.
 * @param data Credenciais (username, password)
 * @returns Tokens de acesso (access, refresh)
 */
export const loginWithPassword = async (data: LoginCredentials): Promise<AuthResponse> => {
  const response = await api.post<AuthResponse>('/token/', data);
  return response.data;
};
