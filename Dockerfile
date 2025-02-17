# filepath: /c:/Users/Neelesh/sigmafinalver/Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--reload", "--ssl-keyfile", "/app/certs/localhost.key", "--ssl-certfile", "/app/certs/localhost.crt"]