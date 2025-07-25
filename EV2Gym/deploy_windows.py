#!/usr/bin/env python3
"""
Script de déploiement EV2Gym pour Windows

Lance le dashboard complet avec Docker, Gurobi, et entraînement IA
basé sur les données réelles du dossier data/.
"""

import subprocess
import sys
import os
import time
import json
from pathlib import Path
import webbrowser

def print_banner():
    """Affiche la bannière de démarrage"""
    print("🚗⚡ EV2Gym Enhanced Dashboard Deployment")
    print("=" * 50)
    print("🎯 Fonctionnalités:")
    print("  ✅ Dashboard interactif avec données réelles")
    print("  ✅ Agents MPC avec Gurobi (si licence disponible)")
    print("  ✅ Entraînement IA basé sur données Pays-Bas")
    print("  ✅ Monitoring avec Grafana + Prometheus")
    print("  ✅ Jupyter pour analyse avancée")
    print("  ✅ Base de données PostgreSQL + Redis")
    print("=" * 50)

def check_docker():
    """Vérifie que Docker est installé et fonctionne"""
    try:
        result = subprocess.run(['docker', '--version'], 
                              capture_output=True, text=True, check=True)
        print(f"✅ Docker détecté: {result.stdout.strip()}")
        
        result = subprocess.run(['docker-compose', '--version'], 
                              capture_output=True, text=True, check=True)
        print(f"✅ Docker Compose détecté: {result.stdout.strip()}")
        
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Docker ou Docker Compose non trouvé")
        print("💡 Installez Docker Desktop depuis: https://www.docker.com/products/docker-desktop")
        return False

def check_data():
    """Vérifie la présence des données"""
    data_path = Path("EV2Gym/ev2gym/data")
    
    if not data_path.exists():
        print("❌ Dossier de données non trouvé")
        return False
    
    required_files = [
        "Netherlands_day-ahead-2015-2024.csv",
        "ev_specs_v2g_enabled2024.json",
        "residential_loads.csv"
    ]
    
    missing_files = []
    for file in required_files:
        if not (data_path / file).exists():
            missing_files.append(file)
    
    if missing_files:
        print(f"⚠️  Fichiers de données manquants: {missing_files}")
    else:
        print("✅ Toutes les données requises sont présentes")
    
    return len(missing_files) == 0

def check_gurobi():
    """Vérifie la licence Gurobi"""
    if Path("gurobi.lic").exists():
        print("✅ Licence Gurobi trouvée - Agents MPC disponibles")
        return True
    else:
        print("⚠️  Licence Gurobi non trouvée - Agents heuristiques uniquement")
        print("💡 Pour obtenir Gurobi (gratuit académique):")
        print("   1. Créez un compte sur gurobi.com")
        print("   2. Téléchargez la licence académique")
        print("   3. Placez gurobi.lic dans ce répertoire")
        return False

