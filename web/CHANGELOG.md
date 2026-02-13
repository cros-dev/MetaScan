# Changelog - MetaScan Frontend

Este arquivo registra mudanças notáveis no frontend do MetaScan.

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
- Layout Base (Sidebar, Header).
- Dashboard e Gestão de Cavaletes.
