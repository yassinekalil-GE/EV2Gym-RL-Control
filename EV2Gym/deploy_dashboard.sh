#!/bin/bash

# EV2Gym Dashboard Deployment Script
# Automatise le déploiement du dashboard avec Docker

set -e  # Arrêter en cas d'erreur

echo "🚗⚡ EV2Gym Dashboard Deployment Script"
echo "======================================"

# Couleurs pour les messages
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Fonctions utilitaires
log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Vérifier que Docker est installé
check_docker() {
    if ! command -v docker &> /dev/null; then
        log_error "Docker n'est pas installé"
        echo "Installez Docker depuis: https://docs.docker.com/get-docker/"
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        log_error "Docker Compose n'est pas installé"
        echo "Installez Docker Compose depuis: https://docs.docker.com/compose/install/"
        exit 1
    fi
    
    log_success "Docker et Docker Compose sont disponibles"
}

# Vérifier les fichiers requis
check_files() {
    required_files=(
        "Dockerfile.dashboard"
        "docker-compose.dashboard.yml"
        "ev2gym_dashboard.py"
        "requirements_dashboard.txt"
    )
    
    for file in "${required_files[@]}"; do
        if [[ ! -f "$file" ]]; then
            log_error "Fichier requis manquant: $file"
            exit 1
        fi
    done
    
    log_success "Tous les fichiers requis sont présents"
}

# Créer les répertoires nécessaires
create_directories() {
    log_info "Création des répertoires..."
    
    mkdir -p data
    mkdir -p custom_configs
    mkdir -p exports
    
    log_success "Répertoires créés"
}

# Construire l'image Docker
build_image() {
    log_info "Construction de l'image Docker..."
    
    docker build -f Dockerfile.dashboard -t ev2gym-dashboard:latest .
    
    if [[ $? -eq 0 ]]; then
        log_success "Image Docker construite avec succès"
    else
        log_error "Échec de la construction de l'image Docker"
        exit 1
    fi
}

# Démarrer les services
start_services() {
    log_info "Démarrage des services..."
    
    docker-compose -f docker-compose.dashboard.yml up -d
    
    if [[ $? -eq 0 ]]; then
        log_success "Services démarrés avec succès"
    else
        log_error "Échec du démarrage des services"
        exit 1
    fi
}

# Vérifier la santé des services
check_health() {
    log_info "Vérification de la santé des services..."
    
    # Attendre que le service soit prêt
    sleep 10
    
    # Vérifier le dashboard
    if curl -f http://localhost:8501/_stcore/health &> /dev/null; then
        log_success "Dashboard accessible sur http://localhost:8501"
    else
        log_warning "Dashboard pas encore prêt, vérifiez les logs avec:"
        echo "docker-compose -f docker-compose.dashboard.yml logs ev2gym-dashboard"
    fi
}

# Afficher les informations de déploiement
show_info() {
    echo ""
    echo "🎉 Déploiement EV2Gym Complet Terminé!"
    echo "======================================"
    echo ""
    echo "🌐 **Services Disponibles:**"
    echo "📊 Dashboard Principal:     http://localhost:8501"
    echo "📈 Grafana (Monitoring):    http://localhost:3000 (admin/ev2gym_admin)"
    echo "🔍 Prometheus (Métriques):  http://localhost:9090"
    echo "📓 Jupyter (Analyse IA):    http://localhost:8888 (token: ev2gym_jupyter_token)"
    echo ""
    echo "🗄️  **Bases de Données:**"
    echo "PostgreSQL: localhost:5432 (ev2gym/ev2gym_secure_password)"
    echo "Redis:      localhost:6379 (password: ev2gym_redis_password)"
    echo ""
    echo "🤖 **Fonctionnalités IA:**"
    echo "✅ Entraînement de modèles basé sur données réelles"
    echo "✅ Prédiction de stratégies de charge optimales"
    echo "✅ Analyse prédictive des prix de l'électricité"
    echo ""
    echo "⚡ **Agents MPC avec Gurobi:**"
    if [[ -f "gurobi.lic" ]]; then
        echo "✅ Licence Gurobi détectée - Agents MPC disponibles"
    else
        echo "⚠️  Licence Gurobi non trouvée - Agents heuristiques uniquement"
    fi
    echo ""
    echo "📋 **Commandes Utiles:**"
    echo "  - Logs dashboard:    docker-compose -f docker-compose.dashboard.yml logs -f ev2gym-dashboard"
    echo "  - Logs tous services: docker-compose -f docker-compose.dashboard.yml logs -f"
    echo "  - Arrêter:           docker-compose -f docker-compose.dashboard.yml down"
    echo "  - Redémarrer:        docker-compose -f docker-compose.dashboard.yml restart"
    echo "  - Reconstruire:      docker-compose -f docker-compose.dashboard.yml up --build -d"
    echo ""
    echo "📚 **Données Utilisées:**"
    echo "  - Prix électricité Pays-Bas (2015-2024)"
    echo "  - Spécifications VE 2024 (Tesla, BMW, Audi, etc.)"
    echo "  - Charges résidentielles réelles"
    echo "  - Génération PV et distribution d'arrivée"
    echo ""
}

# Menu principal
show_menu() {
    echo "Choisissez une option:"
    echo "1) 🚀 Déploiement complet avec IA et Gurobi (recommandé)"
    echo "2) 🔨 Construire les images seulement"
    echo "3) ▶️  Démarrer les services existants"
    echo "4) ⏹️  Arrêter les services"
    echo "5) 📋 Voir les logs"
    echo "6) 🤖 Entraîner les modèles IA"
    echo "7) 🧹 Nettoyer (arrêter et supprimer)"
    echo "8) 👋 Quitter"
    echo ""
    read -p "Votre choix (1-8): " choice
}

