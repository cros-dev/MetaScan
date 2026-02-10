# Documentação Técnica - MetaScan

Esta pasta contém a documentação técnica do **MetaScan**.

O **MetaScan** é um sistema de conferência de estoque em cavaletes: apoio à auditoria e ao controle de inventário com cavaletes, slots (posições), atribuição de responsáveis, fluxo de conferência (disponível → em conferência → concluído) e integração ao ERP Sankhya para validação de produtos. A documentação aqui cobre visão do produto, regras de negócio, modelo de dados, API e decisões técnicas.

## Estrutura

```
docs/
├── product/                # Visão e backlog (placeholders)
│   ├── vision.md           # Visão geral do produto
│   ├── backlog.md          # Épicos e backlog (alto nível) - para projetos standalone
│   └── backlog-shared.md    # Cards multi-plataforma - para monorepos
├── system/                 # Documentação técnica do sistema
│   ├── api-spec.md         # Especificação de API (base)
│   ├── data-model.md       # Modelo de dados (base)
│   ├── business-rules.md   # Regras de negócio (base)
│   └── postman-guide.md    # Padrão de uso do Postman
├── governance/             # Papéis e responsabilidades
│   └── roles.md            # Papéis funcionais (negócio)
├── decisions/              # Registro de decisões (ADR)
│   └── index.md            # Índice de decisões
├── templates/              # Modelos de documentos e guias
│   └── planner-card.md     # Padrão de card (Planner)
├── CONTRIBUTING.md         # Guia de contribuição e commits
└── README.md               # Este arquivo
```

## Estrutura de Backlog

### Projeto Standalone (Padrão)

Para projetos com apenas backend, use `backlog.md`:

```
docs/product/
├── vision.md
└── backlog.md          # Todos os épicos e cards
```

### Monorepo (Múltiplas Plataformas)

Para monorepos com múltiplas plataformas, separe os backlogs:

```
docs/product/
├── vision.md
├── backlog-shared.md    # Cards multi-plataforma
├── backlog-backend.md   # Cards específicos do backend
├── backlog-web.md       # Cards específicos do frontend
└── backlog-mobile.md    # Cards específicos do mobile (se aplicável)
```

**Regra:** Cards que afetam múltiplas plataformas vão em `backlog-shared.md`. Cards específicos de uma plataforma vão em `backlog-{plataforma}.md`.

## Documentação por Plataforma

Documentação técnica específica do backend:

- **Backend:** [`../backend/ARCHITECTURE.md`](../backend/ARCHITECTURE.md) | [`../backend/QUALITY.md`](../backend/QUALITY.md)

## Fonte da Verdade

Separação recomendada para manter a informação organizada:

1. **Git (`docs/`)**: Documentação técnica estável e padrões.
2. **Notion** (opcional): Documentação de produto colaborativa.
3. **Planner** (opcional): Execução diária (tasks, bugs, code reviews).

---

**Status:** Documentação do MetaScan  
**Última atualização:** 2026-02-09
