import {
  Box,
  CloseButton,
  Flex,
  Icon,
  Tooltip,
  useColorModeValue,
  Text,
  type BoxProps,
  type FlexProps,
} from '@chakra-ui/react';
import { FiHome, FiBox, FiClock, FiChevronLeft, FiChevronRight, FiPackage } from 'react-icons/fi';
import type { IconType } from 'react-icons';
import { useNavigate, useLocation } from 'react-router-dom';
import {
  BAR_HEIGHT,
  SIDEBAR_ICON_SIZE,
  SIDEBAR_FONT_SIZE,
  SIDEBAR_NAV_ITEM_H,
  SIDEBAR_WIDTH_COLLAPSED,
  SIDEBAR_WIDTH_EXPANDED,
  SIDEBAR_HORIZONTAL_INSET,
} from './constants';

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
  isCollapsed?: boolean;
  onToggleCollapse?: () => void;
}

/**
 * Sidebar de navegação.
 * No desktop pode ser recolhida (só ícones); no mobile é exibida em Drawer.
 */
export const SidebarContent = ({
  onClose,
  isCollapsed = false,
  onToggleCollapse,
  ...rest
}: SidebarProps) => {
  const navigate = useNavigate();
  const location = useLocation();
  const hoverBg = useColorModeValue('gray.200', 'gray.700');

  return (
    <Box
      transition="width 0.2s ease"
      bg={useColorModeValue('white', 'gray.900')}
      borderRight="1px"
      borderRightColor={useColorModeValue('gray.200', 'gray.700')}
      w={{ base: 'full', md: isCollapsed ? SIDEBAR_WIDTH_COLLAPSED : SIDEBAR_WIDTH_EXPANDED }}
      pos="fixed"
      top="0"
      left="0"
      bottom="0"
      display="flex"
      flexDirection="column"
      {...rest}
    >
      <Box
        flexShrink={0}
        h={BAR_HEIGHT}
        borderBottomWidth="1px"
        borderBottomColor={useColorModeValue('gray.200', 'gray.700')}
      >
        <Flex
          h="full"
          alignItems="center"
          mx={SIDEBAR_HORIZONTAL_INSET}
          justifyContent={isCollapsed ? 'center' : 'space-between'}
        >
          {isCollapsed ? (
            <Flex flex="1" justifyContent="center" alignItems="center">
              <Icon as={FiPackage} fontSize={SIDEBAR_ICON_SIZE} color="blue.600" />
            </Flex>
          ) : (
            <Flex alignItems="center" gap="3" overflow="hidden" flex="1" minW={0} pl="4">
              <Icon as={FiPackage} fontSize={SIDEBAR_ICON_SIZE} color="blue.600" flexShrink={0} />
              <Text fontSize="xl" fontFamily="monospace" fontWeight="extrabold" color="blue.600" whiteSpace="nowrap">
                MetaScan
              </Text>
            </Flex>
          )}
          <CloseButton display={{ base: 'flex', md: 'none' }} onClick={onClose} flexShrink={0} />
        </Flex>
      </Box>

      <Flex as="nav" flex="1" direction="column" py={2} pb={{ base: 2, md: 14 }} gap={1}>
        {LinkItems.map((link) => (
          <NavItem
            key={link.name}
            icon={link.icon}
            isCollapsed={isCollapsed}
            label={link.name}
            isSelected={location.pathname === link.path}
            hoverBg={hoverBg}
            onClick={() => {
              navigate(link.path);
              onClose();
            }}
          >
            {link.name}
          </NavItem>
        ))}
      </Flex>

      {onToggleCollapse && (
        <Flex
          position="absolute"
          bottom="0"
          left="0"
          right="0"
          pt="2"
          pb="2"
          px={SIDEBAR_HORIZONTAL_INSET}
          borderTopWidth="1px"
          borderColor={useColorModeValue('gray.200', 'gray.700')}
          bg={useColorModeValue('white', 'gray.900')}
          display={{ base: 'none', md: 'flex' }}
          justifyContent="center"
        >
          <Tooltip label={isCollapsed ? 'Expandir menu' : 'Recolher menu'} placement="right">
            <Flex
              as="button"
              type="button"
              aria-label={isCollapsed ? 'Expandir menu' : 'Recolher menu'}
              onClick={onToggleCollapse}
              align="center"
              justify="center"
              h={SIDEBAR_NAV_ITEM_H}
              minH={SIDEBAR_NAV_ITEM_H}
              py="0"
              px="4"
              borderRadius="lg"
              role="group"
              cursor="pointer"
              w="full"
              _hover={{ bg: hoverBg }}
            >
              <Icon
                as={isCollapsed ? FiChevronRight : FiChevronLeft}
                fontSize={SIDEBAR_ICON_SIZE}
              />
            </Flex>
          </Tooltip>
        </Flex>
      )}
    </Box>
  );
};

interface NavItemProps extends FlexProps {
  icon: IconType;
  children: React.ReactNode;
  isCollapsed?: boolean;
  label: string;
  isSelected?: boolean;
  hoverBg?: string;
}

const NavItem = ({
  icon,
  children,
  isCollapsed = false,
  label,
  isSelected = false,
  hoverBg = 'gray.200',
  ...rest
}: NavItemProps) => {
  const content = (
    <Flex
      align="center"
      h={SIDEBAR_NAV_ITEM_H}
      minH={SIDEBAR_NAV_ITEM_H}
      py="0"
      px="4"
      mx={SIDEBAR_HORIZONTAL_INSET}
      borderRadius="lg"
      role="group"
      cursor="pointer"
      justifyContent={isCollapsed ? 'center' : 'flex-start'}
      bg={isSelected ? 'blue.500' : undefined}
      color={isSelected ? 'white' : undefined}
      _hover={{
        bg: isSelected ? 'blue.500' : hoverBg,
      }}
      {...rest}
    >
      {icon && (
        <Icon
          mr={isCollapsed ? 0 : 4}
          fontSize={SIDEBAR_ICON_SIZE}
          flexShrink={0}
          color={isSelected ? 'white' : undefined}
          _groupHover={isSelected ? undefined : { color: 'inherit' }}
          as={icon}
        />
      )}
      <Text
        as="span"
        fontSize={SIDEBAR_FONT_SIZE}
        overflow="hidden"
        whiteSpace="nowrap"
        opacity={isCollapsed ? 0 : 1}
        w={isCollapsed ? 0 : 'auto'}
        transition="opacity 0.15s ease"
      >
        {children}
      </Text>
    </Flex>
  );

  if (isCollapsed) {
    return (
      <Tooltip label={label} placement="right">
        {content}
      </Tooltip>
    );
  }

  return content;
};
