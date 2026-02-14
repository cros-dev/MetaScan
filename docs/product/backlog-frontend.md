# Backlog Frontend - MetaScan

Este backlog foca exclusivamente nas tarefas do cliente web (React/Vite).

---

## Checkpoint atual (commit 0.5.0 — 2026-02-14)

**Entregue:** Lista de cavaletes com linha clicável para detalhes e botão "Atribuir"; a11y na tabela (`role="button"`, tabIndex, Enter/Space); modal de criação com overlay mais escuro, sem rótulo "Estrutura Inicial", cursor pointer no Select, tipagem do erro sem `any`; página placeholder Histórico (`HistoryPage`, Chakra) em `/inventory/history`; alinhamento às .cursor/rules (TypeScript estrito, JSDoc, feature-based). To-do de localização por rua registrado neste backlog, no backlog-backend e em `types.ts`. Detalhes em `web/CHANGELOG.md` (0.5.0).

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
- [ ] Filtros por Status (Disponível, Em Conferência, Concluído).
- [ ] Filtros/listagem por localização (rua do cavalete) — alinhar quando backend/cliente tiver ruas definidas.
- [x] Modal de Criação de Cavalete (com definição de estrutura e tipo).
- [ ] Detalhes do Cavalete (Visualização em Grade/Rack):
    - [ ] Componente `CavaleteGrid`: Renderiza Lado A e Lado B.
    - [ ] Componente `SlotCard`: Mostra estado (Vazio, Conferido) e produto.
- [ ] Atribuir Conferente (Dropdown de usuários).

### Próximos passos (pós-checkpoint)

Backend disponível: `POST .../cavaletes/{id}/assign-user/`, `?search=`, `?status=` (ver backlog-backend e CHANGELOG backend 1.8.0).

- [ ] **Modal de Atribuição de Conferente:** Abrir ao clicar em "Atribuir" na lista; dropdown de usuários (conferentes); chamar `POST .../assign-user/` com `user_id`; fechar e invalidar lista.
- [ ] **Busca por código de cavalete:** Campo de busca na tela; enviar `?search=...` na listagem.
- [ ] **Filtro por status:** Filtros (chips ou select) por Status; enviar `?status=AVAILABLE|IN_PROGRESS|COMPLETED|BLOCKED` na listagem.

## 4. Conferência (Epic 3)
- [ ] Tela "Meus Cavaletes" (Visão do Conferente).
- [ ] Workflow de Slot (Interação):
    - [ ] Drawer/Modal de Conferência ao clicar no SlotCard.
    - [ ] Integração com Leitor de Código de Barras (câmera ou input focado).
    - [ ] Feedback visual imediato (Slot fica verde após sucesso).

## 5. Histórico e Auditoria (Epic 4)
- [ ] Tela de Histórico de Cavaletes (Readonly).
- [ ] Visualização de Logs de Slot (Quem fez o quê).
