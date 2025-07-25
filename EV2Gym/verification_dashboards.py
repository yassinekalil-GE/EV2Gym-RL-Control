#!/usr/bin/env python3
"""
🔍 Script de Vérification des Dashboards EV2Gym

Vérifie que les dashboards 8506 et 8507 sont fonctionnels
"""

import os
import sys
from pathlib import Path
import importlib.util

def verify_file_exists(file_path, description):
    """Vérifie qu'un fichier existe"""
    if Path(file_path).exists():
        print(f"✅ {description}: {file_path}")
        return True
    else:
        print(f"❌ {description}: {file_path} - MANQUANT")
        return False

def verify_python_syntax(file_path):
    """Vérifie la syntaxe Python d'un fichier"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            code = f.read()
        compile(code, file_path, 'exec')
        print(f"✅ Syntaxe Python valide: {file_path}")
        return True
    except SyntaxError as e:
        print(f"❌ Erreur syntaxe Python: {file_path} - {e}")
        return False
    except Exception as e:
        print(f"⚠️ Erreur lecture: {file_path} - {e}")
        return False

def verify_imports(file_path):
    """Vérifie que les imports sont disponibles"""
    required_modules = ['streamlit', 'pandas', 'numpy', 'plotly']
    missing_modules = []
    
    for module in required_modules:
        try:
            importlib.import_module(module)
        except ImportError:
            missing_modules.append(module)
    
    if missing_modules:
        print(f"❌ Modules manquants pour {file_path}: {', '.join(missing_modules)}")
        return False
    else:
        print(f"✅ Tous les modules disponibles pour {file_path}")
        return True

def main():
    """Fonction principale de vérification"""
    
    print("🔍 VÉRIFICATION DES DASHBOARDS EV2GYM")
    print("=" * 50)
    
    # Vérification des fichiers principaux
    files_to_check = [
        ("professional_soc_power_dashboard.py", "Dashboard 8506 - SOC & Power"),
        ("professional_grid_impact_dashboard.py", "Dashboard 8507 - Grid Impact"),
        ("start_dashboard.bat", "Script de démarrage Windows"),
        ("requirements.txt", "Fichier des dépendances")
    ]
    
    all_files_ok = True
    for file_path, description in files_to_check:
        if not verify_file_exists(file_path, description):
            all_files_ok = False
    
    print("\n" + "=" * 50)
    
    # Vérification syntaxe Python
    python_files = [
        "professional_soc_power_dashboard.py",
        "professional_grid_impact_dashboard.py"
    ]
    
    syntax_ok = True
    for file_path in python_files:
        if Path(file_path).exists():
            if not verify_python_syntax(file_path):
                syntax_ok = False
        else:
            syntax_ok = False
    
    print("\n" + "=" * 50)
    
    # Vérification des imports
    imports_ok = True
    for file_path in python_files:
        if Path(file_path).exists():
            if not verify_imports(file_path):
                imports_ok = False
    
    print("\n" + "=" * 50)
    
    # Vérification dossier données
    data_path = Path("ev2gym/data")
    if data_path.exists():
        data_files = list(data_path.glob("*.csv")) + list(data_path.glob("*.json"))
        print(f"✅ Dossier données: {len(data_files)} fichiers trouvés")
        data_ok = True
    else:
        print("❌ Dossier données: ev2gym/data/ manquant")
        data_ok = False
    
    print("\n" + "=" * 50)
    print("📊 RÉSUMÉ DE LA VÉRIFICATION")
    print("=" * 50)
    
    if all_files_ok:
        print("✅ Fichiers principaux: TOUS PRÉSENTS")
    else:
        print("❌ Fichiers principaux: MANQUANTS")
    
    if syntax_ok:
        print("✅ Syntaxe Python: VALIDE")
    else:
        print("❌ Syntaxe Python: ERREURS")
    
    if imports_ok:
        print("✅ Modules Python: DISPONIBLES")
    else:
        print("❌ Modules Python: MANQUANTS")
        print("   💡 Installer avec: pip install streamlit plotly pandas numpy")
    
    if data_ok:
        print("✅ Données EV2Gym: PRÉSENTES")
    else:
        print("❌ Données EV2Gym: MANQUANTES")
    
    print("\n" + "=" * 50)
    
    if all_files_ok and syntax_ok and imports_ok and data_ok:
        print("🎉 VÉRIFICATION RÉUSSIE - DASHBOARDS PRÊTS !")
        print("\n🚀 Commandes de lancement:")
        print("   Dashboard 8506: start_dashboard.bat 8506")
        print("   Dashboard 8507: start_dashboard.bat 8507")
        print("\n🌐 URLs d'accès:")
        print("   SOC & Power: http://localhost:8506")
        print("   Grid Impact: http://localhost:8507")
        return True
    else:
        print("❌ VÉRIFICATION ÉCHOUÉE - PROBLÈMES DÉTECTÉS")
        print("\n🔧 Actions recommandées:")
        if not imports_ok:
            print("   1. Installer modules: pip install streamlit plotly pandas numpy")
        if not data_ok:
            print("   2. Vérifier dossier ev2gym/data/")
        if not all_files_ok or not syntax_ok:
            print("   3. Vérifier intégrité des fichiers dashboard")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
