# MetaScan

Projeto monorepo que reúne as aplicações backend, mobile e web do MetaScan.

## Tecnologias

- **Backend:** Django + Django REST Framework (Python)
- **Mobile:** Kotlin (Android Studio)
- **Web:** Angular

## Estrutura do repositório

```
MetaScan/
  ├── backend/   # Backend Django (estrutura modular)
  ├── mobile/    # App Android Kotlin
  ├── web/       # Frontend Angular
  ├── .gitignore
  └── README.md
```

---

## Backend Django - Arquitetura Modular

O backend foi reorganizado em apps Django específicos para melhor organização e manutenibilidade. **Todas as funcionalidades existentes foram preservadas** e organizadas por domínio.

### 🏗️ Estrutura de Apps:

#### **`core/`** - Configurações Globais
- **Responsabilidade**: Usuários, autenticação e permissões
- **Modelos**: `CustomUser` (com roles e senha Sankhya criptografada)
- **Views**: `LoginView`, `MeView`, `TokenRefreshView`, `UserViewSet`
- **Funcionalidades**: Autenticação JWT, autorização e gestão de usuários

#### **`cavaletes/`** - Gestão de Cavaletes
- **Responsabilidade**: Cavaletes e slots
- **Modelos**: `Cavalete`, `Slot`
- **Views**: `CavaleteViewSet` (com todas as actions funcionais)
- **Funcionalidades**: CRUD de cavaletes, exportação Excel, atribuição de usuários

#### **`inventory/`** - Auditoria e Histórico
- **Responsabilidade**: Auditoria e controle de estoque
- **Modelos**: `SlotHistory`, `CavaleteHistory`
- **Views**: `SlotViewSet`, `SlotHistoryViewSet`, `CavaleteHistoryViewSet`
- **Funcionalidades**: Gestão de slots, conferência de estoque, actions bulk

#### **`sankhya/`** - Integração ERP
- **Responsabilidade**: Integração com ERP Sankhya
- **Views**: `ProductConsultView`
- **Serviços**: Autenticação, consulta de produtos e estoque
- **Funcionalidades**: Validação de produtos, consulta de estoque em tempo real

#### **`reports/`** - Relatórios (Futuro)
- **Responsabilidade**: Relatórios e análises
- **Funcionalidades**: Dashboards, métricas, exportação

### 📁 Estrutura de Cada App:
```
app_name/
├── __init__.py
├── admin.py          # Configuração do Django Admin
├── apps.py           # Configuração do app
├── models.py         # Modelos de dados
├── views.py          # Views da API
├── urls.py           # URLs do app
├── serializers.py    # Serializers DRF
├── services/         # Lógica de negócio
├── tests/            # Testes unitários
└── migrations/       # Migrações do banco
```

### ✅ Funcionalidades Preservadas:
- **Autenticação JWT** com integração Sankhya
- **Gestão completa de cavaletes** (CRUD, exportação, atribuição)
- **Gestão de slots** com workflow de conferência
- **Histórico completo** de todas as ações
- **Integração Sankhya** para validação de produtos
- **Sistema de permissões** por roles (admin, gestor, conferente)
- **Exportação Excel** de dados
- **Actions customizadas** para mudanças de status

### 🔗 URLs Principais:
- `/cavaletes/` - Gestão de cavaletes
- `/slots/` - Gestão de slots
- `/slot-history/` - Histórico de slots
- `/cavalete-history/` - Histórico de cavaletes
- `/users/` - Gestão de usuários
- `/product/<code>/` - Consulta Sankhya
- `/login/` - Autenticação
- `/me/` - Dados do usuário logado

**📖 Para documentação detalhada dos apps, consulte `backend/README_APPS.md`**

---

## Como rodar cada aplicação

### Backend (Django)

#### Rodando localmente sem Docker

1. Navegue até a pasta `backend/`
2. Crie e ative o ambiente virtual (recomendado):

```bash
python -m venv metascan
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate   # Windows PowerShell
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

4. Rode as migrations:

```bash
python manage.py migrate
```

5. Execute o servidor:

```bash
python manage.py runserver
```

---

#### Rodando com Docker

O projeto possui configuração para rodar backend, banco de dados Postgres e MinIO via Docker Compose.

1. Crie um arquivo `.env` baseado no `.env.example` (veja seção abaixo)
2. Na pasta `backend/` rode:

```bash
docker-compose up --build
```

3. O backend estará acessível em `http://localhost:8000`
4. O MinIO console fica disponível em `http://localhost:9001`

---

### Mobile (Android Kotlin)

- Abra a pasta `mobile/` no Android Studio
- Aguarde o Gradle sincronizar
- Rode o app em um emulador ou dispositivo físico

---

### Web (Angular)

1. Navegue até a pasta `web/`
2. Instale as dependências:

```bash
npm install
```

3. Rode o servidor de desenvolvimento:

```bash
npm start
```

4. Acesse no navegador: `http://localhost:4200`

---

## Integração com ERP Sankhya

Esta aplicação possui integração direta com o ERP Sankhya para validação de códigos de produtos e consulta de estoque em tempo real nos diferentes locais de armazenagem.

Isso permite:

- Conferir rapidamente a disponibilidade dos produtos nos cavaletes.
- Atualizar quantidades e locais de armazenagem com precisão.
- Evitar erros manuais na conferência do inventário.
- Otimizar o processo de registro utilizando QR Codes e códigos de barras.

---

## Variáveis de ambiente - `.env.example`

Copie o arquivo `.env.example` para `.env` e ajuste os valores conforme seu ambiente:

```
# Configuração do banco Postgres
DB_NAME=metascan_db
DB_USER=metascan_user
DB_PASSWORD=metascan_pass

# Configuração MinIO
MINIO_ACCESS_KEY=minioaccesskey
MINIO_SECRET_KEY=miniosecretkey
MINIO_BUCKET=metascan-bucket

# Superusuário Django (será criado automaticamente no container)
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@metascan.com
DJANGO_SUPERUSER_PASSWORD=changeme123
```

---

## Fluxo de trabalho

- Branches principais:
    - `main`: branch estável
    - `develop`: branch de desenvolvimento
    - `feature/*`: branches de funcionalidades/etapas
- Organização das tarefas via **Kanban** no GitHub Projects com colunas:
    - Backlog
    - To Do
    - Doing
    - Done

---

## Contato

Caio Riquelmy — [LinkedIn](https://www.linkedin.com/in/caio-riquelmy-a295ba19b/) — crosnegocios@hotmail.com

---

*README atualizado em 29/08/2025 para o projeto MetaScan com nova arquitetura modular.*
