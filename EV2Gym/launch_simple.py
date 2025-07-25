#!/usr/bin/env python3
"""
Lanceur simple pour le dashboard EV2Gym
Installe automatiquement les dépendances et lance le dashboard
"""

import subprocess
import sys
import os
from pathlib import Path

def install_package(package):
    """Installe un package Python"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        return True
    except subprocess.CalledProcessError:
        return False

def check_and_install_dependencies():
    """Vérifie et installe les dépendances requises"""
    required_packages = [
        "streamlit",
        "pandas", 
        "numpy",
        "pyyaml"
    ]
    
    print("🔍 Vérification des dépendances...")
    
    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
            print(f"✅ {package} - OK")
        except ImportError:
            print(f"⚠️  {package} - Installation en cours...")
            if install_package(package):
                print(f"✅ {package} - Installé")
            else:
                print(f"❌ {package} - Échec de l'installation")
                return False
    
    return True

def check_ev2gym():
    """Vérifie si EV2Gym est disponible"""
    try:
        import ev2gym
        print("✅ EV2Gym - OK")
        return True
    except ImportError:
        print("⚠️  EV2Gym non trouvé")
        
        # Essayer d'installer depuis le répertoire local
        ev2gym_path = Path("EV2Gym")
        if ev2gym_path.exists():
            print("📦 Installation d'EV2Gym depuis le répertoire local...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", "-e", str(ev2gym_path)])
                print("✅ EV2Gym installé")
                return True
            except subprocess.CalledProcessError:
                print("❌ Échec de l'installation d'EV2Gym")
        
        return False

def launch_dashboard():
    """Lance le dashboard"""
    dashboard_file = "simple_dashboard.py"
    
    if not Path(dashboard_file).exists():
        print(f"❌ Fichier {dashboard_file} non trouvé")
        return False
    
    print("🚀 Lancement du dashboard...")
    print("🌐 Le dashboard va s'ouvrir dans votre navigateur")
    print("⏹️  Utilisez Ctrl+C pour arrêter")
    
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", dashboard_file])
        return True
    except KeyboardInterrupt:
        print("\n⏹️  Dashboard arrêté")
        return True
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def main():
    """Fonction principale"""
    print("🚗⚡ EV2Gym Simple Dashboard Launcher")
    print("=" * 40)
    
    # Vérifier et installer les dépendances
    if not check_and_install_dependencies():
        print("❌ Impossible d'installer toutes les dépendances")
        input("Appuyez sur Entrée pour quitter...")
        return
    
    # Vérifier EV2Gym
    if not check_ev2gym():
        print("⚠️  EV2Gym n'est pas disponible")
        print("💡 Pour installer EV2Gym:")
        print("   1. Téléchargez EV2Gym depuis GitHub")
        print("   2. Placez le dossier EV2Gym dans ce répertoire")
        print("   3. Ou installez avec: pip install ev2gym")
        
        response = input("\nContinuer quand même? (y/N): ")
        if response.lower() not in ['y', 'yes', 'oui']:
            return
    
    print("\n" + "=" * 40)
    
    # Lancer le dashboard
    if not launch_dashboard():
        input("Appuyez sur Entrée pour quitter...")

if __name__ == "__main__":
    main()
