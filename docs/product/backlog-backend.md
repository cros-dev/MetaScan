# Backlog - Backend MetaScan

Este arquivo contém o backlog do **backend** do MetaScan, organizado por épicos. Os cards de execução (tasks, bugs, code reviews) ficam no Planner ou nas Issues do repositório. Detalhes técnicos de implementação podem ser consultados em [../backend/ARCHITECTURE.md](../backend/ARCHITECTURE.md).

---

## Épico 0: Setup e configuração

### Objetivo

Preparar o ambiente do backend com variáveis de ambiente, dependências e configurações necessárias para o MetaScan (Sankhya, criptografia, timezone, CORS).

### Entregas principais

- `.env.example` com `FIELD_ENCRYPTION_KEY` e variáveis Sankhya (`SANKHYA_API_BASE_URL`, `SANKHYA_LOGIN_PATH`, `SANKHYA_APPKEY`, `SANKHYA_TOKEN`, `SANKHYA_PRODUTO_PATH`).
- `requirements.txt` com `requests` e `encrypted-model-fields`.
- `config/settings.py` com timezone America/Manaus (ou via env), CORS para Angular (ex.: `http://localhost:4200`).
- Documentação de referência (README/ARCHITECTURE) mencionando o que é o MetaScan.

### Dependências

Nenhuma.

### Status

Planejado

---

## Épico 1: Autenticação e usuários

### Objetivo

Implementar o modelo de usuário customizado (login por email, papéis, senha Sankhya criptografada), fluxo de autenticação JWT e gestão de usuários (CRUD, desativação/reativação, proteção do primeiro superuser).

### Entregas principais

- Modelo `CustomUser`: email como USERNAME_FIELD, role (admin/gestor/conferente), `sankhya_password` criptografada; lógica de save para is_staff/is_superuser e extração de nomes do email.
- Ajuste de serializers e views de accounts para o novo modelo (sem username, com role).
- Login por email em `POST /api/token/` (serializer customizado para TokenObtainPairView).
- Endpoint `GET /api/me/` retornando usuário logado (id, email, role, etc.).
- UserViewSet: CRUD de usuários (admin), actions deactivate e reactivate, proteção do primeiro superuser contra remoção e desativação.
- Migrações de accounts para CustomUser; `AUTH_USER_MODEL` e `encrypted_model_fields` configurados em settings.

### Dependências

Épico 0.

### Status

Planejado

---

## Épico 2: Autorização e core

### Objetivo

Aplicar as convenções e boas práticas em [ARCHITECTURE](../backend/ARCHITECTURE.md): choices nos modelos, mensagens em `messages.py`, permissões por papel em core.

### Entregas principais

- **Choices** nos modelos por app: accounts (ROLE_CHOICES); cavaletes (CAVALETE_*, SLOT_* em Cavalete/Slot); inventory (ACTION_CHOICES em histórico).
- **Mensagens:** `core/messages.py` para genéricas; cada app pode ter `messages.py` para seu domínio.
- **core:** `apps/core/permissions.py` com IsAdmin, IsManager, IsAuditor e IsOwnerOrReadOnly.

### Dependências

Épico 1 (depende de role no User).

### Status

Planejado

---

## Épico 3: Cavaletes e slots

### Objetivo

Implementar o domínio de cavaletes e slots: modelos, CRUD, exportação Excel, atribuição de usuários (single e bulk), workflow de conferência em 3 estados (disponível → em conferência → concluído).

### Entregas principais

- Seguir [ARCHITECTURE](../backend/ARCHITECTURE.md) (UniqueConstraint, related_name, Admin, validação no serializer).
- App `cavaletes`: modelos Cavalete (name, code, type, user FK, status) e Slot (cavalete FK, side, number, product_code, product_description, quantity, status); UniqueConstraint (cavalete, side, number); code/name no save(); slots conforme quantidade informada na requisição; registrar no Admin.
- CavaleteViewSet: CRUD, filtros, search, ordering; get_queryset por role (conferente só vê atribuídos); actions export (Excel), assign_user, assign (bulk).
- SlotViewSet: CRUD, filtros; regra “editar produto/quantidade só se status=auditing” no serializer; actions start_confirmation e finish_confirmation; opcional start_all/finish_all.
- Rotas em config/urls.py (cavaletes, slots).

### Dependências

Épico 2.

### Status

Planejado

---

## Épico 4: Histórico e auditoria

### Objetivo

Registrar e expor o histórico de ações em slots e cavaletes para rastreabilidade e auditoria.

### Entregas principais

- App `inventory`: modelos SlotHistory e CavaleteHistory (FKs para cavaletes.Slot e cavaletes.Cavalete, com related_name; campos: slot/cavalete, user, timestamp, action, etc.). Registrar no Admin.
- Helper ou service (`inventory/services.py`) que cria registros de histórico; views de cavaletes/slots chamam o helper (create, update, assign, start_confirmation, finish_confirmation).
- SlotHistoryViewSet e CavaleteHistoryViewSet: somente leitura, filtros e ordering.
- Rotas slot-history e cavalete-history em config/urls.py.

### Dependências

Épico 3.

### Status

Planejado

---

## Épico 5: Integração Sankhya

### Objetivo

Integrar o backend ao ERP Sankhya para consulta de produtos por código (validação e dados de estoque/descrição), com autenticação por usuário, cache de token e retry.

### Entregas principais

- App `sankhya`: serviços de auth (login, cache de token, refresh) e de produto (consulta por código, retry e timeout conforme ARCHITECTURE); endpoint GET /api/sankhya/products/<code>/; variáveis Sankhya no .env.example.

### Dependências

Épico 1 (usa usuário autenticado para obter token Sankhya).

### Status

Planejado

---

## Épico 6: Documentação e qualidade

### Objetivo

Documentar a API e o modelo de dados do MetaScan, consolidar regras de negócio na documentação e garantir cobertura de testes e qualidade de código (format, lint, test-cov).

### Entregas principais

- Atualizar `docs/system/api-spec.md`, `data-model.md` e `business-rules.md` com endpoints, modelos e regras do MetaScan.
- Testes: auth/me, CustomUser, cavaletes, slots (workflow), históricos, Sankhya (mock); `make format`, `make lint`, `make test-cov` passando.

### Dependências

Épicos 1 a 5 (documentar e testar o que foi implementado).

### Status

Planejado

---

## Observações

- Este backlog é de **produto** (o que entregar), não de execução técnica passo a passo.
- Para criar cards no Planner, use o [modelo de card](../templates/planner-card.md): relacione ao épico, defina critérios de aceite e checklist.
- A ordem de implementação sugerida segue as dependências (0 → 1 → 2 → 3 → 4; o Épico 5 pode ser desenvolvido em paralelo após o 1; o Épico 6 ao final).

---

**Última atualização:** 2026-02-09
