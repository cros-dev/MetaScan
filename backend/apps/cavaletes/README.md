# App: Cavaletes

Domínio principal do inventário: gestão de cavaletes e slots.

## Modelos

### `Cavalete`
Estrutura física que contém os produtos.
- **Status:** `AVAILABLE`, `IN_PROGRESS`, `COMPLETED`, `BLOCKED`.
- **User:** Conferente responsável.

### `Slot`
Posição no cavalete (Lado A/B + Número).
- **Status:** `AVAILABLE`, `AUDITING`, `COMPLETED`.
- **Dados:** Produto e quantidade conferidos.

## Workflow de Conferência

1. **Atribuição:** Gestor atribui cavalete a um Auditor.
2. **Início:** Auditor inicia conferência do slot (`start-confirmation`). Status -> `AUDITING`.
3. **Edição:** Auditor informa produto e quantidade (apenas se `AUDITING`).
4. **Fim:** Auditor finaliza conferência do slot (`finish-confirmation`). Status -> `COMPLETED`.

## Endpoints

- `/api/inventory/cavaletes/`: CRUD de cavaletes. Listagem: `?search=` (código), `?status=AVAILABLE|IN_PROGRESS|COMPLETED|BLOCKED`. Action: `POST .../cavaletes/{id}/assign-user/` (body `{"user_id": <id>}`) para atribuir conferente.
- `/api/inventory/slots/`: Gestão de slots e actions de workflow.
