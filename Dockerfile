FROM python:3.11-alpine

WORKDIR /app

COPY . /app

ENV DJANGO_SETTINGS_MODULE=chatapp.settings
ENV REDIS_PORT=6379
ENV REDIS_HOST=beta-redis
ENV DEBUG=False

RUN apk add --no-cache postgresql postgresql-contrib libpq-dev musl-dev gcc
RUN ln -s /usr/bin/pg_config /usr/local/bin/pg_config

RUN pip install -r requirements.txt

EXPOSE 8000

ENTRYPOINT ["daphne", "-b", "0.0.0.0", "-p", "8000", "chatapp.asgi:application"]