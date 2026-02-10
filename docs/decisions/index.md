# Registro de Decisões Técnicas (ADR)

Este diretório contém o registro de decisões de arquitetura e produto do MetaScan.

## Decisões Aceitas

1. **Backend como fonte única da verdade**
   * **Motivo:** Evitar inconsistência e fraude. Garantir que regras críticas sejam sempre validadas no servidor.
   * **Impacto:** Frontend mais simples, consistência garantida, segurança aumentada.

2. **UUID gerado pelo backend**
   * **Motivo:** Garantir unicidade e evitar conflitos em sincronização offline ou distribuída.
   * **Impacto:** UUIDs sempre únicos, evita problemas de sincronização.

3. **Timestamp do backend para operações críticas**
   * **Motivo:** Evitar fraudes por manipulação de data/hora no cliente.
   * **Impacto:** Timestamps confiáveis, impossível fraudar horário de operações críticas.

4. **Sincronização offline com transação atômica**
   * **Motivo:** Garantir que sincronização em lote seja consistente (tudo ou nada).
   * **Impacto:** Consistência de dados, evita estados parciais.

5. **Separação de responsabilidades (Notion/Planner/Docs)**
   * **Motivo:** Organizar informação de forma profissional, desacoplando planejamento de execução.
   * **Impacto:** Notion (produto), Planner (execução), Git/docs (conhecimento técnico).

---

**Status:** Decisões consolidadas  
**Última atualização:** 2026-01-26
