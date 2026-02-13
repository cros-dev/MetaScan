import { useToast, type UseToastOptions } from '@chakra-ui/react';

/**
 * Hook customizado para notificações (toasts).
 * Centraliza configurações padrão e simplifica o uso.
 */
export const useNotify = () => {
  const toast = useToast();

  const defaultOptions: UseToastOptions = {
    duration: 5000,
    isClosable: true,
    position: 'bottom-right',
    variant: 'subtle',
  };

  const notify = {
    success: (title: string, description?: string) => {
      toast({
        ...defaultOptions,
        title,
        description,
        status: 'success',
      });
    },
    error: (title: string, description?: string) => {
      toast({
        ...defaultOptions,
        title,
        description,
        status: 'error',
      });
    },
    warning: (title: string, description?: string) => {
      toast({
        ...defaultOptions,
        title,
        description,
        status: 'warning',
      });
    },
    info: (title: string, description?: string) => {
      toast({
        ...defaultOptions,
        title,
        description,
        status: 'info',
      });
    },
  };

  return notify;
};
