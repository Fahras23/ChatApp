FROM python:3.11

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

COPY . /app/backend

EXPOSE 8000

CMD ["gunicorn", "chatapp.wsgi:application", "--bind", "0.0.0.0:8000"]