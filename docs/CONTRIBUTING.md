# Guia de Contribuição - MetaScan

Este documento define padrões mínimos para contribuir com o projeto MetaScan.

**Para detalhes técnicos das ferramentas de qualidade, veja [`../QUALITY.md`](../QUALITY.md).**

## Documentação

- Estrutura e padrões gerais estão em [`README.md`](./README.md).

## Padrão de Commits

Seguimos o padrão **Conventional Commits** adaptado para o contexto do projeto.

### Formato

```
<tipo>[escopo]: <descrição curta>

[corpo opcional]

[rodapé opcional]
```

### Tipos de Commit

| Tipo | Descrição | Exemplo |
|------|-----------|---------|
| `feat` | Nova funcionalidade | `feat(auth): adiciona login com JWT` |
| `fix` | Correção de bug | `fix(api): corrige validação de email` |
| `docs` | Documentação | `docs(readme): atualiza instruções de setup` |
| `style` | Formatação, ponto e vírgula, etc | `style: formata código com black` |
| `refactor` | Refatoração de código | `refactor: reorganiza estrutura de apps` |
| `perf` | Melhoria de performance | `perf(api): otimiza query` |
| `test` | Testes | `test(auth): adiciona testes de login` |
| `build` | Build, dependências, ferramentas | `build(deps): atualiza Django` |
| `ci` | CI/CD | `ci: adiciona pipeline` |
| `chore` | Tarefas de manutenção | `chore: atualiza dependências` |
| `setup` | Configuração inicial | `setup: initial commit` |

### Escopo (Opcional)

O escopo indica a área do projeto afetada:

- `backend` - Backend Django
- `docs` - Documentação
- `config` - Configurações gerais

### Descrição

- **Curta e objetiva** (máximo 72 caracteres)
- **Imperativo** (ex: "adiciona" não "adicionando" ou "adicionado")
- **Sem ponto final**
- **Primeira letra minúscula**

### Exemplos

#### Bons Exemplos

```
feat(auth): adiciona login com JWT
fix(api): corrige validação de email
docs(readme): atualiza instruções de setup
refactor(backend): reorganiza estrutura de apps
setup: initial commit - estrutura do repositório
setup(backend): cria estrutura de apps do backend
feat(backend): configura ferramentas de qualidade de código
```

#### ❌ Exemplos Incorretos

```
feat: Adiciona login com JWT.  # Ponto final e maiúscula
feat(auth): adicionando login   # Gerúndio
fix: bug corrigido              # Muito genérico
feat(auth): adiciona funcionalidade de login com autenticação JWT e refresh token  # Muito longo
```

### Corpo do Commit (Opcional)

Use o corpo para explicar o **porquê** e **como**, não o **o quê**:

```
feat(auth): adiciona refresh token

Implementa renovação automática de tokens JWT para melhorar
a experiência do usuário e evitar logout inesperado.

Closes #123
```

### Rodapé (Opcional)

Use para referenciar issues, PRs ou breaking changes:

```
feat(api): altera formato de resposta

BREAKING CHANGE: endpoint /users agora retorna array ao invés de objeto
```

## Validação de Commits


## Fluxo de trabalho por card (recomendado)

1. Definir/atualizar o card no Planner e no backlog do projeto (se aplicável)
2. Criar branch a partir de `dev` seguindo o padrão em "Branches"
3. Implementar a funcionalidade + testes
4. Atualizar documentação e changelog quando aplicável
5. Abrir PR e revisar

### Workflow Antes de Fazer Commit

**Sempre execute antes de commitar:**

#### Backend (Django)

**Linux/Mac (com make):**
```bash
make check
```

**Windows (sem make):**
```powershell
black apps config manage.py
flake8 apps config manage.py
pytest
```

**Windows (com WSL ou make instalado):**
```bash
make check
```

**Detalhes técnicos das ferramentas:** Veja [`../QUALITY.md`](../QUALITY.md).

### Checklist Antes de Commit

- [ ] Código formatado (`make format` ou `black apps config manage.py`)
- [ ] Estilo verificado (`make lint` ou `flake8 apps config manage.py`)
- [ ] Testes passando (`make test-cov` ou `pytest`)
- [ ] Tipo de commit está correto?
- [ ] Descrição está clara e objetiva?
- [ ] Escopo está correto (se aplicável)?
- [ ] Mensagem segue o padrão?

**Nota Windows:** Se `make` não estiver disponível, use os comandos diretos listados acima.

### Git Hooks (Opcional)

Para validar commits automaticamente, você pode usar:

```bash
# Instalar commitlint (se configurado)
npm install -g @commitlint/cli @commitlint/config-conventional
```

## Checklist de Pull Request

Antes de abrir um PR:

- [ ] Código formatado e verificado (`make check` ou comandos diretos)
- [ ] Testes passam (`make test-cov` ou `pytest`)
- [ ] Coverage adequado (mínimo configurável)
- [ ] Documentação atualizada (se necessário)
- [ ] Commits seguem o padrão definido
- [ ] Branch está atualizada com `master`/`dev`

**Nota Windows:** Veja seção "Workflow Antes de Fazer Commit" acima para comandos alternativos.

## Convenções Adicionais

### Branches

- `master` - Código em produção
- `dev` - Desenvolvimento
- `feature/nome-da-feature` - Nova funcionalidade
- `fix/nome-do-fix` - Correção de bug
- `hotfix/nome-do-hotfix` - Correção urgente

### Code Review

- Seja construtivo e respeitoso
- Foque no código, não na pessoa
- Explique o "porquê" das sugestões
- Aprenda com feedbacks

---

**Status:** Padrões de contribuição estabelecidos  
**Última atualização:** 2026-01-26
