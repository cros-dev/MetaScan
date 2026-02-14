# Backlog Frontend - MetaScan

Este backlog foca exclusivamente nas tarefas do cliente web (React/Vite).

---

## Checkpoint atual (commit 0.6.0 — 2026-02-14)

**Entregue:** Lista de cavaletes com linha clicável, botão "Atribuir", busca por código e filtro por status; modal de atribuição de conferente (RHF + Zod); modal de criação; AppModal reutilizável (overlay padronizado); CavaletesPage orquestra modais, CavaleteList apenas exibe e notifica; a11y na tabela; placeholder Histórico; tipos em `inventory/types.ts`; getUsers em `users/api`. To-do de localização por rua registrado. Detalhes em `web/CHANGELOG.md` (0.5.0 e 0.6.0).

---

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
- [x] Listagem de Cavaletes (`/inventory/cavaletes`).
- [x] Filtros por Status (Disponível, Em Conferência, Concluído, Bloqueado).
- [ ] Filtros/listagem por localização (rua do cavalete) — alinhar quando backend/cliente tiver ruas definidas.
- [x] Modal de Criação de Cavalete (com definição de estrutura e tipo).
- [ ] Detalhes do Cavalete (Visualização em Grade/Rack):
    - [ ] Componente `CavaleteGrid`: Renderiza Lado A e Lado B.
    - [ ] Componente `SlotCard`: Mostra estado (Vazio, Conferido) e produto.
- [x] Atribuir Conferente (Modal com dropdown de usuários; RHF + Zod; POST assign-user).
- [x] Busca por código e filtro por status na listagem (`?search=`, `?status=`).

## 4. Conferência (Epic 3)
- [ ] Tela "Meus Cavaletes" (Visão do Conferente).
- [ ] Workflow de Slot (Interação):
    - [ ] Drawer/Modal de Conferência ao clicar no SlotCard.
    - [ ] Integração com Leitor de Código de Barras (câmera ou input focado).
    - [ ] Feedback visual imediato (Slot fica verde após sucesso).

## 5. Histórico e Auditoria (Epic 4)
- [ ] Tela de Histórico de Cavaletes (Readonly).
- [ ] Visualização de Logs de Slot (Quem fez o quê).
