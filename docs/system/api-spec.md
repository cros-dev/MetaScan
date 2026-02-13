# Especificação de API - MetaScan

Este documento descreve os endpoints da API do MetaScan (conferência de estoque em cavaletes, integração Sankhya).

## Segurança e Limites

**Autenticação:** `Bearer <token>` (JWT).

**Rate Limiting:**
- **Global:** 2000 req/dia (usuários logados), 100 req/dia (anônimos).
- **Sankhya:** 60 req/min (endpoints `/api/sankhya/*`).

## Autenticação

- `POST /api/token/` - Login (access/refresh)
- `POST /api/token/refresh/` - Renovação do access token
- `POST /api/token/verify/` - Verificação de token

## Usuários

- `GET /api/users/profile/` - Perfil do usuário logado
- `PATCH /api/users/profile/` - Atualização do perfil logado
## Cavaletes (Inventory)

- `GET /api/inventory/cavaletes/` - Listar cavaletes
  - Gestor: Vê todos.
  - Conferente: Vê apenas os atribuídos a ele.
- `POST /api/inventory/cavaletes/` - Criar cavalete (Gestor)
- `GET /api/inventory/cavaletes/{id}/` - Detalhes do cavalete
- `PATCH /api/inventory/cavaletes/{id}/` - Atualizar cavalete (Gestor)
- `DELETE /api/inventory/cavaletes/{id}/` - Excluir cavalete (Gestor)

## Slots (Inventory)

- `GET /api/inventory/slots/` - Listar slots
- `GET /api/inventory/slots/{id}/` - Detalhes do slot
- `PATCH /api/inventory/slots/{id}/` - Atualizar dados (produto/quantidade)
  - Conferente: Apenas se status=`AUDITING`.
- `POST /api/inventory/slots/{id}/start-confirmation/` - Action: Iniciar conferência (Status -> AUDITING)
- `POST /api/inventory/slots/{id}/finish-confirmation/` - Action: Finalizar conferência (Status -> COMPLETED)

## Histórico (Inventory History)

- `GET /api/inventory/history/cavaletes/` - Histórico de cavaletes (Gestor)
- `GET /api/inventory/history/slots/` - Histórico de slots (Gestor)

## Integração Sankhya

- `GET /api/sankhya/products/{code}/` - Consulta de produto
  - Retorna descrição e código do produto direto do ERP.
