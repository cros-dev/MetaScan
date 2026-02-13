import { Box, Drawer, DrawerContent, useDisclosure, useColorModeValue } from '@chakra-ui/react';
import { Outlet } from 'react-router-dom';
import { SidebarContent } from './Sidebar';
import { Header } from './Header';

/**
 * Layout principal da aplicação logada.
 * Gerencia a responsividade da Sidebar (Drawer no mobile) e o Header.
 */
export const Layout = () => {
  const { isOpen, onOpen, onClose } = useDisclosure();

  return (
    <Box minH="100vh" bg={useColorModeValue('gray.50', 'gray.900')}>
      {/* Sidebar Desktop */}
      <SidebarContent onClose={() => onClose} display={{ base: 'none', md: 'block' }} />

      {/* Sidebar Mobile */}
      <Drawer
        autoFocus={false}
        isOpen={isOpen}
        placement="left"
        onClose={onClose}
        returnFocusOnClose={false}
        onOverlayClick={onClose}
        size="full"
      >
        <DrawerContent>
          <SidebarContent onClose={onClose} />
        </DrawerContent>
      </Drawer>

      {/* Header */}
      <Header onOpen={onOpen} />

      {/* Main Content */}
      <Box ml={{ base: 0, md: 60 }} p="4">
        <Outlet />
      </Box>
    </Box>
  );
};
