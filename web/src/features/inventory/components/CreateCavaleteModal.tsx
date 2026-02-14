import {
  ModalContent,
  ModalHeader,
  ModalFooter,
  ModalBody,
  ModalCloseButton,
  Button,
  FormControl,
  FormLabel,
  Input,
  Select,
  FormErrorMessage,
  VStack,
  HStack,
  NumberInput,
  NumberInputField,
  NumberInputStepper,
  NumberIncrementStepper,
  NumberDecrementStepper,
  Divider,
} from '@chakra-ui/react';
import { AppModal } from '@/components/AppModal';
import { useForm, Controller } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { createCavalete } from '../api/cavaletes';
import { useNotify } from '@/hooks/useNotify';

const createCavaleteSchema = z.object({
  code: z.string().min(1, 'Código é obrigatório'),
  type: z.enum(['DEFAULT', 'PINE'] as const),
  slots_a: z.number().min(0, 'Mínimo 0'),
  slots_b: z.number().min(0, 'Mínimo 0'),
});

type CreateCavaleteForm = z.infer<typeof createCavaleteSchema>;

/** Resposta de erro da API (ex.: Axios). */
interface ApiErrorResponse {
  response?: {
    data?: { structure?: string[]; detail?: string | string[] };
  };
}

/** Props do modal de criação de cavalete. */
interface CreateCavaleteModalProps {
  isOpen: boolean;
  onClose: () => void;
}

/**
 * Modal para criação de novos cavaletes.
 */
export const CreateCavaleteModal = ({ isOpen, onClose }: CreateCavaleteModalProps) => {
  const notify = useNotify();
  const queryClient = useQueryClient();

  const {
    register,
    handleSubmit,
    control,
    reset,
    formState: { errors, isValid },
  } = useForm<CreateCavaleteForm>({
    resolver: zodResolver(createCavaleteSchema),
    mode: 'onChange',
    defaultValues: {
      code: '',
      type: 'DEFAULT',
      slots_a: 0,
      slots_b: 0,
    },
  });

  const mutation = useMutation({
    mutationFn: (data: CreateCavaleteForm) => {
      return createCavalete({
        code: data.code,
        type: data.type,
        structure: {
          slots_a: data.slots_a,
          slots_b: data.slots_b,
        },
      });
    },
    onSuccess: () => {
      notify.success('Cavalete criado com sucesso!');
      queryClient.invalidateQueries({ queryKey: ['cavaletes'] });
      reset();
      onClose();
    },
    onError: (error: unknown) => {
      const data = (error as ApiErrorResponse)?.response?.data;
      const message =
        data?.structure?.[0] ??
        (Array.isArray(data?.detail) ? data.detail[0] : data?.detail) ??
        'Verifique os dados e tente novamente.';
      notify.error('Erro ao criar cavalete.', message);
    },
  });

  const onSubmit = (data: CreateCavaleteForm) => {
    mutation.mutate(data);
  };

  return (
    <AppModal isOpen={isOpen} onClose={onClose}>
      <ModalContent as="form" onSubmit={handleSubmit(onSubmit)}>
        <ModalHeader>Novo Cavalete</ModalHeader>
        <ModalCloseButton />
        
        <ModalBody>
          <VStack spacing={4}>
            <FormControl isInvalid={!!errors.code}>
              <FormLabel>Código</FormLabel>
              <Input 
                placeholder="Ex: CAV-001" 
                {...register('code')} 
              />
              <FormErrorMessage>
                {errors.code && errors.code.message}
              </FormErrorMessage>
            </FormControl>

            <FormControl isInvalid={!!errors.type}>
              <FormLabel>Tipo de Estrutura</FormLabel>
              <Select {...register('type')} cursor="pointer">
                <option value="DEFAULT">Padrão</option>
                <option value="PINE">Pinheiro</option>
              </Select>
              <FormErrorMessage>
                {errors.type && errors.type.message}
              </FormErrorMessage>
            </FormControl>

            <Divider />
            
            <VStack width="100%" align="start" spacing={3}>
              <HStack width="100%" spacing={4}>
                <FormControl isInvalid={!!errors.slots_a}>
                  <FormLabel fontSize="sm">Slots Lado A</FormLabel>
                  <Controller
                    control={control}
                    name="slots_a"
                    render={({ field }) => (
                      <NumberInput 
                        min={0} 
                        max={100} 
                        value={field.value} 
                        onChange={(_, val) => field.onChange(val)}
                      >
                        <NumberInputField />
                        <NumberInputStepper>
                          <NumberIncrementStepper />
                          <NumberDecrementStepper />
                        </NumberInputStepper>
                      </NumberInput>
                    )}
                  />
                  <FormErrorMessage>
                    {errors.slots_a && errors.slots_a.message}
                  </FormErrorMessage>
                </FormControl>

                <FormControl isInvalid={!!errors.slots_b}>
                  <FormLabel fontSize="sm">Slots Lado B</FormLabel>
                  <Controller
                    control={control}
                    name="slots_b"
                    render={({ field }) => (
                      <NumberInput 
                        min={0} 
                        max={100} 
                        value={field.value} 
                        onChange={(_, val) => field.onChange(val)}
                      >
                        <NumberInputField />
                        <NumberInputStepper>
                          <NumberIncrementStepper />
                          <NumberDecrementStepper />
                        </NumberInputStepper>
                      </NumberInput>
                    )}
                  />
                  <FormErrorMessage>
                    {errors.slots_b && errors.slots_b.message}
                  </FormErrorMessage>
                </FormControl>
              </HStack>
            </VStack>
          </VStack>
        </ModalBody>

        <ModalFooter>
          <Button variant="ghost" mr={3} onClick={onClose}>
            Cancelar
          </Button>
          <Button 
            colorScheme="blue" 
            type="submit" 
            isLoading={mutation.isPending}
            isDisabled={!isValid || mutation.isPending}
          >
            Criar
          </Button>
        </ModalFooter>
      </ModalContent>
    </AppModal>
  );
};
