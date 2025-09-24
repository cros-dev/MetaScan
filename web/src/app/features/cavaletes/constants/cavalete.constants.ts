// Constantes para status de cavaletes
export const CAVALETE_STATUS = {
  AVAILABLE: 'available',
  ASSIGNED: 'assigned',
  INACTIVE: 'inactive'
} as const;

// Labels para status
export const CAVALETE_STATUS_LABELS: Record<string, string> = {
  [CAVALETE_STATUS.AVAILABLE]: 'Disponível',
  [CAVALETE_STATUS.ASSIGNED]: 'Atribuído',
  [CAVALETE_STATUS.INACTIVE]: 'Inativo'
};

// Classes CSS para status (usando variáveis CSS do tema)
export const CAVALETE_STATUS_CLASSES: Record<string, string> = {
  [CAVALETE_STATUS.AVAILABLE]: 'badge badge-success',
  [CAVALETE_STATUS.ASSIGNED]: 'badge badge-occupied',
  [CAVALETE_STATUS.INACTIVE]: 'badge badge-danger'
};

// Opções para filtros
export const STATUS_FILTER_OPTIONS = [
  { value: '', label: 'Todos os Status' },
  { value: CAVALETE_STATUS.AVAILABLE, label: CAVALETE_STATUS_LABELS[CAVALETE_STATUS.AVAILABLE] },
  { value: CAVALETE_STATUS.ASSIGNED, label: CAVALETE_STATUS_LABELS[CAVALETE_STATUS.ASSIGNED] },
  { value: CAVALETE_STATUS.INACTIVE, label: CAVALETE_STATUS_LABELS[CAVALETE_STATUS.INACTIVE] }
];
