# Arquitetura do Backend MetaScan

Este documento descreve a arquitetura e os componentes do backend do **MetaScan**. Visão do produto em [docs/product/vision.md](../docs/product/vision.md). Estrutura: apps base (accounts, core); apps de domínio (cavaletes, inventory, sankhya) conforme [backlog-backend](../docs/product/backlog-backend.md).

### Convenções de código

- **Choices:** ficam como atributos de classe no modelo que possui o campo (ex.: `User.ROLE_CHOICES` em `accounts/models.py`). Serializers e views importam do modelo quando precisarem da lista. Não usar `constants.py` só para choices de um único modelo.
- **Mensagens da API:** textos de resposta (erro, validação, sucesso) ficam em `messages.py` — em `core` para mensagens genéricas e em cada app para mensagens do domínio. Views e serializers importam e usam as constantes (ex.: `Response({"detail": USER_NOT_REGISTERED}, status=401)`).
- **Comentários e documentação (Django + PEP 257):** docstrings concisos — uma linha quando o propósito for óbvio; usar Args/Returns quando ajudar. Comentários e docstrings com quebra de linha em 79 caracteres. Evitar "we" em comentários. Não usar emojis em código, comentários, docstrings, commits ou documentação. Em `.env.example`, usar apenas cabeçalho de seção (`# ===`) e no máximo uma linha de explicação por bloco de variáveis. Contexto longo (ex.: migração OAuth) fica em ARCHITECTURE ou ADR, não no código.

### Boas práticas Django/DRF

- **Unicidade em modelos:** usar `Meta.constraints = [UniqueConstraint(fields=[...], name='...')]` em código novo (Django 2.2+); `unique_together` continua válido mas é legado.
- **ForeignKey:** definir `related_name` explícito em todas as FKs (evita conflitos de reverse e deixa a API clara), ex.: `user = models.ForeignKey(..., related_name='assigned_cavaletes')`.
- **Admin:** registrar novos modelos no Django Admin para operação e debug (list_display, list_filter quando fizer sentido).
- **Validação:** regras de negócio que dependem do estado do objeto (ex.: “só editar produto se status=auditing”) devem ser implementadas no **serializer** (validate ou validate_*), não apenas na view; a view delega ao serializer.
- **Lógica repetida:** uso de helper ou service (ex.: criação de histórico) em vez de duplicar lógica nas views; views permanecem enxutas.
- **Chamadas externas (ex.: Sankhya):** usar timeout e retry com backoff nas requisições HTTP para não bloquear workers.

## Componentes principais

### Apps

**apps.accounts**
- Serializers genéricos para User do Django (`UserSerializer`, `UserProfileSerializer`)
- Views para perfil e detalhes de usuário
- Endpoints: `/api/users/profile/` e `/api/users/<id>/`
- Configuração do Django Admin para User

**apps.core**
- Validators genéricos (`validate_cpf`, `validate_cnpj`)
- Funções utilitárias (`format_phone`, `format_cpf`, `format_cnpj`)
- Permissão customizada (`IsOwnerOrReadOnly`)

**Filtros**
- Suporte a filtros com `django-filter` para endpoints de listagem

### Autenticação JWT

**Endpoints JWT**
- `POST /api/token/` - Obter token (login)
- `POST /api/token/refresh/` - Renovar access token
- `POST /api/token/verify/` - Verificar token

**Configuração**
- JWT com blacklist de tokens habilitado
- Rotação de refresh tokens
- Tempo de vida configurável via variáveis de ambiente

**Exception handler (DRF)**
- Handler customizado em `apps.core.exceptions.custom_exception_handler` converte exceções do client Sankhya em respostas HTTP: `SankhyaAuthError` -> 503 (detail com mensagem); `SankhyaProductError` -> 404 se "Produto não encontrado", senão 502. Views que chamam `get_valid_token()` ou `get_product()` podem deixar a exceção subir; o DRF devolve JSON padronizado.

### Configurações

**settings.py**
- Carrega automaticamente o arquivo **`.env`**. Em ambientes Docker, as variáveis injetadas pelo Compose têm prioridade.
- **Banco de Dados**: Prioriza PostgreSQL se as variáveis estiverem definidas; caso contrário, usa SQLite em modo DEBUG.
- **Segurança**: HTTPS forçado em produção via `SECURE_SSL_REDIRECT` (configurável via env var).
- **Cache**: Usa Redis dinamicamente se `REDIS_URL` estiver definido, senão LocMemCache.
- **WhiteNoise**: Middleware configurado para servir arquivos estáticos em produção.
- CORS configurado (permissivo em dev, restritivo em prod)
- Logging configurado
- I18N configurável

**Ambientes**
- **Execução Nativa**: Uso de **`.env`** (SQLite/Cache Local) via `python manage.py runserver`.
- **Execução Docker Local**: Uso de **`.env.local`** (Postgres/Redis) via `docker-compose.local.yml`.
- **Deploy (Homol/Prod)**: Uso de **`.env`** (Postgres Externo/Nginx) via `docker-compose.yml`.

**Docker**
- `Dockerfile` configurado com Gunicorn
- `docker-compose.yml` para produção e homologação (PostgreSQL externo, Redis incluído, bind mounts customizáveis para static/media)
- `docker-compose.local.yml` para desenvolvimento local (PostgreSQL e Redis incluídos)
- `docker-entrypoint.sh` com timeout, migrate, collectstatic e criação de superusuário

