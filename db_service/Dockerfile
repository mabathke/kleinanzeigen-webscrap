FROM python:3.12-slim

WORKDIR /app

COPY . /app

RUN ls -la /app
RUN cat /app/requirements.txt

# Redirect the output of pip install to a file
RUN pip install -r requirements.txt > pip_install.log 2>&1

# Set environment variables
ENV PYTHONUNBUFFERED=1

CMD ["python","-u", "app/db_service.py"]
