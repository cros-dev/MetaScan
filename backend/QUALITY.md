# Ferramentas de Qualidade de Código - MetaScan Backend

Este documento descreve as ferramentas de qualidade de código configuradas no backend e como utilizá-las.

**Para workflow de commits e padrões, veja [`../docs/CONTRIBUTING.md`](../docs/CONTRIBUTING.md).**

## Ferramentas Instaladas

- **pytest** - Framework de testes
- **pytest-django** - Plugin do pytest para Django
- **pytest-cov** - Plugin de coverage para pytest
- **coverage** - Análise de cobertura de código
- **black** - Formatador automático de código
- **flake8** - Linter de código Python

## Uso Rápido

**Nota:** Para workflow completo antes de commits, veja [`../docs/CONTRIBUTING.md`](../docs/CONTRIBUTING.md).

### Comandos Makefile (Linux/Mac)

```bash
# Executar todas as verificações (recomendado antes de commits)
make check
# ou
make quality

# Comandos individuais
make format    # Formatar código
make lint      # Verificar estilo de código
make test-cov  # Executar testes com coverage
```

### Windows (PowerShell/WSL)

**Opção 1: Instalar Make (Recomendado)**

```powershell
# Via Chocolatey
choco install make

# Ou usar WSL (Windows Subsystem for Linux)
wsl
# Depois use os comandos make normalmente
```

**Opção 2: Usar Comandos Diretos**

Se o `make` não estiver disponível, use os comandos diretos abaixo.

### Comandos Diretos

**Use estes comandos se o `make` não estiver disponível (Windows sem make):**

```bash
# Formatar código
black apps config manage.py

# Verificar estilo
flake8 apps config manage.py

# Executar testes com coverage
pytest
```

**Windows PowerShell:**

No PowerShell, execute os comandos separadamente (não use `&&`):

```powershell
# Executar sequencialmente
black apps config manage.py
flake8 apps config manage.py
pytest
```

**Windows CMD:**

No CMD, você pode usar `&&`:

```cmd
black apps config manage.py && flake8 apps config manage.py && pytest
```

**Nota:** O `make check` já executa todos os comandos na ordem correta, então é recomendado usar `make` quando disponível.

**Ver relatório de coverage em HTML:**
```bash
pytest
# Abrir: htmlcov/index.html
```

## Detalhamento das Ferramentas

### 1. Black (Formatador)

**O que faz:** Formata automaticamente o código Python seguindo o estilo PEP 8.

**Configuração:** `pyproject.toml`

**Uso:**
```bash
# Formatar todos os arquivos
black apps config manage.py

# Verificar sem formatar (dry-run)
black --check apps config manage.py
```

**Características:**
- Linha máxima: 88 caracteres
- Formatação automática de imports
- Compatível com Python 3.8+

### 2. Flake8 (Linter)

**O que faz:** Verifica estilo de código, erros e complexidade.

**Configuração:** `.flake8`

**Uso:**
```bash
# Verificar código
flake8 apps config manage.py

# Verificar com estatísticas
flake8 --statistics apps config manage.py
```

**Regras configuradas:**
- Linha máxima: 88 caracteres
- Complexidade máxima: 10
- Ignora migrations e arquivos de configuração
- Ignora imports não utilizados em `__init__.py`

### 3. Pytest (Testes)

**O que faz:** Framework de testes moderno e poderoso.

**Configuração:** `pytest.ini` e `pyproject.toml`

**Uso:**
```bash
# Executar todos os testes
pytest

# Executar testes de um app específico
pytest apps/accounts/

# Executar testes de um client específico
pytest clients/sankhya/

# Executar um arquivo de teste específico
pytest apps/accounts/tests/test_views.py

# Executar um teste específico
pytest apps/accounts/tests/test_views.py::test_login

# Modo verbose
pytest -v

# Parar no primeiro erro
pytest -x
```

**Características:**
- Integração com Django
- Coverage automático
- Relatórios em HTML e XML
- Coverage mínimo configurável (atualmente 0% para desenvolvimento inicial)

### 4. Coverage (Cobertura)

**O que faz:** Mede a cobertura de código pelos testes.

**Configuração:** `.coveragerc`

**Uso:**
```bash
# Executar testes com coverage
pytest

# Ver relatório no terminal
coverage report

# Ver relatório em HTML
coverage html
# Abrir: htmlcov/index.html

# Ver apenas arquivos não cobertos
coverage report --show-missing
```

**Métricas:**
- Cobertura mínima: configurável (atualmente 0% para desenvolvimento inicial)
- Relatórios em HTML, XML e terminal
- Exclui migrations e arquivos de configuração

## Estrutura de Arquivos

```
backend/
├── pytest.ini          # Configuração do pytest
├── .flake8             # Configuração do flake8
├── .coveragerc         # Configuração do coverage
├── pyproject.toml      # Configuração do black e pytest
└── QUALITY.md          # Este arquivo
```

## Workflow Recomendado

**Para workflow completo antes de commits, consulte [`../docs/CONTRIBUTING.md`](../docs/CONTRIBUTING.md#-validação-de-commits).**

### Em CI/CD:

```bash
# Verificar sem modificar arquivos
black --check apps config manage.py
flake8 apps config manage.py
pytest
```

## Configurações Importantes

### Black
- **Linha máxima:** 88 caracteres
- **Target:** Python 3.8+
- **Exclui:** migrations, venv, __pycache__

### Flake8
- **Linha máxima:** 88 caracteres
- **Complexidade máxima:** 10
- **Exclui:** migrations, venv, arquivos de configuração

### Pytest
- **Coverage mínimo:** Configurável (atualmente 0% para desenvolvimento inicial)
- **Relatórios:** HTML, XML, terminal
- **Cobertura de:** `apps/` e `clients/`
- **Testpaths:** `apps` e `clients` (cada app/client com pasta `tests/`)
- **Ignora:** arquivos `tests.py` (usa apenas diretório `tests/`)

### Coverage
- **Exclui:** migrations, testes, arquivos de configuração
- **Relatório HTML:** `htmlcov/index.html`

## Solução de Problemas

### Make não encontrado no Windows

**Erro:** `make: O termo 'make' não é reconhecido...`

**Soluções:**

1. **Instalar Make via Chocolatey:**
   ```powershell
   choco install make
   ```

2. **Usar WSL (Windows Subsystem for Linux):**
   ```powershell
   wsl
   # Depois use make normalmente
   ```

3. **Usar comandos diretos:**
   ```powershell
   black apps config manage.py
   flake8 apps config manage.py
   pytest
   ```

### Black não formata arquivos
```bash
# Verificar se o arquivo está sendo ignorado
black --check --verbose apps/
```

### Flake8 encontra muitos erros
```bash
# Ver apenas erros críticos
flake8 --select=E,F apps/

# Ignorar erros específicos
flake8 --ignore=E501,W503 apps/
```

### Coverage abaixo do mínimo
```bash
# Ver quais arquivos não estão cobertos
coverage report --show-missing

# Executar testes novamente
pytest --cov=apps --cov-report=term-missing
```

## Recursos

- [Black Documentation](https://black.readthedocs.io/)
- [Flake8 Documentation](https://flake8.pycqa.org/)
- [Pytest Documentation](https://docs.pytest.org/)
- [Coverage Documentation](https://coverage.readthedocs.io/)
- [Pytest-Django](https://pytest-django.readthedocs.io/)
