import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { useMutation } from '@tanstack/react-query';
import {
  Box,
  Button,
  FormControl,
  FormLabel,
  Input,
  FormErrorMessage,
  VStack,
  useToast,
  Text,
} from '@chakra-ui/react';
import { useNavigate } from 'react-router-dom';

import { loginSchema, type LoginCredentials, loginWithPassword } from '../api/login';

/**
 * Formulário de Login.
 * Gerencia validação, estado de loading e feedback de erro.
 */
export const LoginForm = () => {
  const toast = useToast();
  const navigate = useNavigate();

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<LoginCredentials>({
    resolver: zodResolver(loginSchema),
  });

  const mutation = useMutation({
    mutationFn: loginWithPassword,
    onSuccess: (data) => {
      localStorage.setItem('metascan_token', data.access);
      localStorage.setItem('metascan_refresh', data.refresh);
      
      toast({
        title: 'Login realizado com sucesso.',
        status: 'success',
        duration: 3000,
        isClosable: true,
      });

      navigate('/'); // Redireciona para Dashboard
    },
    onError: () => {
      toast({
        title: 'Erro ao entrar.',
        description: 'Verifique suas credenciais e tente novamente.',
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
    },
  });

  const onSubmit = (data: LoginCredentials) => {
    mutation.mutate(data);
  };

  return (
    <Box as="form" onSubmit={handleSubmit(onSubmit)} w="100%">
      <VStack spacing={4}>
        <FormControl isInvalid={!!errors.username} h="105px">
          <FormLabel>Usuário</FormLabel>
          <Input 
            type="text" 
            placeholder="Digite seu usuário" 
            {...register('username')} 
          />
          <FormErrorMessage>
            {errors.username && errors.username.message}
          </FormErrorMessage>
        </FormControl>

        <FormControl isInvalid={!!errors.password} h="105px">
          <FormLabel>Senha</FormLabel>
          <Input 
            type="password" 
            placeholder="Digite sua senha" 
            {...register('password')} 
          />
          <FormErrorMessage>
            {errors.password && errors.password.message}
          </FormErrorMessage>
        </FormControl>

        <Button
          type="submit"
          colorScheme="blue"
          width="full"
          isLoading={mutation.isPending}
          loadingText="Entrando..."
        >
          Entrar
        </Button>

        {mutation.isError && (
          <Text color="red.500" fontSize="sm">
            Falha na autenticação.
          </Text>
        )}
      </VStack>
    </Box>
  );
};
