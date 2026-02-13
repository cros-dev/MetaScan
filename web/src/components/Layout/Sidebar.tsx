import {
  Box,
  CloseButton,
  Flex,
  Icon,
  useColorModeValue,
  Text,
  type BoxProps,
  type FlexProps,
} from '@chakra-ui/react';
import { FiHome, FiBox, FiClock, FiUsers } from 'react-icons/fi';
import type { IconType } from 'react-icons';
import { useNavigate } from 'react-router-dom';

interface LinkItemProps {
  name: string;
  icon: IconType;
  path: string;
}

const LinkItems: Array<LinkItemProps> = [
  { name: 'Dashboard', icon: FiHome, path: '/' },
  { name: 'Cavaletes', icon: FiBox, path: '/inventory/cavaletes' },
  { name: 'Histórico', icon: FiClock, path: '/inventory/history' },
];

interface SidebarProps extends BoxProps {
  onClose: () => void;
}

/**
 * Sidebar de navegação.
 * Exibe os links principais do sistema.
 */
export const SidebarContent = ({ onClose, ...rest }: SidebarProps) => {
  const navigate = useNavigate();

  return (
    <Box
      transition="3s ease"
      bg={useColorModeValue('white', 'gray.900')}
      borderRight="1px"
      borderRightColor={useColorModeValue('gray.200', 'gray.700')}
      w={{ base: 'full', md: 60 }}
      pos="fixed"
      h="full"
      {...rest}
    >
      <Flex h="20" alignItems="center" mx="8" justifyContent="space-between">
        <Text fontSize="2xl" fontFamily="monospace" fontWeight="bold" color="blue.600">
          MetaScan
        </Text>
        <CloseButton display={{ base: 'flex', md: 'none' }} onClick={onClose} />
      </Flex>
      {LinkItems.map((link) => (
        <NavItem 
          key={link.name} 
          icon={link.icon} 
          onClick={() => {
            navigate(link.path);
            onClose();
          }}
        >
          {link.name}
        </NavItem>
      ))}
    </Box>
  );
};

interface NavItemProps extends FlexProps {
  icon: IconType;
  children: React.ReactNode;
}

const NavItem = ({ icon, children, ...rest }: NavItemProps) => {
  return (
    <Flex
      align="center"
      p="4"
      mx="4"
      borderRadius="lg"
      role="group"
      cursor="pointer"
      _hover={{
        bg: 'blue.400',
        color: 'white',
      }}
      {...rest}
    >
      {icon && (
        <Icon
          mr="4"
          fontSize="16"
          _groupHover={{
            color: 'white',
          }}
          as={icon}
        />
      )}
      {children}
    </Flex>
  );
};
