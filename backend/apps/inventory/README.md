# App: Inventory

Histórico e auditoria de ações no sistema.

## Responsabilidade
Registrar todas as alterações relevantes em cavaletes e slots para rastreabilidade.

## Modelos

### `CavaleteHistory`
Logs de ações em cavaletes (criação, edição, exclusão, mudança de status).

### `SlotHistory`
Logs de ações em slots.
- Inclui snapshot dos dados anteriores e novos (`old_quantity`, `new_quantity`, etc.) para auditoria detalhada.

## Integração
Os logs são gerados automaticamente pelos `Services` chamados nas Views do app `cavaletes`.

## Endpoints
Endpoints readonly para consulta de histórico.
- `/api/inventory/history/cavaletes/`
- `/api/inventory/history/slots/`
