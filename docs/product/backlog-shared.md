# Backlog - Shared (multi-plataforma)

Este arquivo contém os cards multi-plataforma (quando aplicável).
Use junto dos backlogs por plataforma em projetos monorepo.

## Quando Usar

- **Projeto Standalone (Backend único)**: Use apenas `backlog.md`
- **Monorepo (Múltiplas plataformas)**: Use `backlog-shared.md` + `backlog-{plataforma}.md`

## Estrutura Recomendada para Monorepo

```
docs/product/
├── vision.md           # Visão geral do produto
├── backlog.md          # Visão geral e índice dos backlogs
├── backlog-shared.md   # Cards multi-plataforma
├── backlog-backend.md  # Épicos e entregas do backend (em uso)
├── backlog-web.md      # Cards específicos do frontend (quando houver)
└── backlog-mobile.md   # Cards específicos do mobile (se aplicável)
```

A primeira fase do MetaScan prioriza o **backend**; o detalhamento está em [backlog-backend.md](backlog-backend.md) (épicos 0 a 6).

## Observações

- Este backlog é de **produto**, não de execução técnica.
- Detalhes de implementação devem ficar no Planner/Issues.
- Cards que afetam múltiplas plataformas devem estar em `backlog-shared.md`.
- Cards específicos de uma plataforma devem estar em `backlog-{plataforma}.md`.

---

**Última atualização:** 2026-02-09
