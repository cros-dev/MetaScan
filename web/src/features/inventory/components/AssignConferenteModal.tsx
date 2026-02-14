import {
  ModalContent,
  ModalHeader,
  ModalFooter,
  ModalBody,
  ModalCloseButton,
  Button,
  FormControl,
  FormLabel,
  FormErrorMessage,
  Select,
  VStack,
  Skeleton,
  Text,
} from '@chakra-ui/react';
import { AppModal } from '@/components/AppModal';
import { useForm, Controller } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { getUsers } from '@/features/users/api/getUsers';
import { assignCavaleteUser } from '../api/cavaletes';
import { useNotify } from '@/hooks/useNotify';
import type { Cavalete, PaginatedResponse } from '../types';

/** Resposta de erro da API (ex.: assign-user). */
interface AssignErrorResponse {
  response?: { data?: { detail?: string } };
}

const assignConferenteSchema = z.object({
  user_id: z.string().min(1, 'Selecione um conferente'),
});

type AssignConferenteForm = z.infer<typeof assignConferenteSchema>;

/** Props do modal de atribuição de conferente ao cavalete. */
interface AssignConferenteModalProps {
  isOpen: boolean;
  onClose: () => void;
  cavaleteId: number;
  cavaleteCode: string;
}

/**
 * Modal para atribuir um conferente ao cavalete.
 * Usa React Hook Form + Zod (conforme convenções do projeto).
 */
export const AssignConferenteModal = ({
  isOpen,
  onClose,
  cavaleteId,
  cavaleteCode,
}: AssignConferenteModalProps) => {
  const notify = useNotify();
  const queryClient = useQueryClient();

  const {
    control,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm<AssignConferenteForm>({
    resolver: zodResolver(assignConferenteSchema),
    defaultValues: { user_id: '' },
  });

  const { data: usersData, isLoading: loadingUsers } = useQuery({
    queryKey: ['users'],
    queryFn: getUsers,
    enabled: isOpen,
  });
  const users = Array.isArray(usersData) ? usersData : [];

  const mutation = useMutation({
    mutationFn: (userId: number) => assignCavaleteUser(cavaleteId, userId),
    onSuccess: (updatedCavalete) => {
      // Atualiza o cache com o cavalete retornado pela API (feedback imediato na listagem).
      queryClient.setQueriesData(
        { queryKey: ['cavaletes'] },
        (old: PaginatedResponse<Cavalete> | undefined) => {
          if (!old?.results) return old;
          return {
            ...old,
            results: old.results.map((c) =>
              c.id === updatedCavalete.id ? updatedCavalete : c
            ),
          };
        }
      );
      queryClient.invalidateQueries({ queryKey: ['cavaletes'] }); // Refetch em background.
      notify.success('Conferente atribuído com sucesso.');
      reset();
      onClose();
    },
    onError: (error: unknown) => {
      const err = error as AssignErrorResponse;
      const message = err?.response?.data?.detail ?? 'Erro ao atribuir. Tente novamente.';
      notify.error('Erro ao atribuir conferente', message);
    },
  });

  const onSubmit = (data: AssignConferenteForm) => {
    mutation.mutate(Number(data.user_id));
  };

  return (
    <AppModal isOpen={isOpen} onClose={onClose}>
      <ModalContent as="form" onSubmit={handleSubmit(onSubmit)}>
        <ModalHeader>Atribuir conferente</ModalHeader>
        <ModalCloseButton />
        <ModalBody>
          <Text fontSize="sm" color="gray.500" mb={4}>
            Cavalete: <strong>{cavaleteCode}</strong>
          </Text>
          <VStack spacing={4}>
            <FormControl isInvalid={!!errors.user_id}>
              <FormLabel>Conferente</FormLabel>
              {loadingUsers ? (
                <Skeleton height="40px" borderRadius="md" />
              ) : (
                <Controller
                  name="user_id"
                  control={control}
                  render={({ field }) => (
                    <Select
                      {...field}
                      placeholder="Selecione o conferente"
                      cursor="pointer"
                      isDisabled={mutation.isPending}
                    >
                      {users.map((user) => (
                        <option key={user.id} value={user.id}>
                          {user.first_name || user.last_name
                            ? `${user.first_name} ${user.last_name}`.trim() || user.username
                            : user.username}
                        </option>
                      ))}
                    </Select>
                  )}
                />
              )}
              <FormErrorMessage>{errors.user_id?.message}</FormErrorMessage>
            </FormControl>
          </VStack>
        </ModalBody>
        <ModalFooter>
          <Button variant="ghost" mr={3} onClick={onClose} isDisabled={mutation.isPending}>
            Cancelar
          </Button>
          <Button
            colorScheme="blue"
            type="submit"
            isLoading={mutation.isPending}
            isDisabled={loadingUsers || users.length === 0}
          >
            Atribuir
          </Button>
        </ModalFooter>
      </ModalContent>
    </AppModal>
  );
};
