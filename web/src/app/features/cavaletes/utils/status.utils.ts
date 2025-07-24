export const CAVALETE_STATUS_LABELS: Record<string, string> = {
  available: 'Disponível',
  assigned: 'Atribuído',
  inactive: 'Inativo'
};

export function getCavaleteStatusSeverity(status: string): string {
  switch (status) {
    case 'available': return 'success';
    case 'assigned': return 'info';
    case 'inactive': return 'secondary';
    default: return 'info';
  }
}
