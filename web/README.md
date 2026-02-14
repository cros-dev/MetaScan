# MetaScan Web Frontend

Frontend do sistema MetaScan, construído com React, TypeScript, Vite e Chakra UI.

## Estrutura do Projeto

O projeto segue uma arquitetura orientada a features (Feature-based Architecture).

```
src/
├── assets/          # Imagens, ícones globais
├── components/      # Componentes UI genéricos (botões, layouts, modais)
│   ├── Layout/     # Layout logado: Layout, Sidebar (recolhível no desktop), Header (breadcrumb no desktop), constants
│   └── AppModal.tsx # Modal padrão do app (overlay escuro, centralizado)
├── config/          # Configurações globais (Axios, Theme, Env)
├── features/        # Módulos do domínio (Auth, Inventory, Users)
├── hooks/           # Hooks globais customizados
├── routes/          # Definição de rotas da aplicação
└── types/           # Tipagens TypeScript globais
```

## Stack Tecnológica

- **Core:** React 18, TypeScript, Vite
- **UI:** Chakra UI v2 (Componentes e Estilo)
- **State/Data:** TanStack Query (React Query)
- **Forms:** React Hook Form + Zod
- **Routing:** React Router DOM v6
- **HTTP:** Axios

## Pré-requisitos

- Node.js 18+
- Backend MetaScan rodando (para integração)

## Configuração

1. Clone o repositório.
2. Instale as dependências:
   ```bash
   cd web
   npm install
   ```
3. Crie o arquivo `.env` na raiz da pasta `web/` (copie de `.env.example` se existir):
   ```properties
   VITE_API_BASE_URL=http://localhost:8000/api
   ```

## Execução

### Desenvolvimento
```bash
npm run dev
```
O app estará disponível em `http://localhost:5173`.

### Build de Produção
```bash
npm run build
```
Os arquivos estáticos serão gerados na pasta `dist/`.

## Padrões de Código

Consulte `web/ARCHITECTURE.md` para detalhes sobre arquitetura, e mantenha os padrões de código definidos no projeto (Feature-based, Hooks, Zod).
