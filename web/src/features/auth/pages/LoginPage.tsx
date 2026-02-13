import { Box, Container, Heading, Text, VStack, useColorModeValue } from '@chakra-ui/react';
import { LoginForm } from '../components/LoginForm';

/**
 * Página de Login.
 * Exibe o layout centralizado com o formulário de autenticação.
 */
export const LoginPage = () => {
  const bg = useColorModeValue('gray.50', 'gray.800');
  const cardBg = useColorModeValue('white', 'gray.700');
  const titleColor = useColorModeValue('blue.600', 'blue.200');

  return (
    <Box 
      minH="100vh" 
      display="flex" 
      alignItems="center" 
      justifyContent="center" 
      bg={bg}
    >
      <Container maxW="md" bg={cardBg} p={8} borderRadius="lg" boxShadow="lg">
        <VStack spacing={6} mb={8}>
          <Heading as="h1" size="xl" color={titleColor}>
            MetaScan
          </Heading>
          <Text color="gray.500" textAlign="center">
            Sistema de Conferência de Estoque
          </Text>
        </VStack>
        
        <LoginForm />
      </Container>
    </Box>
  );
};
