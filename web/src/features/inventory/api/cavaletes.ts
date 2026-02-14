import { api } from '@/config/api';
import type { Cavalete, CreateCavaletePayload, PaginatedResponse } from '../types';

/** Parâmetros de listagem de cavaletes (paginada, busca, status). */
export interface GetCavaletesParams {
  page?: number;
  search?: string;
  status?: string;
}

/**
 * Busca a lista de cavaletes paginada.
 * Endpoint: GET /api/inventory/cavaletes/?page=&search=&status=
 */
export const getCavaletes = async (
  params: GetCavaletesParams = {}
): Promise<PaginatedResponse<Cavalete>> => {
  const { page = 1, search, status } = params;
  const response = await api.get<PaginatedResponse<Cavalete>>('/inventory/cavaletes/', {
    params: { page, search, status },
  });
  return response.data;
};

/**
 * Atribui um conferente ao cavalete.
 * Endpoint: POST /api/inventory/cavaletes/{id}/assign-user/
 */
export const assignCavaleteUser = async (
  cavaleteId: number,
  userId: number
): Promise<Cavalete> => {
  const response = await api.post<Cavalete>(
    `/inventory/cavaletes/${cavaleteId}/assign-user/`,
    { user_id: userId }
  );
  return response.data;
};

/**
 * Cria um novo cavalete.
 * Endpoint: POST /api/inventory/cavaletes/
 */
export const createCavalete = async (data: CreateCavaletePayload): Promise<Cavalete> => {
  const response = await api.post<Cavalete>('/inventory/cavaletes/', data);
  return response.data;
};

/**
 * Busca detalhes de um cavalete específico.
 * Endpoint: GET /api/inventory/cavaletes/{id}/
 */
export const getCavaleteById = async (id: number): Promise<Cavalete> => {
  const response = await api.get<Cavalete>(`/inventory/cavaletes/${id}/`);
  return response.data;
};
