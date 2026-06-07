FROM python:3.11-slim
WORKDIR /app
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt
COPY . .
WORKDIR /app/projet_wave1
EXPOSE 8000
ENV PYTHONPATH=/app/projet_wave1:/app
CMD ["gunicorn", "projet_wave1.wsgi", "--log-file", "-", "--timeout", "120", "--workers", "2", "--bind", "0.0.0.0:8080"]
