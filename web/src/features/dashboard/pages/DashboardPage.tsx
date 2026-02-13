import { Box, Heading, Text, SimpleGrid, useColorModeValue } from '@chakra-ui/react';

/**
 * Página inicial (Dashboard).
 * Exibe resumo e atalhos.
 */
export const DashboardPage = () => {
  const cardBg = useColorModeValue('white', 'gray.700');

  return (
    <Box>
      <Heading mb={6}>Dashboard</Heading>
      <SimpleGrid columns={{ base: 1, md: 3 }} spacing={5}>
        <Box p={5} shadow="md" borderWidth="1px" borderRadius="lg" bg={cardBg}>
          <Heading fontSize="xl">Cavaletes</Heading>
          <Text mt={4}>Visão geral do inventário.</Text>
        </Box>
        <Box p={5} shadow="md" borderWidth="1px" borderRadius="lg" bg={cardBg}>
          <Heading fontSize="xl">Minhas Tarefas</Heading>
          <Text mt={4}>Cavaletes atribuídos a você.</Text>
        </Box>
        <Box p={5} shadow="md" borderWidth="1px" borderRadius="lg" bg={cardBg}>
          <Heading fontSize="xl">Histórico</Heading>
          <Text mt={4}>Últimas movimentações.</Text>
        </Box>
      </SimpleGrid>
    </Box>
  );
};
