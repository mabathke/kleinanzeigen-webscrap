FROM python:3.8-slim

WORKDIR /app

COPY . /app

RUN pip install Flask sqlite3

CMD ["python", "app/db_service.py"]
