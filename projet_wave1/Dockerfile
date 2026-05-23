# Image de base Python
FROM python:3.11-slim

# Dossier de travail dans le conteneur
WORKDIR /app

# Installer les dépendances système
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copier et installer les dépendances Python
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copier tout le code
COPY . .

# Exposer le port 8000
EXPOSE 8000

# Lancer le serveur Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
