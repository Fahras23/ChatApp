FROM python:3.11-alpine AS builder

WORKDIR /app

# Copy only requirements first for better caching
COPY requirements.txt .

# Install build deps, pip, requirements; clean up in same layer
RUN apk add --no-cache \
    gcc \
    musl-dev \
    postgresql-dev \
    libpq-dev && \
    pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    apk del gcc musl-dev && \
    rm -rf /root/.cache

# Runtime image
FROM python:3.11-alpine

WORKDIR /app

# Runtime PostgreSQL deps only (no build tools)
RUN apk add --no-cache postgresql-libs && \
    ln -s /usr/bin/pg_config /usr/local/bin/pg_config

# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy app code last (changes often, invalidates cache minimally)
COPY . .

ENV DJANGO_SETTINGS_MODULE=chatapp.settings \
    REDIS_PORT=6379 \
    REDIS_HOST=beta-redis \
    DEBUG=False

EXPOSE 8000

ENTRYPOINT ["daphne", "-b", "0.0.0.0", "-p", "8000", "chatapp.asgi:application"]
