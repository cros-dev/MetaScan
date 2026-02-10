# Changelog - MetaScan Backend

Este arquivo registra mudanças notáveis no backend do MetaScan.

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
