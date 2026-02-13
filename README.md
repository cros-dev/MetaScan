# MetaScan

Repositório do **MetaScan** — sistema de conferência de estoque em cavaletes, com integração ao ERP Sankhya.

## Estrutura do repositório

- **backend/** — API Django (DRF, JWT, cavaletes, slots, histórico, Sankhya). Veja [backend/README.md](backend/README.md) para execução e configuração.
- **web/** — Frontend React (Vite, Chakra UI, PWA). Veja [web/README.md](web/README.md).
- **docs/** — Documentação técnica, produto e governança. Veja [docs/README.md](docs/README.md).

## Início rápido (backend)

```bash
git clone <url-do-repositorio>
cd MetaScan/backend
cp .env.example .env
# Edite .env conforme necessário
python -m venv venv
source venv/bin/activate   # ou venv\Scripts\activate no Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Acesse `http://localhost:8000`. Especificação da API: [docs/system/api-spec.md](docs/system/api-spec.md).
