import { Box, Flex, Heading, Button, useDisclosure, Text, VStack } from '@chakra-ui/react';
import { FiPlus } from 'react-icons/fi';
import { CavaleteList } from '../components/CavaleteList';
import { CreateCavaleteModal } from '../components/CreateCavaleteModal';

/**
 * Página de Gestão de Cavaletes.
 * Lista todos os cavaletes e permite criar novos.
 */
export const CavaletesPage = () => {
  const { isOpen, onOpen, onClose } = useDisclosure();

  return (
    <Box>
      <Flex justify="space-between" align="center" mb={6}>
        <VStack align="start" spacing={1}>
          <Heading size="lg">Cavaletes</Heading>
          <Text color="gray.500" fontSize="sm">
            Gerencie os cavaletes e atribua conferentes.
          </Text>
        </VStack>
        <Button leftIcon={<FiPlus />} colorScheme="blue" onClick={onOpen}>
          Novo Cavalete
        </Button>
      </Flex>

      <CavaleteList />

      <CreateCavaleteModal isOpen={isOpen} onClose={onClose} />
    </Box>
  );
};
