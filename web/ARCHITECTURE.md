# Arquitetura do Frontend MetaScan

Este documento descreve a arquitetura do cliente web do **MetaScan**.

## Visão Geral

O frontend é uma Single Page Application (SPA) construída com **React** e **TypeScript**, servida pelo **Vite**. O design visual e componentes de UI são providos pelo **Chakra UI**.

A aplicação consome a API REST do backend (Django) para todas as operações de dados.

## Estrutura de Pastas (Feature-based)

Adotamos uma arquitetura onde o código é organizado por **funcionalidade (feature)**. Usamos o alias `@/` para imports absolutos a partir de `src/`.

```
src/
├── components/      # Componentes reutilizáveis (UI Kit interno)
│   └── Layout/     # Layout logado: Layout, Sidebar, Header, constants
├── config/          # Singletons e configurações (Axios, Theme)
├── features/        # Módulos de negócio
│   ├── auth/        # Login, Logout, Recuperação de Senha
│   │   ├── api/     # Funções de requisição (login, refresh)
│   │   ├── components/# Componentes específicos (LoginForm)
│   │   ├── pages/   # Páginas da feature (LoginPage)
│   │   └── types/   # Tipos locais (LoginCredentials)
│   ├── inventory/   # Gestão de Cavaletes e Conferência
│   └── ...
├── hooks/           # Hooks genéricos (useDebounce, useNotify)
├── routes/          # Configuração de rotas e rotas protegidas
└── App.tsx          # Ponto de entrada
```

## Gerenciamento de Estado

Temos duas categorias de estado:

1.  **Server State (Dados da API):** Gerenciado pelo **TanStack Query (React Query)**.
    -   Cache automático.
    -   Gerenciamento de loading/error states.
    -   Invalidação de cache após mutações.
    -   **NÃO** usar Redux ou Context API para armazenar dados que vêm do backend.

2.  **Client State (UI Local):**
    -   **Local:** `useState` (ex: abrir/fechar modal, input controlado).
    -   **Global:** `Context API` (apenas para temas, autenticação global, toast notifications).
    -   **Forms:** `React Hook Form` (gerencia estado de formulários complexos sem renderizações desnecessárias).

## Comunicação com Backend

-   **Cliente HTTP:** Axios.
-   **Configuração:** Instância única em `src/config/api.ts`.
-   **Configuração de Ambiente:** `src/config/env.ts` valida variáveis (`.env`) usando Zod antes do app iniciar.
-   **Interceptores:**
    -   **Request:** Injeta automaticamente o token JWT do LocalStorage no header `Authorization`.
    -   **Response:** Intercepta erros 401 (Unauthorized) para tentar refresh token ou deslogar o usuário.

## Roteamento

-   **React Router DOM v6**.
-   **Rotas Protegidas:** Componente `ProtectedRoute` verifica se há token válido. Se não, redireciona para `/login`.
-   **Lazy Loading:** Páginas principais carregadas via `React.lazy` para code splitting.

## Componentes e Hooks Globais

### Layout (`src/components/Layout/`)
- **Layout:** Wrapper para páginas logadas. Controla estado da sidebar (recolhida/expandida) e repassa `ml` (margem do conteúdo) para Header e área principal.
- **Sidebar:** Navegação lateral.
  - **Desktop (md+):** Fixa à esquerda, recolhível (só ícones) ou expandida (ícone + texto). Toggle no rodapé para expandir/recolher. Item da rota atual em destaque (azul); hover neutro (cinza) nos demais. Proporção do hover idêntica nos dois estados (constante `SIDEBAR_HORIZONTAL_INSET`).
  - **Mobile:** Drawer em tela cheia; botão hamburger no Header abre/fecha.
- **Header:** Barra superior com mesma altura que a área da logo (`BAR_HEIGHT`). Menu de usuário, avatar e toggle de tema; no mobile exibe hamburger e título MetaScan.
- **Constantes (`constants.ts`):** Dimensões centralizadas: `BAR_HEIGHT`, `SIDEBAR_WIDTH_EXPANDED`, `SIDEBAR_WIDTH_COLLAPSED`, `SIDEBAR_ICON_SIZE`, `SIDEBAR_FONT_SIZE`, `SIDEBAR_NAV_ITEM_H`, `SIDEBAR_HORIZONTAL_INSET`. Alterações de largura, altura dos itens ou recuo do hover devem ser feitas ali.

### Hooks Customizados
- **`useNotify`:** Wrapper sobre o `useToast` do Chakra. Garante consistência (posição `bottom-right`, duração 5s) e semântica (`notify.success`, `notify.error`).
- **`useProfile`:** Hook para buscar e cachear os dados do usuário logado via React Query.

## Estilização

-   **Chakra UI v2** como biblioteca de componentes base.
-   **Dark Mode:** Suporte nativo. Cores globais (`body bg`, `text`) definidas em `src/config/theme.ts`.
-   Estilização via **Props** (`<Box p={4} />`) para manter o CSS junto do componente.
-   Responsividade usando breakpoints de objeto/array: `width={{ base: "100%", md: "50%" }}`.
-   Tema customizado em `src/config/theme.ts` para cores da marca e fontes.

## Validação de Dados

-   **Zod** para definição de schemas (tipagem runtime + estática).
-   Integração com React Hook Form via `@hookform/resolvers/zod`.

## Testes

-   **Vitest** (Test Runner rápido compatível com Vite).
-   **React Testing Library** (Testes de componentes e integração).
