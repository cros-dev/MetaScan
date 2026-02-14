import { Badge, type BadgeProps } from '@chakra-ui/react';
import type { CavaleteStatus } from '../types';

interface StatusBadgeProps extends BadgeProps {
  status: CavaleteStatus;
}

const statusMap: Record<CavaleteStatus, { label: string; color: string }> = {
  AVAILABLE: { label: 'Disponível', color: 'green' },
  IN_PROGRESS: { label: 'Em Conferência', color: 'yellow' },
  COMPLETED: { label: 'Concluído', color: 'blue' },
  BLOCKED: { label: 'Bloqueado', color: 'red' },
};

/**
 * Badge visual para status do Cavalete.
 */
export const StatusBadge = ({ status, ...rest }: StatusBadgeProps) => {
  const { label, color } = statusMap[status] || { label: status, color: 'gray' };

  return (
    <Badge colorScheme={color} px={2} py={1} borderRadius="md" {...rest}>
      {label}
    </Badge>
  );
};
