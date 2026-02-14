# Changelog - MetaScan Backend

Este arquivo registra mudanças notáveis no backend do MetaScan.

## [1.8.1] - 2026-02-14

### Adicionado
- **Accounts:** Endpoint `GET /api/users/` — listagem de usuários ativos (Gestor/Admin), resposta paginada; usado para dropdown de atribuição de conferente no frontend.

## [1.8.0] - 2026-02-14

### Adicionado
- **CavaleteViewSet:** Action `assign_user` — `POST /api/inventory/cavaletes/{id}/assign-user/` com body `{"user_id": <id>}`; apenas gestores; registra ação ASSIGN em CavaleteHistory.
- **CavaleteViewSet:** Filtro por status — parâmetro `?status=AVAILABLE|IN_PROGRESS|COMPLETED|BLOCKED` (DjangoFilterBackend).
- **CavaleteViewSet:** Busca por código — parâmetro `?search=...` (SearchFilter no campo `code`).

## [1.7.0] - 2026-02-14

### Adicionado
- **Criação Dinâmica de Slots:** Funcionalidade que permite criar slots automaticamente ao cadastrar um Cavalete.
- **API:** Campo `structure` (write-only) no endpoint de criação de cavalete (`POST /api/inventory/cavaletes/`).
- **Validação:** Rejeição de criação com estrutura zerada (`slots_a=0` e `slots_b=0`) se o campo `structure` for enviado.
- **Service:** Função `create_cavalete_structure` para geração em massa de slots.
- **Testes:** Validação da criação de cavalete com estrutura de slots.

### Alterado
- **Modelo Cavalete:** Substituído campo livre `name` por Enum `type` (`DEFAULT`, `PINE`) para melhor categorização.

## [1.6.0] - 2026-02-13

### Melhorado
- **Integridade de Dados:** Implementado `transaction.atomic` nos fluxos críticos do app `cavaletes` para garantir consistência entre operação e log.
- **Segurança:** Implementado Rate Limiting (Throttling) global e específico para integração Sankhya (60 req/min).
- **Testes:** Adicionados testes unitários para o modelo `User` (verificação de permissões por role) e permissões do app `inventory`.
- **Limpeza:** Removida configuração obsoleta `FIELD_ENCRYPTION_KEY`.
- **Qualidade:** Corrigidos warnings de lint e imports não utilizados.


### Adicionado
- **App Sankhya:** Implementado proxy para integração com ERP Sankhya (`apps.sankhya`).
- **Autenticação Sankhya:** Atualizado client para usar usuário de serviço global (`SANKHYA_USER`).
- **API:** Endpoint `GET /api/sankhya/products/<code>/` para consulta de detalhes do produto.
- **Configuração:** Variáveis de ambiente `SANKHYA_USER` e `SANKHYA_PASSWORD` adicionadas.
- **Testes:** Cobertura para client Sankhya (auth/product) e views do app proxy.

## [1.4.0] - 2026-02-13

### Adicionado
- **App Inventory:** Implementado app para histórico e auditoria (`apps.inventory`).
- **Modelos de Histórico:** `CavaleteHistory` e `SlotHistory` registram todas as ações.
- **Auditoria:** Logs automáticos de criação, atualização, exclusão e mudança de status.
- **Snapshots:** `SlotHistory` armazena valores anteriores e novos (produto/quantidade).
- **API:** Endpoints readonly para consulta de histórico (`api/inventory/history/...`).
- **Admin:** Visualização de histórico no Django Admin (readonly).

## [1.3.0] - 2026-02-13

### Adicionado
- **App Cavaletes:** Implementado app de domínio `cavaletes`.
- **Modelos:** `Cavalete` (com status e responsável) e `Slot` (com posições e produtos).
- **API:**
  - `CavaleteViewSet`: CRUD completo, filtro por usuário para conferentes.
  - `SlotViewSet`: Workflow de conferência (`start-confirmation`, `finish-confirmation`).
- **Validação:** Conferentes só podem editar slots com status `AUDITING`.
- **Testes:** Cobertura para Views, Permissões e Workflow de Slots.
- **Admin:** Interface administrativa com `SlotInline` para gestão facilitada.

## [1.2.0] - 2026-02-12

