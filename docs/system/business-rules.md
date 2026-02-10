## Regras de Negócio - MetaScan

Este documento descreve regras de negócio do MetaScan (conferência de estoque em cavaletes).

### Princípios gerais

- O backend é a fonte única da verdade.
- Validações críticas (produto, quantidade, transições de status) ocorrem no servidor.
- Timestamps de histórico são gerados no backend.
- Convenções de código (choices, mensagens, boas práticas Django/DRF): ver [ARCHITECTURE.md](../../backend/ARCHITECTURE.md).

### Regras do MetaScan

- **Cavaletes:** código e nome gerados automaticamente (CAV01, CAV02, …). Quantidade de cavaletes e de slots não é limitada no backend; regras de limite, se desejadas, ficam no frontend.
- **Slots:** quantidade de slots por cavalete é definida pelo usuário (frontend informa ao criar/editar). Workflow com 3 estados — disponível → em conferência → concluído. Edição de produto/quantidade apenas quando o slot está em conferência.
- **Conferente:** vê e opera apenas os cavaletes atribuídos a ele.
- **Gestor/Admin:** podem atribuir cavaletes a usuários, exportar dados (ex.: Excel), finalizar conferências.
- **Sankhya:** consulta de produto por código para validação e dados de estoque; autenticação por usuário (token em cache).
- **Usuários:** primeiro superuser não pode ser removido nem desativado; usuários podem ser desativados (soft delete).

---

**Status:** Regras do MetaScan  
**Última atualização:** 2026-02-09
