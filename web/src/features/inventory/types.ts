/**
 * Resposta paginada genérica do Django Rest Framework.
 */
export interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

/**
 * Status possíveis de um Cavalete.
 */
export type CavaleteStatus = 'AVAILABLE' | 'IN_PROGRESS' | 'COMPLETED' | 'BLOCKED';

/**
 * Representação de um Slot dentro do Cavalete.
 */
export interface Slot {
  id: number;
  side: 'A' | 'B';
  number: number;
  product_code: string | null;
  product_description: string | null;
  quantity: number;
  status: 'AVAILABLE' | 'AUDITING' | 'COMPLETED';
}

/**
 * Tipos de Cavalete.
 */
export type CavaleteType = 'DEFAULT' | 'PINE';

/**
 * Representação completa de um Cavalete.
 * TODO: localização por rua — alinhar quando backend/cliente tiver ruas definidas (ver backlog).
 */
export interface Cavalete {
  id: number;
  code: string;
  type: CavaleteType;
  status: CavaleteStatus;
  user: number | null;
  user_name: string | null;
  slots: Slot[];
  created_at: string;
  updated_at: string;
}

/**
 * Payload para criação de um novo Cavalete.
 */
export interface CreateCavaletePayload {
  code: string;
  type: CavaleteType;
  structure?: {
    slots_a: number;
    slots_b: number;
  };
}
