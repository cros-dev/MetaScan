// Modelo para dados completos de produto do Sankhya
export interface Product {
  code: string;
  description: string;
  marca?: string;
  referencia_fornecedor?: string;
  localizacao?: string;
  data_inventario?: string;
  preco_base?: string;
  estoque?: string;
  unidade?: string;
}

// Modelo para resposta da API de produtos
export interface ProductResponse {
  code: string;
  description: string;
  marca?: string;
  referencia_fornecedor?: string;
  localizacao?: string;
  data_inventario?: string;
  preco_base?: string;
  estoque?: string;
  unidade?: string;
}
