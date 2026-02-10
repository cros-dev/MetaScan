#!/bin/bash
set -e

POSTGRES_HOST=${POSTGRES_HOST:-localhost}
POSTGRES_PORT=${POSTGRES_PORT:-5432}
MAX_WAIT=60
WAIT_COUNT=0

echo "Aguardando PostgreSQL em $POSTGRES_HOST:$POSTGRES_PORT ..."

while ! nc -z "$POSTGRES_HOST" "$POSTGRES_PORT"; do
  WAIT_COUNT=$((WAIT_COUNT + 1))
  if [ $WAIT_COUNT -ge $MAX_WAIT ]; then
    echo "Erro: PostgreSQL não ficou disponível após ${MAX_WAIT}s"
    exit 1
  fi
  sleep 1
done

echo "PostgreSQL está disponível!"

echo "Executando migrações..."
python manage.py migrate --noinput

echo "Coletando arquivos estáticos..."
python manage.py collectstatic --noinput

if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_EMAIL" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
  echo "Verificando superusuário..."
  python manage.py shell << EOF
from django.contrib.auth import get_user_model
User = get_user_model()

username = "$DJANGO_SUPERUSER_USERNAME"
email = "$DJANGO_SUPERUSER_EMAIL"
password = "$DJANGO_SUPERUSER_PASSWORD"

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print("Superusuário criado com sucesso!")
else:
    print("Superusuário já existe.")
EOF
fi

exec "$@"
