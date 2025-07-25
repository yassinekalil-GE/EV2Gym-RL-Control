#!/bin/bash

# Script de démarrage EV2Gym Dashboard
# Usage: ./start_dashboard.sh [local|docker]

set -e

echo "🚗⚡ EV2Gym Real-Time Dashboard Launcher"
echo "========================================"

# Mode de démarrage
MODE=${1:-local}

case $MODE in
    "local")
        echo "🔧 Démarrage en mode LOCAL"
        echo "Vérification des dépendances..."
        
        # Vérifier Python
        if ! command -v python3 &> /dev/null; then
            echo "❌ Python3 non trouvé. Veuillez l'installer."
            exit 1
        fi
        
        # Vérifier pip
        if ! command -v pip &> /dev/null; then
            echo "❌ pip non trouvé. Veuillez l'installer."
            exit 1
        fi
        
        # Installer les dépendances
        echo "📦 Installation des dépendances..."
        pip install -r requirements.txt
        
        # Démarrer le dashboard
        echo "🚀 Démarrage du dashboard..."
        echo "📍 URL: http://localhost:8520"
        streamlit run realtime_ev_dashboard.py --server.port=8520
        ;;
        
    "docker")
        echo "🐳 Démarrage en mode DOCKER"
        
        # Vérifier Docker
        if ! command -v docker &> /dev/null; then
            echo "❌ Docker non trouvé. Veuillez l'installer."
            exit 1
        fi
        
        # Vérifier Docker Compose
        if ! command -v docker-compose &> /dev/null; then
            echo "❌ Docker Compose non trouvé. Veuillez l'installer."
            exit 1
        fi
        
        # Construire et démarrer
        echo "🔨 Construction de l'image Docker..."
        docker-compose build
        
        echo "🚀 Démarrage du conteneur..."
        docker-compose up -d
        
        echo "✅ Dashboard démarré avec succès !"
        echo "📍 URL: http://localhost:8520"
        echo "📊 Logs: docker-compose logs -f"
        echo "🛑 Arrêt: docker-compose down"
        ;;
        
    *)
        echo "❌ Mode non reconnu: $MODE"
        echo "Usage: $0 [local|docker]"
        echo "  local  - Démarrage local avec Python"
        echo "  docker - Démarrage avec Docker"
        exit 1
        ;;
esac

echo ""
echo "🎉 Dashboard EV2Gym prêt !"
echo "🔗 Ouvrez http://localhost:8520 dans votre navigateur"