### Adicionado
- **Autenticação:** Modelo `CustomUser` implementado com campos `username`, `email` e `role`.
- **Roles:** Sistema de papéis (`ADMIN`, `MANAGER`, `AUDITOR`) para controle de acesso.
- **Admin:** Interface administrativa customizada para `CustomUser`.
- **Core:** Módulo de permissões (`IsAdmin`, `IsManager`, `IsAuditor`, `IsOwnerOrReadOnly`) em `apps/core/permissions.py`.
- **Core:** Módulo de mensagens centralizadas em `apps/core/messages.py`.

### Alterado
- `settings.py`: Configurado `AUTH_USER_MODEL = "accounts.User"`.
- `UserSerializer`: Atualizado para incluir e validar o campo `role`.

## [1.1.0] - 2026-01-26

### Adicionado
- `docker-compose.local.yml` para desenvolvimento local (PostgreSQL e Redis incluídos).
- `docker-compose.yml` atualizado para produção (PostgreSQL externo, bind mounts customizáveis).
- `docker-entrypoint.sh` melhorado com timeout de 60s, `collectstatic` e lógica aprimorada de superusuário.
- `Dockerfile` atualizado para usar Gunicorn como CMD padrão.
- `requirements.txt` com `gunicorn` e `whitenoise` adicionados.
- `Makefile` com comandos `docker-*-local` separados para desenvolvimento local e produção.
- `backlog-shared.md` como exemplo para projetos monorepo.
- Documentação sobre estrutura de backlog (standalone vs monorepo) em `docs/README.md`.

### Melhorado
- `settings.py`:
  - Database logic: prioriza PostgreSQL se variáveis estiverem definidas (não apenas em produção).
  - Cache Redis dinâmico: usa Redis se `REDIS_URL` estiver definido, senão LocMemCache.
  - `SECURE_SSL_REDIRECT` configurável via env var.
  - WhiteNoise middleware e storage adicionados.
- `.env.example` reorganizado com seções claras, valores vazios por padrão e novos campos:
  - `STATIC_ROOT_HOST` e `MEDIA_ROOT_HOST` para produção.
  - `GUNICORN_WORKERS` configurável.
  - `SECURE_SSL_REDIRECT` configurável.
- `README.md` reorganizado em 3 seções: Execução Nativa, Docker Local, Deploy.
- `ARCHITECTURE.md` atualizado com novas configurações Docker e variáveis de ambiente.
- `.gitignore` organizado com seções e comentários claros.
- `docs/CONTRIBUTING.md`:
  - Adicionadas seções de exemplos (bons e maus exemplos de commits).
  - Adicionadas seções "Corpo do Commit" e "Rodapé" com explicações detalhadas.
  - Adicionada seção "Fluxo de trabalho por card (recomendado)".
  - Adicionada seção "Convenções Adicionais" (Branches e Code Review).
  - Adicionada seção "Git Hooks (Opcional)".
  - Estrutura alinhada ao padrão estabelecido, mantendo conteúdo genérico.
- `docs/system/postman-guide.md`:
  - Adicionado `console.log` no script de automação de token.
  - Adicionada dica sobre "Inherit auth from parent".
  - Expandida seção "Observações Gerais" com formatação e detalhes.
- `docs/decisions/index.md`:
  - Expandidas decisões genéricas (Backend como fonte única, UUIDs, Timestamps).
  - Adicionadas novas decisões genéricas (Sincronização offline, Separação de responsabilidades).
- `docs/templates/planner-card.md`:
  - Estrutura alinhada ao padrão estabelecido.
  - Adicionado exemplo completo de card com todos os elementos.

### Removido
- Campo `roles` do `UserProfileSerializer` (específico de projetos com sistema de grupos).

## [1.0.2] - 2026-01-21

### Removido
- Pastas de cache `__pycache__` em testes.
- Pastas vazias `media/` e `static/`.

## [1.0.1] - 2026-01-21

### Adicionado
- Placeholders genéricos para `api-spec.md`, `data-model.md` e `business-rules.md`.

### Removido
- Artefatos locais (db, coverage, htmlcov, venv, caches).

## [1.0.0] - 2026-01-21

### Adicionado
- Estrutura de documentação base em `docs/` com padrão genérico.
- Guias iniciais de contribuição e Postman.
- Registro de decisões (ADR) e modelos de planejamento.

---

**Status:** Backend MetaScan (estrutura inicial a partir de base Django + DRF + JWT)
