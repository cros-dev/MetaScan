import { useState } from 'react';
import { Box, Flex, Heading, Button, useDisclosure, Text, VStack } from '@chakra-ui/react';
import { FiPlus } from 'react-icons/fi';
import { CavaleteList } from '../components/CavaleteList';
import { CreateCavaleteModal } from '../components/CreateCavaleteModal';
import { AssignConferenteModal } from '../components/AssignConferenteModal';
import type { Cavalete } from '../types';

/**
 * Página de Gestão de Cavaletes.
 * Orquestra listagem, criação e atribuição de conferentes (donos dos modais).
 */
export const CavaletesPage = () => {
  const { isOpen, onOpen, onClose } = useDisclosure();
  const [assignCavalete, setAssignCavalete] = useState<{
    id: number;
    code: string;
  } | null>(null);

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

      <CavaleteList onAssignClick={(cavalete: Cavalete) => setAssignCavalete({ id: cavalete.id, code: cavalete.code })} />

      <CreateCavaleteModal isOpen={isOpen} onClose={onClose} />

      {assignCavalete && (
        <AssignConferenteModal
          isOpen={!!assignCavalete}
          onClose={() => setAssignCavalete(null)}
          cavaleteId={assignCavalete.id}
          cavaleteCode={assignCavalete.code}
        />
      )}
    </Box>
  );
};
