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
  useColorModeValue,
  Skeleton,
  Stack,
} from '@chakra-ui/react';
import { useNavigate } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { getCavaletes } from '../api/cavaletes';
import { StatusBadge } from './StatusBadge';
import { Pagination } from '@/components/Pagination';

/**
 * Lista de Cavaletes em formato de tabela com paginação.
 */
export const CavaleteList = () => {
  const navigate = useNavigate();
  const [page, setPage] = useState(1);
  
  const borderColor = useColorModeValue('gray.200', 'gray.700');
  const hoverBg = useColorModeValue('gray.200', 'gray.700'); // mesmo estilo do toggle expandir/recolher do menu
  const headerBg = useColorModeValue('gray.50', 'gray.900');

  const { data, isLoading, isError } = useQuery({
    queryKey: ['cavaletes', page],
    queryFn: () => getCavaletes(page),
    placeholderData: (previousData) => previousData, // Mantém dados antigos enquanto carrega novos
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

  return (
    <Stack spacing={4}>
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
            {cavaletes.map((cavalete) => (
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
                      // TODO: abrir modal de atribuir conferente
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
        pageSize={20} // Padrão do backend
        onPageChange={setPage}
      />
    </Stack>
  );
};
