#!/usr/bin/env python3
"""
Déploiement automatique EV2Gym sans interaction utilisateur
"""

import subprocess
import sys
import os
import time
from pathlib import Path

def setup_and_deploy():
    """Configuration et déploiement automatique"""
    
    print("🚗⚡ EV2Gym Auto-Deploy")
    print("=" * 30)
    
    # Créer les répertoires
    directories = [
        "models", "exports", "logs", "notebooks",
        "prometheus", "grafana/dashboards", "grafana/datasources"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
    print("✅ Répertoires créés")
    
    # Configuration Prometheus
    prometheus_config = """global:
  scrape_interval: 15s
scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']"""
    
    with open("prometheus/prometheus.yml", "w") as f:
        f.write(prometheus_config)
    
    # Configuration Grafana
    grafana_datasource = """apiVersion: 1
datasources:
  - name: EV2Gym PostgreSQL
    type: postgres
    url: ev2gym-db:5432
    database: ev2gym
    user: ev2gym
    secureJsonData:
      password: ev2gym_secure_password"""
    
    with open("grafana/datasources/postgres.yml", "w") as f:
        f.write(grafana_datasource)
    
    # Script DB
    init_db = """CREATE SCHEMA IF NOT EXISTS ev2gym;
CREATE TABLE IF NOT EXISTS ev2gym.simulations (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    config JSONB NOT NULL,
    start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);"""
    
    with open("init_db.sql", "w") as f:
        f.write(init_db)
    
    print("✅ Configuration créée")
    
    # Vérifier Docker
    try:
        subprocess.run(['docker', '--version'], check=True, capture_output=True)
        print("✅ Docker disponible")
    except:
        print("❌ Docker non trouvé")
        return False
    
    # Déployer avec Docker Compose
    try:
        print("🚀 Démarrage des services...")
        
        # Arrêter les services existants
        subprocess.run([
            'docker-compose', '-f', 'docker-compose.dashboard.yml', 'down'
        ], capture_output=True)
        
        # Démarrer les nouveaux services
        result = subprocess.run([
            'docker-compose', '-f', 'docker-compose.dashboard.yml', 
            'up', '--build', '-d'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Services démarrés")
            
            # Attendre un peu
            print("⏳ Initialisation...")
            time.sleep(30)
            
            print("\n🎉 Déploiement Terminé!")
            print("=" * 25)
            print("📊 Dashboard:    http://localhost:8501")
            print("📈 Grafana:      http://localhost:3000")
            print("🔍 Prometheus:   http://localhost:9090")
            print("📓 Jupyter:      http://localhost:8888")
            print("\n🌐 Ouvrez http://localhost:8501 dans votre navigateur")
            
            return True
        else:
            print(f"❌ Erreur: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur de déploiement: {e}")
        return False

if __name__ == "__main__":
    setup_and_deploy()
