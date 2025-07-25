#!/usr/bin/env python3
"""
EV2Gym - Script d'Installation Automatique

Script d'installation interactive pour EV2Gym avec vérification des dépendances
et configuration de l'environnement.

Usage:
    python install.py
    python install.py --full  # Installation complète
    python install.py --minimal  # Installation minimale
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path


class EV2GymInstaller:
    """Installateur automatique pour EV2Gym"""
    
    def __init__(self):
        self.python_version = sys.version_info
        self.install_options = {
            "minimal": ["gymnasium>=0.29.0", "numpy>=1.21.0", "pandas>=1.3.0", 
                       "matplotlib>=3.5.0", "pyyaml>=6.0", "scipy>=1.7.0", "tqdm>=4.64.0"],
            "standard": ["gymnasium>=0.29.0", "numpy>=1.21.0", "pandas>=1.3.0", 
                        "matplotlib>=3.5.0", "pyyaml>=6.0", "scipy>=1.7.0", "tqdm>=4.64.0",
                        "seaborn>=0.11.0", "plotly>=5.0.0"],
            "full": ["gymnasium>=0.29.0", "numpy>=1.21.0", "pandas>=1.3.0", 
                    "matplotlib>=3.5.0", "pyyaml>=6.0", "scipy>=1.7.0", "tqdm>=4.64.0",
                    "seaborn>=0.11.0", "plotly>=5.0.0", "streamlit>=1.25.0", 
                    "jupyter>=1.0.0", "torch>=1.12.0", "stable-baselines3>=2.0.0"]
        }
    
    def display_banner(self):
        """Affiche la bannière d'installation"""
        print("=" * 60)
        print("🚗⚡ EV2Gym - Installation Automatique")
        print("=" * 60)
        print("Simulateur de Recharge Intelligente Vehicle-to-Grid")
        print()
    
    def check_python_version(self):
        """Vérifie la version de Python"""
        print("🐍 Vérification de la version Python...")
        
        if self.python_version < (3, 8):
            print(f"❌ Python {self.python_version.major}.{self.python_version.minor} détecté")
            print("   EV2Gym nécessite Python 3.8 ou supérieur")
            print("   Veuillez mettre à jour Python avant de continuer")
            return False
        else:
            print(f"✅ Python {self.python_version.major}.{self.python_version.minor}.{self.python_version.micro} détecté")
            return True
    
    def check_pip(self):
        """Vérifie que pip est disponible"""
        print("📦 Vérification de pip...")
        
        try:
            subprocess.run([sys.executable, "-m", "pip", "--version"], 
                          check=True, capture_output=True)
            print("✅ pip disponible")
            return True
        except subprocess.CalledProcessError:
            print("❌ pip non disponible")
            print("   Veuillez installer pip avant de continuer")
            return False
    
    def select_installation_type(self):
        """Permet à l'utilisateur de sélectionner le type d'installation"""
        print("\n📋 Sélection du type d'installation:")
        print()
        print("1. 🔧 Minimale    - Dépendances de base uniquement")
        print("2. 📊 Standard    - Inclut les outils de visualisation")
        print("3. 🚀 Complète    - Toutes les fonctionnalités (RL, Web, Jupyter)")
        print()
        
        while True:
            choice = input("Choisissez le type d'installation (1-3): ").strip()
            
            if choice == "1":
                return "minimal"
            elif choice == "2":
                return "standard"
            elif choice == "3":
                return "full"
            else:
                print("❌ Choix invalide, veuillez réessayer")
    
    def install_dependencies(self, install_type: str):
        """Installe les dépendances selon le type choisi"""
        packages = self.install_options[install_type]
        
        print(f"\n📦 Installation des dépendances ({install_type})...")
        print(f"   Packages à installer: {len(packages)}")
        
        # Mettre à jour pip
        print("   Mise à jour de pip...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], 
                          check=True, capture_output=True)
            print("   ✅ pip mis à jour")
        except subprocess.CalledProcessError as e:
            print(f"   ⚠️  Avertissement: Impossible de mettre à jour pip: {e}")
        
        # Installer les packages
        failed_packages = []
        
        for i, package in enumerate(packages, 1):
            print(f"   [{i}/{len(packages)}] Installation de {package}...", end=" ")
            
            try:
                subprocess.run([sys.executable, "-m", "pip", "install", package], 
                              check=True, capture_output=True)
                print("✅")
            except subprocess.CalledProcessError:
                print("❌")
                failed_packages.append(package)
        
        if failed_packages:
            print(f"\n⚠️  Packages non installés: {failed_packages}")
            print("   Vous pouvez les installer manuellement plus tard")
        else:
            print("\n✅ Toutes les dépendances installées avec succès!")
        
        return len(failed_packages) == 0
    
    def install_ev2gym(self):
        """Installe EV2Gym en mode développement"""
        print("\n🔧 Installation d'EV2Gym...")
        
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "-e", "."], 
                          check=True, capture_output=True)
            print("✅ EV2Gym installé en mode développement")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Erreur lors de l'installation d'EV2Gym: {e}")
            return False
    
    def create_directories(self):
        """Crée les répertoires nécessaires"""
        print("\n📁 Création des répertoires...")
        
        directories = [
            "./results",
            "./replay", 
            "./analysis_results",
            "./custom_configs"
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
            print(f"   ✅ {directory}")
    
    def test_installation(self):
        """Teste l'installation"""
        print("\n🧪 Test de l'installation...")
        
        try:
            # Test d'import
            print("   Test d'import des modules...", end=" ")
            import ev2gym
            from ev2gym.models.ev2gym_env import EV2Gym
            print("✅")
            
            # Test de création d'environnement
            print("   Test de création d'environnement...", end=" ")
            config_file = "ev2gym/example_config_files/V2GProfitMax.yaml"
            if os.path.exists(config_file):
                env = EV2Gym(config_file=config_file, generate_rnd_game=True)
                print("✅")
                return True
            else:
                print("❌ (fichier de config manquant)")
                return False
                
        except Exception as e:
            print(f"❌ ({e})")
            return False
    
    def display_next_steps(self, install_type: str):
        """Affiche les prochaines étapes"""
        print("\n" + "=" * 60)
        print("🎉 Installation Terminée!")
        print("=" * 60)
        
        print("\n🚀 Prochaines étapes:")
        print()
        print("1. 📖 Lire la documentation:")
        print("   cat README.md")
        print()
        print("2. 🎯 Tester avec le script de démonstration:")
        print("   python tools/demo.py --config V2GProfitMax --agent smart")
        print()
        print("3. 🖥️  Utiliser l'interface CLI interactive:")
        print("   python tools/cli.py")
        print()
        
        if install_type in ["standard", "full"]:
            print("4. 📊 Ouvrir le notebook de démonstration:")
            print("   jupyter notebook notebooks/EV2Gym_Demo.ipynb")
            print()
        
        if install_type == "full":
            print("5. 🌐 Lancer l'interface web:")
            print("   streamlit run tools/web_app.py")
            print()
        
        print("📚 Documentation complète disponible dans README.md")
        print("🐛 Problèmes? Consultez les issues GitHub")
    
    def run_installation(self, install_type: str = None):
        """Lance le processus d'installation complet"""
        self.display_banner()
        
        # Vérifications préliminaires
        if not self.check_python_version():
            return False
        
        if not self.check_pip():
            return False
        
        # Sélection du type d'installation
        if install_type is None:
            install_type = self.select_installation_type()
        
        # Installation
        success = True
        success &= self.install_dependencies(install_type)
        success &= self.install_ev2gym()
        
        # Configuration
        self.create_directories()
        
        # Test
        if success:
            success &= self.test_installation()
        
        # Finalisation
        if success:
            self.display_next_steps(install_type)
            print("\n✅ Installation réussie!")
        else:
            print("\n❌ Installation incomplète. Consultez les messages d'erreur ci-dessus.")
        
        return success


def main():
    """Fonction principale"""
    parser = argparse.ArgumentParser(description="EV2Gym - Installation Automatique")
    
    parser.add_argument("--minimal", action="store_true",
                       help="Installation minimale")
    parser.add_argument("--full", action="store_true", 
                       help="Installation complète")
    parser.add_argument("--standard", action="store_true",
                       help="Installation standard")
    
    args = parser.parse_args()
    
    # Déterminer le type d'installation
    install_type = None
    if args.minimal:
        install_type = "minimal"
    elif args.full:
        install_type = "full"
    elif args.standard:
        install_type = "standard"
    
    # Lancer l'installation
    installer = EV2GymInstaller()
    success = installer.run_installation(install_type)
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
