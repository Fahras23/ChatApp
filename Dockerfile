FROM python:3.11

WORKDIR /app

COPY . /app

ENV DJANGO_SETTINGS_MODULE=chatapp.settings
ENV REDIS_PORT=6379
ENV REDIS_HOST=redis
ENV DEBUG=True

RUN pip install -r requirements.txt
RUN python manage.py makemigrations
RUN python manage.py migrate

EXPOSE 8000

ENTRYPOINT ["daphne", "-b", "0.0.0.0", "-p", "8000", "chatapp.asgi:application"]