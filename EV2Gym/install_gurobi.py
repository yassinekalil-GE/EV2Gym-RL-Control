#!/usr/bin/env python3
"""
Script d'installation automatique de Gurobi pour EV2Gym

Installe Gurobi et configure la licence pour utiliser les agents MPC optimaux.
"""

import subprocess
import sys
import os
import requests
import zipfile
from pathlib import Path
import webbrowser

def print_banner():
    """Affiche la bannière"""
    print("🎯 Installation Gurobi pour EV2Gym")
    print("=" * 40)
    print("Gurobi est requis pour les agents MPC optimaux:")
    print("- OCMF_V2G (Optimal Charging Management)")
    print("- eMPC_V2G (Economic Model Predictive Control)")
    print("- V2GProfitMax (Oracle optimal)")
    print("=" * 40)

def install_gurobipy():
    """Installe le package Python Gurobi"""
    print("📦 Installation de gurobipy...")
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "gurobipy"])
        print("✅ gurobipy installé avec succès")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur lors de l'installation: {e}")
        return False

def check_gurobi_installation():
    """Vérifie si Gurobi est installé et fonctionnel"""
    try:
        import gurobipy as gp
        print("✅ gurobipy importé avec succès")
        
        # Tester la création d'un modèle
        try:
            model = gp.Model("test")
            model.dispose()
            print("✅ Licence Gurobi valide - Modèle de test créé")
            return True, "valid_license"
        except gp.GurobiError as e:
            if "No license" in str(e) or "license" in str(e).lower():
                print("⚠️  gurobipy installé mais licence manquante")
                return True, "no_license"
            else:
                print(f"⚠️  Erreur Gurobi: {e}")
                return True, "error"
    except ImportError:
        print("❌ gurobipy non installé")
        return False, "not_installed"

def get_academic_license_info():
    """Affiche les informations pour obtenir une licence académique"""
    print("\n🎓 Licence Académique Gurobi (GRATUITE)")
    print("=" * 45)
    print("1. Créez un compte sur: https://www.gurobi.com/academia/")
    print("2. Vérifiez votre statut académique avec votre email universitaire")
    print("3. Téléchargez la licence académique")
    print("4. Placez le fichier gurobi.lic dans ce répertoire")
    print("\n💡 La licence académique est gratuite et permet:")
    print("   - Modèles jusqu'à 2000 variables")
    print("   - Parfait pour la recherche et l'éducation")
    print("   - Utilisation sur un seul ordinateur")

def get_commercial_license_info():
    """Affiche les informations pour une licence commerciale"""
    print("\n💼 Licence Commerciale Gurobi")
    print("=" * 35)
    print("1. Visitez: https://www.gurobi.com/products/gurobi-optimizer/")
    print("2. Demandez un essai gratuit de 30 jours")
    print("3. Ou achetez une licence complète")
    print("\n💰 Options commerciales:")
    print("   - Essai gratuit 30 jours")
    print("   - Licence nommée utilisateur")
    print("   - Licence flottante pour équipes")

def setup_license_file():
    """Guide pour configurer le fichier de licence"""
    print("\n📄 Configuration du Fichier de Licence")
    print("=" * 42)
    
    # Vérifier si le fichier existe déjà
    license_files = [
        "gurobi.lic",
        Path.home() / "gurobi.lic",
        Path.home() / ".gurobi" / "gurobi.lic"
    ]
    
    existing_license = None
    for license_file in license_files:
        if Path(license_file).exists():
            existing_license = license_file
            break
    
    if existing_license:
        print(f"✅ Fichier de licence trouvé: {existing_license}")
        
        # Copier vers le répertoire local si nécessaire
        local_license = Path("gurobi.lic")
        if not local_license.exists() and existing_license != local_license:
            try:
                import shutil
                shutil.copy2(existing_license, local_license)
                print(f"✅ Licence copiée vers: {local_license}")
            except Exception as e:
                print(f"⚠️  Impossible de copier la licence: {e}")
        
        return True
    else:
        print("❌ Aucun fichier de licence trouvé")
        print("\n📋 Étapes pour configurer la licence:")
        print("1. Obtenez votre fichier gurobi.lic")
        print("2. Placez-le dans l'un de ces emplacements:")
        for location in license_files:
            print(f"   - {location}")
        print("3. Relancez ce script pour vérifier")
        
        return False

