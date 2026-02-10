# MetaScan - Backend

API REST do **MetaScan** com Django + DRF + JWT.

O MetaScan é um sistema de **conferência de estoque em cavaletes**: permite cadastrar cavaletes e posições (slots), atribuir responsáveis, registrar produtos e quantidades por slot e acompanhar o fluxo de conferência, com integração ao **ERP Sankhya** para validação de produtos e consulta de estoque. Este backend expõe os endpoints de autenticação, usuários, cavaletes, slots, históricos e consulta Sankhya.

## 1. Execução Nativa (Sem Docker)

Ideal para tarefas rápidas ou máquinas com pouca memória. Usa SQLite e cache local automaticamente.

```bash
# Entre na pasta do backend
cd backend

# Crie e ative ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Instale dependências
pip install -r requirements.txt

# Configure variáveis de ambiente
cp .env.example .env
# Edite .env (mantenha variáveis de banco vazias para usar SQLite)

# Execute migrações
python manage.py migrate

# Execute o servidor
python manage.py runserver
```

Acesse `http://localhost:8000`.

## 2. Execução via Docker (Local)

Recomendado para manter paridade com o ambiente de produção (usa PostgreSQL e Redis).

```bash
# Configure variáveis de ambiente
cp .env.example .env.local
# Edite .env.local com suas configurações (ou use os padrões do arquivo)

# Suba os serviços
docker compose -f docker-compose.local.yml up -d --build
```

**Características:**
- PostgreSQL e Redis incluídos no compose
- Hot-reload ativado (`--reload` no gunicorn)
- Volume de código montado para desenvolvimento
- Portas expostas: `8000` (backend) e `5432` (PostgreSQL)
- Superusuário criado automaticamente se variáveis estiverem definidas no `.env.local`

## 3. Deploy (Homologação e Produção)

### Homologação

Ambiente de testes idêntico à produção.

```bash
# Configure variáveis de ambiente
cp .env.example .env
# Edite .env com as configurações de homologação (DNS, Banco, etc)

# Crie os diretórios para static/media isolados
sudo mkdir -p /var/www/seu-projeto/hml/static /var/www/seu-projeto/hml/media
sudo chown -R www-data:www-data /var/www/seu-projeto/hml
sudo chmod -R 755 /var/www/seu-projeto/hml

# Suba os serviços usando o compose de produção
docker compose up -d --build
```

### Produção

Deploy oficial do sistema.

```bash
# Configure variáveis de ambiente
cp .env.example .env
# Edite .env com suas configurações de produção

# Crie os diretórios para static/media (se ainda não existirem)
# RECOMENDADO: use subpastas para separar ambientes (hml, prod, etc)
sudo mkdir -p /var/www/seu-projeto/prod/static /var/www/seu-projeto/prod/media
sudo chown -R www-data:www-data /var/www/seu-projeto
sudo chmod -R 755 /var/www/seu-projeto

# Suba os serviços
docker compose up -d --build
```

**Características:**
- PostgreSQL externo (não incluído no compose)
- Redis incluído
- Gunicorn com workers configuráveis via `GUNICORN_WORKERS`
- `restart: unless-stopped` para alta disponibilidade
- Static/media servidos via Nginx (bind mounts configuráveis via `STATIC_ROOT_HOST` e `MEDIA_ROOT_HOST`)

**Notas:**
- O container usa `gunicorn` por padrão.
- `collectstatic` e `migrate` rodam automaticamente no startup via `docker-entrypoint.sh`.
- Static/media são coletados no container e disponibilizados via bind mounts para o Nginx.
- Defina `SECURE_SSL_REDIRECT=False` quando o acesso for HTTP.
- `POSTGRES_HOST` deve ser `db` no Docker local, ou host/IP externo em produção.
- `REDIS_URL` deve ser `redis://redis:6379/1` no Docker, ou `redis://127.0.0.1:6379/1` fora do Docker.
- `GUNICORN_WORKERS` é opcional (padrão: `2`).
- `STATIC_ROOT_HOST` e `MEDIA_ROOT_HOST` permitem customizar os caminhos no host. Devem ser preenchidos no `.env` de produção.

## Estrutura

```
apps/
├── accounts/      # App de autenticação
├── core/          # Funcionalidades compartilhadas
└── ...            # Seus apps aqui
```

## Documentação

- [ARCHITECTURE.md](./ARCHITECTURE.md) - Arquitetura do backend
- [QUALITY.md](./QUALITY.md) - Ferramentas de qualidade de código
- [CHANGELOG.md](./CHANGELOG.md) - Histórico de mudanças
- [../docs/README.md](../docs/README.md) - Estrutura de documentação
- [../docs/CONTRIBUTING.md](../docs/CONTRIBUTING.md) - Guia de contribuição
- [../docs/system/api-spec.md](../docs/system/api-spec.md) - Especificação da API
- [../docs/system/data-model.md](../docs/system/data-model.md) - Modelo de dados
- [../docs/system/business-rules.md](../docs/system/business-rules.md) - Regras de negócio
- [../docs/system/postman-guide.md](../docs/system/postman-guide.md) - Padrão Postman
- [../docs/decisions/index.md](../docs/decisions/index.md) - Registro de decisões (ADR)

## Scripts

### Desenvolvimento
- `python manage.py runserver` - Servidor de desenvolvimento
- `python manage.py migrate` - Executar migrações
- `python manage.py makemigrations` - Criar migrações
- `make help` - Ver todos os comandos disponíveis

### Qualidade de Código
- `make format` - Formatar código com black
- `make lint` - Verificar código com flake8
- `make test-cov` - Executar testes com coverage
- `make check` - Executar todas as verificações (format + lint + test-cov)

### Docker
- `make docker-up-local` - Iniciar containers (Docker Local)
- `make docker-up` - Iniciar containers (homologação/produção)
- `make docker-down-local` - Parar containers (Docker Local)
- `make docker-down` - Parar containers (homologação/produção)
- `make docker-logs-local` - Ver logs (Docker Local)
- `make docker-logs` - Ver logs (homologação/produção)

## Tecnologias

- Django 6.0.1
- Django REST Framework 3.16.1
- djangorestframework-simplejwt 5.5.1
- django-cors-headers 4.3.1
- django-filter 24.2
- PostgreSQL (produção ou desenvolvimento via Docker Local)
- SQLite (desenvolvimento local nativo sem Docker)

## Configuração Inicial

Configure as variáveis de ambiente:
- **Execução Nativa**: copie `.env.example` para **`.env`** (mantenha variáveis de banco vazias para usar SQLite).
- **Execução Docker Local**: copie `.env.example` para **`.env.local`** (preencha com as credenciais do Postgres do container).
- **Deploy (Homol/Prod)**: copie `.env.example` para **`.env`** no servidor (preencha com as credenciais reais).

O arquivo `settings.py` carrega o `.env` por padrão, mas o Docker Compose Local injeta o `.env.local` com prioridade.

## Endpoints

### Autenticação JWT

- `POST /api/token/` - Obter token (login)
- `POST /api/token/refresh/` - Renovar access token
- `POST /api/token/verify/` - Verificar token

### Usuários

- `GET /api/users/profile/` - Perfil do usuário autenticado
- `PUT/PATCH /api/users/profile/` - Atualizar perfil
- `GET /api/users/<id>/` - Detalhes de um usuário

## Recursos

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Simple JWT](https://django-rest-framework-simplejwt.readthedocs.io/)
