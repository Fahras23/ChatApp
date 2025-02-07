FROM python:3.11

WORKDIR /app

COPY . /app

ENV  DJANGO_SETTINGS_MODULE=chatapp.settings

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "chatapp.asgi:application"]
