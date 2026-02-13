import { Box, Drawer, DrawerContent, useDisclosure, useColorModeValue } from '@chakra-ui/react';
import { useState } from 'react';
import { Outlet } from 'react-router-dom';
import { SidebarContent } from './Sidebar';
import { Header } from './Header';
import { SIDEBAR_WIDTH_COLLAPSED, SIDEBAR_WIDTH_EXPANDED } from './constants';

/**
 * Layout principal da aplicação logada.
 * Gerencia a responsividade da Sidebar (Drawer no mobile, recolhível no desktop) e o Header.
 */
export const Layout = () => {
  const { isOpen, onOpen, onClose } = useDisclosure();
  const [isCollapsed, setIsCollapsed] = useState(false);

  const contentMl = { base: 0, md: isCollapsed ? SIDEBAR_WIDTH_COLLAPSED : SIDEBAR_WIDTH_EXPANDED };

  return (
    <Box minH="100vh" bg={useColorModeValue('gray.50', 'gray.900')}>
      {/* Sidebar Desktop */}
      <SidebarContent
        onClose={onClose}
        isCollapsed={isCollapsed}
        onToggleCollapse={() => setIsCollapsed((p) => !p)}
        display={{ base: 'none', md: 'block' }}
      />

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
      <Header onOpen={onOpen} ml={contentMl} />

      {/* Main Content */}
      <Box ml={contentMl} p="4">
        <Outlet />
      </Box>
    </Box>
  );
};
