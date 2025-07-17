# MetaScan

Projeto monorepo que reúne as aplicações backend, mobile e web do MetaScan.

## Tecnologias

- **Backend:** Django + Django REST Framework (Python)
- **Mobile:** Kotlin (Android Studio)
- **Web:** Angular

## Estrutura do repositório

```
MetaScan/
  ├── backend/   # Backend Django
  ├── mobile/    # App Android Kotlin
  ├── web/       # Frontend Angular
  ├── .gitignore
  └── README.md
```

---

## Como rodar cada aplicação

### Backend (Django)

### Rodando localmente sem Docker

1. Navegue até a pasta `backend/`
2. Crie e ative o ambiente virtual (recomendado):

```bash
python -m venv metascan
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate   # Windows PowerShell
```

1. Instale as dependências:

```bash
pip install -r requirements.txt
```

1. Rode as migrations:

```bash
python manage.py migrate
```

1. Execute o servidor:

```bash
python manage.py runserver
```

---

### Rodando com Docker

O projeto possui configuração para rodar backend, banco de dados Postgres e MinIO via Docker Compose.

1. Crie um arquivo `.env` baseado no `.env.example` (veja seção abaixo)
2. Na pasta `backend/` rode:

```bash
docker-compose up --build
```

1. O backend estará acessível em `http://localhost:8000`
2. O MinIO console fica disponível em `http://localhost:9001`

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

1. Rode o servidor de desenvolvimento:

```bash
npm start
```

1. Acesse no navegador: `http://localhost:4200`

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

Caio Riquelmy — [LinkedIn](https://www.linkedin.com/in/caioriquelmy/) — crosnegocios@hotmail.com

---

*README criado em 17/07/2025 para o projeto MetaScan.*
