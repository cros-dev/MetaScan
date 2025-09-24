import { User } from '../../users/models/user.model';
import { Product } from '../../products/models/product.model';

// Modelo para Slot
export interface Slot {
  id: number;
  cavalete: number;
  side: 'A' | 'B';
  number: number;
  product_code?: string;
  product_description?: string;
  quantity: number;
  status: 'available' | 'auditing' | 'awaiting_approval' | 'completed';
  location_code: string; // Campo adicionado pelo backend

  // Campos opcionais de produto (preenchidos quando produto é consultado)
  product_details?: Product;
}

// Modelo para Cavalete
export interface Cavalete {
  id: number;
  code: string;
  name: string;
  type: 'corredor' | 'torre';
  user?: User;
  status: 'available' | 'assigned' | 'inactive';
  slots: Slot[];
  occupancy: string; // Formato: "5/12 42%"
}

// Modelo para criação de cavalete
export interface CreateCavaleteRequest {
  type?: 'corredor' | 'torre';
}

// Modelo para atribuição de usuário
export interface AssignUserRequest {
  user_id?: number;
}

// Modelo para atribuição em massa
export interface AssignMassRequest {
  cavalete_ids: number[];
  user_id?: number;
}

// Modelo para filtros
export interface CavaleteFilters {
  status?: string;
  search?: string;
  ordering?: string;
}
