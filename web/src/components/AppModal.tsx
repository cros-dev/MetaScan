import { Modal, ModalOverlay } from '@chakra-ui/react';

/** Overlay escuro padrão para todos os modais da aplicação. */
const MODAL_OVERLAY_BG = 'blackAlpha.900';

export interface AppModalProps {
  isOpen: boolean;
  onClose: () => void;
  children: React.ReactNode;
}

/**
 * Modal padrão do app: overlay escuro e centralizado.
 * Use com ModalContent, ModalHeader, ModalBody, ModalFooter do Chakra.
 */
export const AppModal = ({ isOpen, onClose, children }: AppModalProps) => (
  <Modal isOpen={isOpen} onClose={onClose} isCentered>
    <ModalOverlay bg={MODAL_OVERLAY_BG} />
    {children}
  </Modal>
);
