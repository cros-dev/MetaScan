import { useState } from 'react';
import {
  Box,
  Table,
  Thead,
  Tbody,
  Tr,
  Th,
  Td,
  Text,
  Button,
  Input,
  InputGroup,
  InputLeftElement,
  Select,
  useColorModeValue,
  Skeleton,
  Stack,
  Flex,
} from '@chakra-ui/react';
import { useNavigate } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { FiSearch } from 'react-icons/fi';
import type { Cavalete } from '../types';
import { getCavaletes } from '../api/cavaletes';
import { StatusBadge } from './StatusBadge';
import { Pagination } from '@/components/Pagination';

/** Tamanho da página na listagem (alinhado ao backend). */
const CAVALETES_PAGE_SIZE = 20;

const STATUS_OPTIONS = [
  { value: '', label: 'Todos' },
  { value: 'AVAILABLE', label: 'Disponível' },
  { value: 'IN_PROGRESS', label: 'Em Conferência' },
  { value: 'COMPLETED', label: 'Concluído' },
  { value: 'BLOCKED', label: 'Bloqueado' },
] as const;

export interface CavaleteListProps {
  /** Chamado quando o usuário clica em Atribuir na linha (a página abre o modal). */
  onAssignClick?: (cavalete: Cavalete) => void;
}

/**
 * Lista de Cavaletes em formato de tabela com paginação, busca e filtro por status.
 * Apenas exibe dados e notifica eventos (ex.: onAssignClick); não possui modais.
 */
export const CavaleteList = ({ onAssignClick }: CavaleteListProps) => {
  const navigate = useNavigate();
  const [page, setPage] = useState(1);
  const [search, setSearch] = useState('');
  const [statusFilter, setStatusFilter] = useState('');

  const borderColor = useColorModeValue('gray.200', 'gray.700');
  const hoverBg = useColorModeValue('gray.200', 'gray.700');
  const headerBg = useColorModeValue('gray.50', 'gray.900');

  const { data, isLoading, isError } = useQuery({
    queryKey: ['cavaletes', page, search, statusFilter],
    queryFn: () =>
      getCavaletes({
        page,
        search: search.trim() || undefined,
        status: statusFilter || undefined,
      }),
    placeholderData: (previousData) => previousData,
  });

  const cavaletes = data?.results || [];
  const totalCount = data?.count || 0;

  if (isLoading) {
    return (
      <Box borderWidth="1px" borderRadius="lg" overflow="hidden" borderColor={borderColor}>
        <Table variant="simple">
          <Thead>
            <Tr>
              <Th>Código</Th>
              <Th>Tipo</Th>
              <Th>Status</Th>
              <Th>Responsável</Th>
              <Th>Ações</Th>
            </Tr>
          </Thead>
          <Tbody>
            {[1, 2, 3, 4, 5].map((i) => (
              <Tr key={i}>
                <Td><Skeleton height="20px" /></Td>
                <Td><Skeleton height="20px" /></Td>
                <Td><Skeleton height="20px" width="80px" /></Td>
                <Td><Skeleton height="20px" /></Td>
                <Td><Skeleton height="30px" width="60px" /></Td>
              </Tr>
            ))}
          </Tbody>
        </Table>
      </Box>
    );
  }

  if (isError) {
    return <Text color="red.500">Erro ao carregar cavaletes.</Text>;
  }

  if (cavaletes.length === 0) {
    return (
      <Box p={8} textAlign="center" borderWidth="1px" borderRadius="lg" borderColor={borderColor}>
        <Text color="gray.500">Nenhum cavalete encontrado.</Text>
      </Box>
    );
  }

  const handleSearchChange = (value: string) => {
    setSearch(value);
    setPage(1);
  };
  const handleStatusChange = (value: string) => {
    setStatusFilter(value);
    setPage(1);
  };

  return (
    <Stack spacing={4}>
      <Flex gap={4} flexWrap="wrap" align="center">
        <InputGroup maxW="xs">
          <InputLeftElement pointerEvents="none">
            <FiSearch color="gray" />
          </InputLeftElement>
          <Input
            placeholder="Buscar por código"
            value={search}
            onChange={(e) => handleSearchChange(e.target.value)}
          />
        </InputGroup>
        <Select
          w="fit-content"
          minW="180px"
          placeholder="Status"
          value={statusFilter}
          onChange={(e) => handleStatusChange(e.target.value)}
          cursor="pointer"
        >
          {STATUS_OPTIONS.map((opt) => (
            <option key={opt.value || 'all'} value={opt.value}>
              {opt.label}
            </option>
          ))}
        </Select>
      </Flex>

      <Box borderWidth="1px" borderRadius="lg" overflow="hidden" borderColor={borderColor}>
        <Table variant="simple">
          <Thead bg={headerBg}>
            <Tr>
              <Th>Código</Th>
              <Th>Tipo</Th>
              <Th>Status</Th>
              <Th>Responsável</Th>
              <Th>Ações</Th>
            </Tr>
          </Thead>
          <Tbody>
            {cavaletes.map((cavalete: Cavalete) => (
              <Tr
                key={cavalete.id}
                role="button"
                tabIndex={0}
                cursor="pointer"
                _hover={{ bg: hoverBg }}
                onClick={() => navigate(`/inventory/cavaletes/${cavalete.id}`)}
                onKeyDown={(e) => {
                  if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    navigate(`/inventory/cavaletes/${cavalete.id}`);
                  }
                }}
              >
                <Td fontWeight="medium">{cavalete.code}</Td>
                <Td>{cavalete.type === 'PINE' ? 'Pinheiro' : 'Padrão'}</Td>
                <Td>
                  <StatusBadge status={cavalete.status} />
                </Td>
                <Td>{cavalete.user_name || '-'}</Td>
                <Td onClick={(e) => e.stopPropagation()}>
                  <Button
                    size="sm"
                    colorScheme="blue"
                    variant="outline"
                    onClick={(e) => {
                      e.stopPropagation();
                      onAssignClick?.(cavalete);
                    }}
                  >
                    Atribuir
                  </Button>
                </Td>
              </Tr>
            ))}
          </Tbody>
        </Table>
      </Box>

      <Pagination
        currentPage={page}
        totalCount={totalCount}
        pageSize={CAVALETES_PAGE_SIZE}
        onPageChange={setPage}
      />
    </Stack>
  );
};