def test_mpc_agents():
    """Teste les agents MPC avec Gurobi"""
    print("\n🧪 Test des Agents MPC")
    print("=" * 25)
    
    try:
        # Tester l'import des agents MPC
        sys.path.append("EV2Gym")
        
        try:
            from ev2gym.baselines.mpc.ocmf_mpc import OCMF_V2G
            print("✅ OCMF_V2G importé")
        except ImportError as e:
            print(f"❌ OCMF_V2G: {e}")
        
        try:
            from ev2gym.baselines.mpc.eMPC_v2 import eMPC_V2G_v2
            print("✅ eMPC_V2G importé")
        except ImportError as e:
            print(f"❌ eMPC_V2G: {e}")
        
        try:
            from ev2gym.baselines.mpc.V2GProfitMax import V2GProfitMaxOracle
            print("✅ V2GProfitMax importé")
        except ImportError as e:
            print(f"❌ V2GProfitMax: {e}")
        
        print("\n🎉 Agents MPC prêts à utiliser!")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        return False

def create_gurobi_test_script():
    """Crée un script de test Gurobi"""
    test_script = """
import gurobipy as gp
from gurobipy import GRB

def test_gurobi():
    try:
        # Créer un modèle simple
        model = gp.Model("test_ev_charging")
        
        # Variables de test (puissance de charge)
        charge_power = model.addVar(lb=0, ub=11, name="charge_power")
        
        # Fonction objectif simple
        model.setObjective(charge_power, GRB.MAXIMIZE)
        
        # Optimiser
        model.optimize()
        
        if model.status == GRB.OPTIMAL:
            print(f"✅ Test Gurobi réussi!")
            print(f"   Solution optimale: {charge_power.x:.2f} kW")
            return True
        else:
            print(f"⚠️  Statut d'optimisation: {model.status}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur de test: {e}")
        return False
    finally:
        if 'model' in locals():
            model.dispose()

if __name__ == "__main__":
    test_gurobi()
"""
    
    with open("test_gurobi.py", "w") as f:
        f.write(test_script)
    
    print("📝 Script de test créé: test_gurobi.py")

def main():
    """Fonction principale"""
    print_banner()
    
    # Vérifier l'installation actuelle
    installed, status = check_gurobi_installation()
    
    if not installed:
        print("\n📦 Installation de gurobipy...")
        if not install_gurobipy():
            print("❌ Échec de l'installation")
            return
        
        # Revérifier après installation
        installed, status = check_gurobi_installation()
    
    if status == "valid_license":
        print("\n🎉 Gurobi est complètement configuré!")
        
        # Tester les agents MPC
        if test_mpc_agents():
            print("\n✅ Tous les agents MPC sont prêts!")
            print("\n🚀 Vous pouvez maintenant utiliser:")
            print("   - OCMF_V2G pour l'optimisation V2G")
            print("   - eMPC_V2G pour le contrôle économique")
            print("   - V2GProfitMax pour la solution optimale")
        
    elif status == "no_license":
        print("\n📄 Configuration de la licence requise...")
        
        if not setup_license_file():
            print("\n🎓 Options pour obtenir une licence:")
            
            choice = input("\nChoisissez une option:\n1) Licence académique (gratuite)\n2) Licence commerciale\n3) Continuer sans Gurobi\nVotre choix (1-3): ")
            
            if choice == "1":
                get_academic_license_info()
                webbrowser.open("https://www.gurobi.com/academia/")
            elif choice == "2":
                get_commercial_license_info()
                webbrowser.open("https://www.gurobi.com/products/gurobi-optimizer/")
            else:
                print("\n⚠️  Continuez avec les agents heuristiques uniquement")
                print("   (ChargeAsFastAsPossible, RandomAgent, RoundRobin)")
    
    # Créer un script de test
    create_gurobi_test_script()
    
    print("\n📋 Résumé:")
    print(f"   gurobipy: {'✅' if installed else '❌'}")
    print(f"   Licence: {'✅' if status == 'valid_license' else '❌'}")
    print(f"   Agents MPC: {'✅' if status == 'valid_license' else '❌'}")
    
    if status != "valid_license":
        print("\n💡 Pour activer les agents MPC:")
        print("   1. Obtenez une licence Gurobi")
        print("   2. Placez gurobi.lic dans ce répertoire")
        print("   3. Relancez ce script")
    
    input("\nAppuyez sur Entrée pour quitter...")

if __name__ == "__main__":
    main()
