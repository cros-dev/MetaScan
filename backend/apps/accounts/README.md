# App: Accounts

Gerencia autenticação e usuários do sistema.

## Modelos

### `User` (CustomUser)
Estende `AbstractUser` do Django.
- **username:** Login principal (matrícula ou nome curto).
- **email:** Opcional.
- **role:** Papel do usuário (`ADMIN`, `MANAGER`, `AUDITOR`).

## Roles e Permissões

- **ADMIN:** Acesso total (incluindo Django Admin e gerenciamento de usuários).
- **MANAGER:** Gestor. Pode criar/editar cavaletes e visualizar relatórios.
- **AUDITOR:** Conferente. Pode realizar conferência em cavaletes atribuídos a ele.

## Endpoints

- `POST /api/token/`: Obter token JWT (Login).
- `POST /api/token/refresh/`: Atualizar token.
- `GET /api/users/`: Listar usuários ativos (Gestor/Admin). Resposta paginada. Usado para dropdown de atribuição de cavalete.
- `GET /api/users/profile/`: Dados do usuário logado.
- `GET /api/users/<id>/`: Detalhes de um usuário por ID.
