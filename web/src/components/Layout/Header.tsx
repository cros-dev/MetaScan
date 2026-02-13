import {
  Box,
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
import { useNavigate } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { getProfile } from '@/features/users/api/getProfile';

interface HeaderProps extends FlexProps {
  onOpen: () => void;
}

/**
 * Header (Barra Superior).
 * Contém o botão de menu (mobile) e o perfil do usuário.
 */
export const Header = ({ onOpen, ...rest }: HeaderProps) => {
  const navigate = useNavigate();
  const { colorMode, toggleColorMode } = useColorMode();

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
      ml={{ base: 0, md: 60 }}
      px={{ base: 4, md: 4 }}
      height="20"
      alignItems="center"
      bg={useColorModeValue('white', 'gray.900')}
      borderBottomWidth="1px"
      borderBottomColor={useColorModeValue('gray.200', 'gray.700')}
      justifyContent={{ base: 'space-between', md: 'flex-end' }}
      {...rest}
    >
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

      <HStack spacing={{ base: '0', md: '6' }}>
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
              bg={useColorModeValue('white', 'gray.800')}
              borderColor={useColorModeValue('gray.200', 'gray.700')}
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
              <MenuItem icon={<FiUser />} _hover={{ bg: useColorModeValue('gray.100', 'gray.700') }} bg="transparent">
                Perfil
              </MenuItem>
              <MenuDivider />
              <MenuItem icon={<FiLogOut />} onClick={handleLogout} _hover={{ bg: useColorModeValue('red.50', 'red.900'), color: 'red.500' }} bg="transparent">
                Sair
              </MenuItem>
            </MenuList>
          </Menu>
        </Flex>
      </HStack>
    </Flex>
  );
};
