FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       build-essential \
       libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

COPY . /app/

EXPOSE 8000

CMD sh -c "python manage.py makemigrations && \
           python manage.py migrate --noinput && \
           python manage.py createsuperuser --noinput --email $DJANGO_SUPERUSER_EMAIL || true && \
           python manage.py runserver 0.0.0.0:8000"