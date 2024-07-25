# Use Python 3.12 as the base image
FROM python:3.12-slim

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

# Set environment variables
ENV PYTHONUNBUFFERED=1

CMD ["python","-u", "app/scraper_service.py"]
