export interface Slot {
  id: number;
  cavalete: number;
  side: string;
  number: number;
  product_code: string | null;
  product_description: string | null;
  quantity: number;
  status: string;
}

export interface SlotListResponse {
  count: number;
  next: string | null;
  previous: string | null;
  results: Slot[];
}
