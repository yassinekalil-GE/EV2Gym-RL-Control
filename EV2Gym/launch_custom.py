#!/usr/bin/env python3
"""
Lanceur pour le dashboard personnalisé EV2Gym
"""

import subprocess
import sys
import os

def main():
    print("🚗⚡ Lancement du Dashboard Personnalisé EV2Gym")
    print("=" * 50)
    print("📊 Fonctionnalités:")
    print("  - Supervision complète du réseau")
    print("  - Monitoring des véhicules en temps réel")
    print("  - Contrôle manuel du nombre de VE")
    print("  - Visualisation des prix et économie")
    print("=" * 50)
    
    try:
        # Lancer le dashboard personnalisé
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            "custom_dashboard.py",
            "--server.port=8502",  # Port différent pour éviter les conflits
            "--server.headless=true"
        ])
    except KeyboardInterrupt:
        print("\n⏹️  Dashboard arrêté")
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    main()
