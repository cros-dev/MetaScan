# Changelog - MetaScan Frontend

Este arquivo registra mudanças notáveis no frontend do MetaScan.

## [0.5.0] - 2026-02-12

### Adicionado
- **Lista de Cavaletes:** Linha da tabela clicável para abrir detalhes do cavalete; botão "Atribuir" na coluna Ações (ação a implementar).
- **Acessibilidade:** Linha clicável com `role="button"`, `tabIndex={0}` e `onKeyDown` (Enter/Space) para navegação por teclado.
- **Rota Histórico:** Página placeholder `HistoryPage` (Chakra Box + Text) em `/inventory/history` em vez de `<div>`.

### Melhorado
- **Modal Novo Cavalete:** Overlay mais escuro; removido rótulo "Estrutura Inicial"; cursor `pointer` no Select "Tipo de Estrutura"; hover das linhas da tabela alinhado ao estilo do toggle do menu (`gray.200`/`gray.700`).
- **CreateCavaleteModal:** Tipagem do erro da mutation com `unknown` e interface `ApiErrorResponse` (sem `any`), em conformidade com as regras do projeto.
- **CavaleteList:** Removido `isPlaceholderData` não utilizado; consistência com .rules.

## [0.4.0] - 2026-02-13

### Adicionado
- **Breadcrumb no Header (desktop):** Gerado pela rota atual; separador `>`; links anteriores com cor suave, página atual em negrito. Na raiz exibe só "Dashboard"; em Cavaletes/Histórico exibe "Inventário > …" (sem Dashboard). Rótulos em `ROUTE_LABELS` no Header.

### Melhorado
- **Header:** Cores de tema extraídas em variáveis (`bgColor`, `borderColor`, etc.); `px` simplificado; docstring atualizada.

## [0.3.0] - 2026-02-13

### Adicionado
- **Sidebar recolhível (desktop):** Toggle no rodapé para expandir/recolher; modo recolhido exibe só ícones com Tooltip; ícone da logo (FiPackage) + texto "MetaScan" quando expandida.
- **Constantes de layout (`Layout/constants.ts`):** Centralização de dimensões: `BAR_HEIGHT`, `SIDEBAR_WIDTH_EXPANDED`, `SIDEBAR_WIDTH_COLLAPSED`, `SIDEBAR_ICON_SIZE`, `SIDEBAR_FONT_SIZE`, `SIDEBAR_NAV_ITEM_H`, `SIDEBAR_HORIZONTAL_INSET`.
- **Item selecionado vs hover:** Rota atual em destaque (azul); hover neutro (cinza) nos demais itens e no toggle; mesma proporção do hover recolhida e expandida (recuo em %).

### Melhorado
- **Layout:** Altura da barra (logo + header) alinhada entre Sidebar e Header; linhas divisórias contínuas; altura fixa dos itens de nav e do toggle nos dois estados.
- **Sidebar:** Larguras e recuos passam a usar constantes; Header usa `SIDEBAR_WIDTH_EXPANDED` no fallback de `ml`.
- **Header:** Altura reduzida via `BAR_HEIGHT` em constants (`'16'`).

## [0.2.0] - 2026-02-13

### Adicionado
- **Layout:** Estrutura base da aplicação logada (`DashboardLayout`).
  - Sidebar responsiva (Drawer no mobile, Fixa no desktop).
  - Header com menu de usuário, avatar e logout.
- **Tema:** Suporte completo a Dark Mode (botão de toggle no header).
  - Paleta de cores otimizada para contraste em ambos os modos.
  - Tipografia Inter via Google Fonts.
- **Dashboard:** Página inicial (`DashboardPage`) com cards de resumo.
- **Hooks:**
  - `useNotify`: Wrapper para toasts consistentes (bottom-right).
  - `useProfile`: Integração com API de perfil de usuário.
- **Rotas:** Configuração de rotas protegidas (`ProtectedRoute`) e estrutura aninhada.

## [0.1.0] - 2026-02-13

### Adicionado
- **Auth:** Feature de Login completa.
  - Tela de Login responsiva (`LoginPage`).
  - Formulário com validação Zod (`LoginForm`).
  - Integração com API (`POST /api/token/`).
  - Armazenamento de Token (LocalStorage) e redirecionamento.
- **Config:** Configuração de Alias (`@/`) e Variáveis de Ambiente (`.env`).
- **Setup:** Instalação inicial do projeto (Vite + React + TS + Chakra UI).

## [Unreleased]

### Planejado
- Dashboard e Gestão de Cavaletes (listagem, filtros, modal de criação).