def create_directories():
    """Crée les répertoires nécessaires"""
    directories = [
        "models", "exports", "logs", "notebooks",
        "prometheus", "grafana/dashboards", "grafana/datasources"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
    
    print("✅ Répertoires créés")

def setup_configuration():
    """Configure les fichiers de configuration"""
    
    # Configuration Prometheus
    prometheus_config = """
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']
  
  - job_name: 'ev2gym-dashboard'
    static_configs:
      - targets: ['ev2gym-dashboard:8501']
    metrics_path: '/metrics'
    scrape_interval: 30s
"""
    
    with open("prometheus/prometheus.yml", "w") as f:
        f.write(prometheus_config)
    
    # Configuration Grafana datasource
    grafana_datasource = """
apiVersion: 1

datasources:
  - name: EV2Gym PostgreSQL
    type: postgres
    url: ev2gym-db:5432
    database: ev2gym
    user: ev2gym
    secureJsonData:
      password: ev2gym_secure_password
    jsonData:
      sslmode: disable
      postgresVersion: 1500
"""
    
    with open("grafana/datasources/postgres.yml", "w") as f:
        f.write(grafana_datasource)
    
    # Script d'initialisation DB
    init_db_sql = """
-- Schéma pour EV2Gym
CREATE SCHEMA IF NOT EXISTS ev2gym;

-- Table des simulations
CREATE TABLE IF NOT EXISTS ev2gym.simulations (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    config JSONB NOT NULL,
    start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    end_time TIMESTAMP,
    status VARCHAR(50) DEFAULT 'running'
);

-- Table des métriques
CREATE TABLE IF NOT EXISTS ev2gym.metrics (
    id SERIAL PRIMARY KEY,
    simulation_id INTEGER REFERENCES ev2gym.simulations(id),
    step INTEGER NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    reward FLOAT,
    power_consumption FLOAT,
    ev_count INTEGER,
    metrics JSONB
);

-- Table des modèles IA
CREATE TABLE IF NOT EXISTS ev2gym.ai_models (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    model_type VARCHAR(100) NOT NULL,
    performance_metrics JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    model_path VARCHAR(500)
);

-- Index pour les performances
CREATE INDEX IF NOT EXISTS idx_metrics_simulation_step ON ev2gym.metrics(simulation_id, step);
CREATE INDEX IF NOT EXISTS idx_simulations_status ON ev2gym.simulations(status);
"""
    
    with open("init_db.sql", "w") as f:
        f.write(init_db_sql)
    
    print("✅ Fichiers de configuration créés")

def deploy_services():
    """Déploie tous les services Docker"""
    print("🚀 Démarrage du déploiement...")
    
    try:
        # Construire et démarrer les services
        cmd = [
            'docker-compose', '-f', 'docker-compose.dashboard.yml', 
            'up', '--build', '-d'
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print("✅ Services déployés avec succès")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur lors du déploiement: {e}")
        print(f"Sortie d'erreur: {e.stderr}")
        return False

def wait_for_services():
    """Attend que les services soient prêts"""
    print("⏳ Attente du démarrage des services...")
    
    services = {
        "Dashboard": "http://localhost:8501",
        "Grafana": "http://localhost:3000",
        "Prometheus": "http://localhost:9090",
        "Jupyter": "http://localhost:8888"
    }
    
    import requests
    
    for service, url in services.items():
        print(f"   Vérification de {service}...")
        
        for attempt in range(30):  # 30 tentatives = 5 minutes
            try:
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    print(f"   ✅ {service} prêt")
                    break
            except:
                pass
            
            time.sleep(10)
        else:
            print(f"   ⚠️  {service} pas encore prêt")

def show_final_info():
    """Affiche les informations finales"""
    print("\n🎉 Déploiement EV2Gym Terminé!")
    print("=" * 40)
    print("\n🌐 Services Disponibles:")
    print("📊 Dashboard Principal:     http://localhost:8501")
    print("📈 Grafana (Monitoring):    http://localhost:3000")
    print("   └─ Login: admin / ev2gym_admin")
    print("🔍 Prometheus (Métriques):  http://localhost:9090")
    print("📓 Jupyter (Analyse IA):    http://localhost:8888")
    print("   └─ Token: ev2gym_jupyter_token")
    
    print("\n🗄️ Bases de Données:")
    print("PostgreSQL: localhost:5432 (ev2gym/ev2gym_secure_password)")
    print("Redis:      localhost:6379 (password: ev2gym_redis_password)")
    
    print("\n🤖 Fonctionnalités IA:")
    print("✅ Entraînement basé sur données réelles")
    print("✅ Prédiction de stratégies optimales")
    print("✅ Analyse des prix de l'électricité")
    
    print("\n📚 Données Utilisées:")
    print("✅ Prix électricité Pays-Bas (2015-2024)")
    print("✅ Spécifications VE 2024")
    print("✅ Charges résidentielles réelles")
    
    print("\n📋 Commandes Utiles:")
    print("Arrêter:    docker-compose -f docker-compose.dashboard.yml down")
    print("Logs:       docker-compose -f docker-compose.dashboard.yml logs -f")
    print("Redémarrer: docker-compose -f docker-compose.dashboard.yml restart")

def open_dashboard():
    """Ouvre le dashboard dans le navigateur"""
    try:
        webbrowser.open("http://localhost:8501")
        print("🌐 Dashboard ouvert dans le navigateur")
    except:
        print("⚠️  Impossible d'ouvrir automatiquement le navigateur")
        print("   Ouvrez manuellement: http://localhost:8501")

def main():
    """Fonction principale"""
    print_banner()
    
    # Vérifications préliminaires
    if not check_docker():
        input("Appuyez sur Entrée pour quitter...")
        return
    
    data_ok = check_data()
    gurobi_ok = check_gurobi()
    
    if not data_ok:
        print("\n⚠️  Certaines données sont manquantes")
        response = input("Continuer quand même? (y/N): ")
        if response.lower() not in ['y', 'yes', 'oui']:
            return
    
    print(f"\n📊 Résumé:")
    print(f"   Données: {'✅' if data_ok else '⚠️'}")
    print(f"   Gurobi:  {'✅' if gurobi_ok else '⚠️'}")
    
    response = input("\n🚀 Démarrer le déploiement complet? (Y/n): ")
    if response.lower() in ['n', 'no', 'non']:
        return
    
    # Déploiement
    create_directories()
    setup_configuration()
    
    if deploy_services():
        wait_for_services()
        show_final_info()
        
        response = input("\n🌐 Ouvrir le dashboard? (Y/n): ")
        if response.lower() not in ['n', 'no', 'non']:
            open_dashboard()
    
    input("\nAppuyez sur Entrée pour quitter...")

if __name__ == "__main__":
    main()
