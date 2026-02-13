## Regras de Negócio - MetaScan

Este documento descreve regras de negócio do MetaScan (conferência de estoque em cavaletes).

### Princípios gerais

- O backend é a fonte única da verdade.
- Validações críticas (produto, quantidade, transições de status) ocorrem no servidor.
- Timestamps de histórico são gerados no backend.
- Convenções de código (choices, mensagens, boas práticas Django/DRF): ver [ARCHITECTURE.md](../../backend/ARCHITECTURE.md).

### Papéis e Permissões

- **ADMIN:** Acesso total ao sistema e ao Django Admin.
- **MANAGER (Gestor):** Pode criar, editar e excluir cavaletes. Pode visualizar todo o histórico. Pode atribuir cavaletes a auditores.
- **AUDITOR (Conferente):** Pode visualizar apenas cavaletes atribuídos a ele. Pode iniciar conferência, editar slots (enquanto em conferência) e finalizar.

### Regras do MetaScan

- **Cavaletes:** Código único. Status: `AVAILABLE`, `IN_PROGRESS`, `COMPLETED`, `BLOCKED`.
- **Slots:**
  - Posição definida por Lado (A/B) e Número.
  - Workflow de 3 estados: `AVAILABLE` → `AUDITING` → `COMPLETED`.
  - **Regra de Edição:** Produto e quantidade só podem ser alterados se status for `AUDITING`.
  - Ações de workflow (`start-confirmation`, `finish-confirmation`) geram logs automáticos.
- **Sankhya:**
  - Consulta de produto por código para validação e descrição.
  - Autenticação via **usuário de serviço global** (configurado no backend), não por credenciais individuais do usuário logado.
  - Token de sessão armazenado em cache para performance.
- **Histórico (Auditoria):**
  - Todas as ações de criação, atualização, exclusão e mudança de status geram registros em `CavaleteHistory` ou `SlotHistory`.
  - Histórico de Slot guarda "snapshot" dos dados anteriores e novos (produto/quantidade) para auditoria de divergências.

---

**Status:** Regras do MetaScan  
**Última atualização:** 2026-02-09
