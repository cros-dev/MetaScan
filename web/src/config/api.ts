/**
 * Configuração global do Axios.
 * Inclui interceptors para JWT e tratamento de erros 401.
 */
import axios from 'axios';
import { env } from './env';

export const api = axios.create({
  baseURL: env.VITE_API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('metascan_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('metascan_token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);
