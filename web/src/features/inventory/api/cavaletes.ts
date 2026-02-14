import { api } from '@/config/api';
import type { Cavalete, CreateCavaletePayload, PaginatedResponse } from '../types';

/**
 * Busca a lista de cavaletes paginada.
 * Endpoint: GET /api/inventory/cavaletes/?page=X
 */
export const getCavaletes = async (page = 1): Promise<PaginatedResponse<Cavalete>> => {
  const response = await api.get<PaginatedResponse<Cavalete>>('/inventory/cavaletes/', {
    params: { page },
  });
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