**Makefile**
- Comandos úteis para desenvolvimento e Docker
- Comandos separados para desenvolvimento local (`-local`) e produção

**Qualidade de código**
- Configurações de `black`, `flake8`, `pytest` e `coverage`
- Referência em `QUALITY.md`

### Testes

- **Apps:** estrutura em `tests/` dentro de cada app (`apps/<app>/tests/`). Testes para serializers, views, autenticação, validators, utils e permissions.
- **Clients:** estrutura em `tests/` dentro de cada client (`clients/<client>/tests/`). Usar mock de HTTP (ex.: `unittest.mock.patch` em `requests`) para não chamar API real. Pytest descobre e executa com `testpaths = apps clients`.

### Documentação

- Estrutura em [`../docs/README.md`](../docs/README.md)
- Guia de contribuição em [`../docs/CONTRIBUTING.md`](../docs/CONTRIBUTING.md)
- ADRs em [`../docs/decisions/index.md`](../docs/decisions/index.md)

## Configuração

### 1. Variáveis de Ambiente

Arquivos: **`.env`** (produção ou nativo) ou **`.env.local`** (Docker local)

**Obrigatórias:**
- `SECRET_KEY`: Gere uma chave segura
- `DEBUG`: `true` ou `false`
- `ALLOWED_HOSTS`: Hosts permitidos

**PostgreSQL (obrigatórias quando variáveis estiverem definidas):**
- `POSTGRES_DB`: Nome do banco
- `POSTGRES_USER`: Usuário do PostgreSQL
- `POSTGRES_PASSWORD`: Senha do PostgreSQL
- `POSTGRES_HOST`: Host do PostgreSQL (`db` no Docker local, host/IP externo em produção)
- `POSTGRES_PORT`: Porta do PostgreSQL (padrão: `5432`)

**Opcionais:**
- `SECURE_SSL_REDIRECT`: Força HTTPS (padrão: `True` em produção)
- `JWT_ACCESS_MINUTES`: Tempo de vida do access token (padrão: 5)
- `JWT_REFRESH_DAYS`: Tempo de vida do refresh token (padrão: 1)
- `CORS_ALLOWED_ORIGINS`: Origens permitidas para CORS
- `LANGUAGE_CODE`: Código do idioma (padrão: `pt-br`)
- `TIME_ZONE`: Timezone (padrão: `UTC`)
- `REDIS_URL`: URL do Redis (`redis://redis:6379/1` no Docker, `redis://127.0.0.1:6379/1` fora)
- `GUNICORN_WORKERS`: Número de workers do Gunicorn (padrão: `2`)
- `STATIC_ROOT_HOST`: Caminho absoluto no host para arquivos estáticos (produção)
- `MEDIA_ROOT_HOST`: Caminho absoluto no host para arquivos de mídia (produção)
- `DJANGO_SUPERUSER_*`: Variáveis para criação automática de superusuário (apenas desenvolvimento)

### 2. Filtros (Opcional)

Dependência: `django-filter`

Para usar filtros em views, adicione `DjangoFilterBackend` e defina `filterset_fields`:

```python
from django_filters.rest_framework import DjangoFilterBackend

class ExampleViewSet(viewsets.ModelViewSet):
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["status", "created_at"]
```

### 3. CORS

Arquivo: `config/settings.py`

Em produção, configure `CORS_ALLOWED_ORIGINS` no `.env` com as origens permitidas.

### 4. Models e Apps

Pasta: `apps/`

Crie seus apps específicos em `apps/` seguindo o padrão:

```bash
python manage.py startapp meu_app
mv meu_app apps/
```

Atualize `config/settings.py` e `apps/meu_app/apps.py`.

### 5. Customização do User (Opcional)

Se precisar de campos adicionais no User, crie um modelo customizado:

```python
# apps/accounts/models.py
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # Seus campos customizados
    pass
```

Atualize `config/settings.py`:

```python
AUTH_USER_MODEL = 'accounts.User'
```

**Nota:** Faça isso antes de executar as primeiras migrações.

### 6. Validators (Opcional)

Arquivo: `apps/core/validators.py`

O validator de CPF implementa dígitos verificadores. O validator de CNPJ é básico; para validação completa, considere usar biblioteca externa.

## Estrutura de Apps

```
apps/
├── accounts/          # Autenticação e usuários
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── tests/
├── core/              # Funcionalidades compartilhadas
│   ├── validators.py
│   ├── utils.py
│   ├── permissions.py
│   └── tests/
└── ...                # Apps de domínio (cavaletes, inventory, sankhya)
```

**Clients (fora de apps/)**

```
clients/
├── sankhya/
│   ├── auth.py
│   ├── product.py
│   ├── constants.py
│   ├── exceptions.py
│   └── tests/
│       ├── test_auth.py
│       └── test_product.py
└── ...
```

## Notas

- **Migrations**: Versionadas em `apps/*/migrations/` para deploy.
- **Autenticação**: Por padrão, todas as views requerem autenticação JWT.
- **Paginação**: Padrão de 20 itens por página.
- **Cache**: LocMemCache por padrão, Redis dinâmico se `REDIS_URL` estiver definido.
- **Docker**: Use `docker-compose.local.yml` para ambiente local e `docker-compose.yml` para deploy (Homol/Prod).
