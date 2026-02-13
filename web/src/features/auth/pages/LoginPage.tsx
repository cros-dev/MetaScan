import { Box, Container, Heading, Text, VStack } from '@chakra-ui/react';
import { LoginForm } from '../components/LoginForm';

/**
 * Página de Login.
 * Exibe o layout centralizado com o formulário de autenticação.
 */
export const LoginPage = () => {
  return (
    <Box 
      minH="100vh" 
      display="flex" 
      alignItems="center" 
      justifyContent="center" 
      bg="gray.50"
    >
      <Container maxW="md" bg="white" p={8} borderRadius="lg" boxShadow="lg">
        <VStack spacing={6} mb={8}>
          <Heading as="h1" size="xl" color="blue.600">
            MetaScan
          </Heading>
          <Text color="gray.600" textAlign="center">
            Sistema de Conferência de Estoque
          </Text>
        </VStack>
        
        <LoginForm />
      </Container>
    </Box>
  );
};