# Installer Gurobi (si licence disponible)
setup_gurobi() {
    log_info "Configuration de Gurobi..."

    if [[ -f "gurobi.lic" ]]; then
        log_success "Licence Gurobi trouvée"
    else
        log_warning "Licence Gurobi non trouvée"
        echo "Pour utiliser les agents MPC optimaux:"
        echo "1. Obtenez une licence Gurobi (gratuite pour l'académique)"
        echo "2. Placez le fichier gurobi.lic dans ce répertoire"
        echo "3. Relancez le déploiement"
    fi
}

# Initialiser la base de données
init_database() {
    log_info "Initialisation de la base de données..."

    cat > init_db.sql << EOF
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
EOF

    log_success "Script d'initialisation DB créé"
}

# Configuration Prometheus
setup_prometheus() {
    log_info "Configuration de Prometheus..."

    mkdir -p prometheus

    cat > prometheus/prometheus.yml << EOF
global:
  scrape_interval: 15s
  evaluation_interval: 15s

rule_files:
  # - "first_rules.yml"

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  - job_name: 'ev2gym-dashboard'
    static_configs:
      - targets: ['ev2gym-dashboard:8501']
    metrics_path: '/metrics'
    scrape_interval: 30s
EOF

    log_success "Configuration Prometheus créée"
}

# Configuration Grafana
setup_grafana() {
    log_info "Configuration de Grafana..."

    mkdir -p grafana/dashboards grafana/datasources

    # Datasource PostgreSQL
    cat > grafana/datasources/postgres.yml << EOF
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
EOF

    # Dashboard de base
    cat > grafana/dashboards/ev2gym.json << EOF
{
  "dashboard": {
    "id": null,
    "title": "EV2Gym Dashboard",
    "tags": ["ev2gym"],
    "timezone": "browser",
    "panels": [
      {
        "id": 1,
        "title": "Simulations Actives",
        "type": "stat",
        "targets": [
          {
            "expr": "SELECT COUNT(*) FROM ev2gym.simulations WHERE status = 'running'",
            "format": "table"
          }
        ]
      }
    ],
    "time": {
      "from": "now-1h",
      "to": "now"
    },
    "refresh": "30s"
  }
}
EOF

    log_success "Configuration Grafana créée"
}

# Créer des notebooks d'exemple
create_notebooks() {
    log_info "Création des notebooks d'exemple..."

    mkdir -p notebooks

    cat > notebooks/EV2Gym_Analysis.ipynb << EOF
{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# EV2Gym Data Analysis\\n",
    "\\n",
    "Notebook pour l'analyse des données EV2Gym et l'entraînement de modèles IA."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "import pandas as pd\\n",
    "import numpy as np\\n",
    "import plotly.express as px\\n",
    "import plotly.graph_objects as go\\n",
    "from sklearn.ensemble import RandomForestRegressor\\n",
    "\\n",
    "# Charger les données réelles\\n",
    "prices_df = pd.read_csv('data/Netherlands_day-ahead-2015-2024.csv')\\n",
    "print(f'Données de prix chargées: {len(prices_df)} points')\\n",
    "\\n",
    "# Afficher les premières lignes\\n",
    "prices_df.head()"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
EOF

    log_success "Notebooks d'exemple créés"
}

# Traitement des choix du menu
handle_choice() {
    case $choice in
        1)
            log_info "Déploiement complet avec IA et Gurobi..."
            check_docker
            check_files
            create_directories
            setup_gurobi
            init_database
            setup_prometheus
            setup_grafana
            create_notebooks
            build_image
            start_services
            check_health
            show_info
            ;;
        2)
            log_info "Construction des images..."
            check_docker
            check_files
            build_image
            ;;
        3)
            log_info "Démarrage des services..."
            check_docker
            start_services
            check_health
            ;;
        4)
            log_info "Arrêt des services..."
            docker-compose -f docker-compose.dashboard.yml down
            log_success "Services arrêtés"
            ;;
        5)
            log_info "Affichage des logs..."
            docker-compose -f docker-compose.dashboard.yml logs -f
            ;;
        6)
            log_info "Entraînement des modèles IA..."
            train_ai_models
            ;;
        7)
            log_warning "Nettoyage complet..."
            read -p "Êtes-vous sûr? (y/N): " confirm
            if [[ $confirm =~ ^[Yy]$ ]]; then
                docker-compose -f docker-compose.dashboard.yml down -v --rmi all
                log_success "Nettoyage terminé"
            fi
            ;;
        8)
            log_info "Au revoir!"
            exit 0
            ;;
        *)
            log_error "Choix invalide"
            ;;
    esac
}

# Entraînement des modèles IA
train_ai_models() {
    log_info "Lancement de l'entraînement des modèles IA..."

    if docker ps | grep -q ev2gym-dashboard; then
        docker exec ev2gym-dashboard python ai_training_module.py
        log_success "Entraînement terminé"
    else
        log_error "Le dashboard n'est pas en cours d'exécution"
    fi
}

# Boucle principale
main() {
    while true; do
        echo ""
        show_menu
        handle_choice
        echo ""
        read -p "Appuyez sur Entrée pour continuer..."
    done
}

# Vérifier si le script est exécuté directement
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main
fi
