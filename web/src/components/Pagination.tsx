import { Flex, Button, Text, IconButton, useColorModeValue } from '@chakra-ui/react';
import { FiChevronLeft, FiChevronRight } from 'react-icons/fi';

interface PaginationProps {
  currentPage: number;
  totalCount: number;
  pageSize: number;
  onPageChange: (page: number) => void;
}

/**
 * Componente de paginação simples.
 * Mostra botões Anterior/Próximo e a página atual.
 */
export const Pagination = ({
  currentPage,
  totalCount,
  pageSize,
  onPageChange,
}: PaginationProps) => {
  const totalPages = Math.ceil(totalCount / pageSize);
  const hasPrevious = currentPage > 1;
  const hasNext = currentPage < totalPages;

  if (totalPages <= 1) return null;

  return (
    <Flex align="center" justify="space-between" mt={4} px={2}>
      <Text fontSize="sm" color={useColorModeValue('gray.600', 'gray.400')}>
        Página <strong>{currentPage}</strong> de <strong>{totalPages}</strong> ({totalCount} itens)
      </Text>

      <Flex gap={2}>
        <IconButton
          aria-label="Página anterior"
          icon={<FiChevronLeft />}
          onClick={() => onPageChange(currentPage - 1)}
          isDisabled={!hasPrevious}
          size="sm"
          variant="outline"
        />
        <IconButton
          aria-label="Próxima página"
          icon={<FiChevronRight />}
          onClick={() => onPageChange(currentPage + 1)}
          isDisabled={!hasNext}
          size="sm"
          variant="outline"
        />
      </Flex>
    </Flex>
  );
};
