import {
  Box,
  Breadcrumb,
  BreadcrumbItem,
  BreadcrumbLink,
  Flex,
  IconButton,
  Text,
  HStack,
  Menu,
  MenuButton,
  Avatar,
  MenuList,
  MenuItem,
  MenuDivider,
  useColorModeValue,
  useColorMode,
  Skeleton,
  type FlexProps,
} from '@chakra-ui/react';
import { FiMenu, FiLogOut, FiMoon, FiSun, FiUser } from 'react-icons/fi';
import { useNavigate, useLocation, Link } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { getProfile } from '@/features/users/api/getProfile';
import { BAR_HEIGHT, SIDEBAR_WIDTH_EXPANDED } from './constants';

interface HeaderProps extends FlexProps {
  onOpen: () => void;
}

/**
 * Header (Barra Superior).
 * Breadcrumb à esquerda (desktop), menu/perfil à direita; no mobile: hamburger + título à esquerda.
 */
const ROUTE_LABELS: Record<string, string> = {
  '': 'Dashboard',
  inventory: 'Inventário',
  cavaletes: 'Cavaletes',
  history: 'Histórico',
};

export const Header = ({ onOpen, ...rest }: HeaderProps) => {
  const navigate = useNavigate();
  const location = useLocation();
  const { colorMode, toggleColorMode } = useColorMode();

  const bgColor = useColorModeValue('white', 'gray.900');
  const borderColor = useColorModeValue('gray.200', 'gray.700');
  const breadcrumbLinkColor = useColorModeValue('gray.600', 'gray.400');
  const menuListBg = useColorModeValue('white', 'gray.800');
  const menuItemHover = useColorModeValue('gray.100', 'gray.700');
  const logoutHover = useColorModeValue('red.50', 'red.900');

  const pathSegments = location.pathname.split('/').filter(Boolean);
  const isHome = pathSegments.length === 0;
  const breadcrumbItems = isHome
    ? [{ path: '/', label: ROUTE_LABELS[''] ?? 'Dashboard' }]
    : pathSegments.map((segment, i) => ({
        path: '/' + pathSegments.slice(0, i + 1).join('/'),
        label: ROUTE_LABELS[segment] ?? segment,
      }));

  const { data: user, isLoading } = useQuery({
    queryKey: ['profile'],
    queryFn: getProfile,
  });

  const handleLogout = () => {
    localStorage.removeItem('metascan_token');
    localStorage.removeItem('metascan_refresh');
    navigate('/login');
  };

  const displayName = user?.first_name || user?.username || 'Usuário';
  const displayRole = user?.role || 'Carregando...';

  return (
    <Flex
      ml={{ base: 0, md: SIDEBAR_WIDTH_EXPANDED }}
      px="4"
      height={BAR_HEIGHT}
      alignItems="center"
      bg={bgColor}
      borderBottomWidth="1px"
      borderBottomColor={borderColor}
      justifyContent="space-between"
      {...rest}
    >
      <HStack spacing={3} flex="1" minW={0}>
        <IconButton
          display={{ base: 'flex', md: 'none' }}
          onClick={onOpen}
          variant="outline"
          aria-label="open menu"
          icon={<FiMenu />}
        />
        <Text
          display={{ base: 'flex', md: 'none' }}
          fontSize="2xl"
          fontFamily="monospace"
          fontWeight="bold"
          color="blue.600"
        >
          MetaScan
        </Text>
        <Breadcrumb
          display={{ base: 'none', md: 'block' }}
          listProps={{ flexWrap: 'wrap', gap: 1 }}
          separator=">"
        >
          {breadcrumbItems.map((item, i) => {
            const isCurrent = i === breadcrumbItems.length - 1;
            return (
              <BreadcrumbItem key={item.path} isCurrentPage={isCurrent}>
                <BreadcrumbLink
                  {...(!isCurrent && { as: Link, to: item.path })}
                  isCurrentPage={isCurrent}
                  fontSize="sm"
                  color={isCurrent ? undefined : breadcrumbLinkColor}
                  fontWeight={isCurrent ? 'semibold' : 'normal'}
                >
                  {item.label}
                </BreadcrumbLink>
              </BreadcrumbItem>
            );
          })}
        </Breadcrumb>
      </HStack>

      <HStack spacing={{ base: '0', md: '6' }} flexShrink={0}>
        <IconButton
          size="lg"
          variant="ghost"
          aria-label="Toggle color mode"
          onClick={toggleColorMode}
          icon={colorMode === 'light' ? <FiMoon /> : <FiSun />}
        />
        <Flex alignItems={'center'}>
          <Menu>
            <MenuButton py={2} transition="all 0.3s" _focus={{ boxShadow: 'none' }}>
              <HStack>
                <Skeleton isLoaded={!isLoading}>
                  <Avatar
                    size={'sm'}
                    name={displayName}
                    src=""
                  />
                </Skeleton>
              </HStack>
            </MenuButton>
            <MenuList
              bg={menuListBg}
              borderColor={borderColor}
              boxShadow="lg"
            >
              <Box px={3} py={2}>
                <Skeleton isLoaded={!isLoading} minW="100px" mb={1}>
                  <Text fontWeight="bold" fontSize="sm">{displayName}</Text>
                </Skeleton>
                <Skeleton isLoaded={!isLoading} minW="80px">
                  <Text fontSize="xs" color="gray.500">
                    {displayRole}
                  </Text>
                </Skeleton>
              </Box>
              <MenuDivider />
              <MenuItem icon={<FiUser />} _hover={{ bg: menuItemHover }} bg="transparent">
                Perfil
              </MenuItem>
              <MenuDivider />
              <MenuItem icon={<FiLogOut />} onClick={handleLogout} _hover={{ bg: logoutHover, color: 'red.500' }} bg="transparent">
                Sair
              </MenuItem>
            </MenuList>
          </Menu>
        </Flex>
      </HStack>
    </Flex>
  );
};
