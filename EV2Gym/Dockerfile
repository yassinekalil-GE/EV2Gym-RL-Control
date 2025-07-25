# Dockerfile pour EV2Gym Dashboard
FROM python:3.9-slim

# Métadonnées
LABEL maintainer="EV2Gym Team"
LABEL description="Real-Time EV Behavior Dashboard with RL/MPC/Heuristics"
LABEL version="1.0"

# Variables d'environnement
ENV PYTHONUNBUFFERED=1
ENV STREAMLIT_SERVER_PORT=8520
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Répertoire de travail
WORKDIR /app

# Installation des dépendances système
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copie des fichiers requirements
COPY requirements.txt .

# Installation des dépendances Python
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copie du code source
COPY . .

# Création des répertoires nécessaires
RUN mkdir -p /app/models /app/logs /app/data

# Permissions
RUN chmod +x realtime_ev_dashboard.py

# Port exposé
EXPOSE 8520

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8520/_stcore/health || exit 1

# Commande de démarrage
CMD ["streamlit", "run", "realtime_ev_dashboard.py", "--server.port=8520", "--server.address=0.0.0.0", "--server.headless=true"]
