# Backlog Frontend - MetaScan

Este backlog foca exclusivamente nas tarefas do cliente web (React/Vite).

## 1. Setup & Fundação (Status: Concluído)
- [x] Inicializar projeto Vite + React + TS.
- [x] Configurar Chakra UI e Tema.
- [x] Configurar Axios e React Query.
- [x] Definir estrutura de pastas (Feature-based).
- [x] Implementar Layout Base (Sidebar recolhível no desktop, Drawer no mobile, Header responsivo com Breadcrumb, constantes em `Layout/constants.ts`).
- [x] Configurar Rotas Protegidas (AuthGuard).

## 2. Autenticação (Epic 1) (Status: Concluído)
- [x] Tela de Login (`/login`).
- [x] Integração com `POST /api/token/`.
- [x] Armazenamento de Token (LocalStorage) e Contexto de Auth.
- [x] Logout e Refresh Token automático (Interceptor - Logout básico implementado).

## 3. Gestão de Cavaletes (Epic 2)
- [ ] Listagem de Cavaletes (`/inventory/cavaletes`).
- [ ] Filtros por Status (Disponível, Em Conferência, Concluído).
- [ ] Modal de Criação de Cavalete.
- [ ] Detalhes do Cavalete (Visualizar Slots).
- [ ] Atribuir Conferente (Dropdown de usuários).

## 4. Conferência (Epic 3)
- [ ] Tela "Meus Cavaletes" (Visão do Conferente).
- [ ] Workflow de Slot:
    - [ ] Botão "Iniciar Conferência".
    - [ ] Input de Código de Barras (integração Sankhya).
    - [ ] Input de Quantidade.
    - [ ] Botão "Finalizar Conferência".

## 5. Histórico e Auditoria (Epic 4)
- [ ] Tela de Histórico de Cavaletes (Readonly).
- [ ] Visualização de Logs de Slot (Quem fez o quê).
