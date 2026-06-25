# Utiliser une image de base légère
FROM python:3.11-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier uniquement requirements.txt d'abord pour profiter du cache Docker
COPY requirements.txt .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Retirer perl (non utilisé par l'application) pour réduire la surface de vulnérabilités
RUN apt-get remove -y --purge --allow-remove-essential perl-base perl && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/*

# Copier le reste du code de l'application
COPY app.py .

# Créer un utilisateur non-root et lui donner les droits sur /app
RUN useradd -m appuser && chown -R appuser /app
USER appuser

# Exposer le port utilisé par l'application
EXPOSE 5000

# Lancer l'application
CMD ["python", "app.py"]
