# Modelo de Card do Microsoft Planner

### Título do card:
```
[Área] Descrição curta da tarefa
```

### Descrição:
```
Relacionado ao Épico: [Nome do Épico]

Objetivo:
[Descreva o objetivo da tarefa]

Critérios de aceite:
- [Critério 1]
- [Critério 2]
```

### Checklist:
- [ ] Task 1
- [ ] Task 2
- [ ] Revisão

### Labels (TAGS):
- `Área` (Backend, Docs, Infra)
- `Tipo` (Feature, Bug, Refactor, Tech Debt)
- `Prioridade` (Alta, Média, Baixa)
- `Épico` (Ex: Épico: Base Técnica)

### Observações
- Registre o card no backlog do projeto (se aplicável).
- Cards multi-plataforma podem ser organizados em backlogs separados.

---

### Exemplo de Card Completo

**Título:** `[Backend] API de Autenticação JWT`

**Descrição:**
```
Relacionado ao Épico: Autenticação e Autorização

Objetivo:
Implementar sistema de autenticação JWT para permitir acesso seguro à API.

Critérios de aceite:
- API REST completa permite login e refresh token
- Validações: email válido, senha obrigatória
- Autenticação JWT obrigatória para endpoints protegidos
- Testes de integração passando
```

**Checklist:**
- [ ] Criar serializer de autenticação
- [ ] Criar ViewSet para login e refresh
- [ ] Configurar URLs
- [ ] Testes de integração
- [ ] Revisão de código

**Labels:**
- `Backend`
- `Feature`
- `Alta`
- `Épico: Autenticação e Autorização`

**Bucket:** `Backlog` (ou `Em andamento`)

---

**Status:** Modelo ativo  
**Última atualização:** 2026-01-26
