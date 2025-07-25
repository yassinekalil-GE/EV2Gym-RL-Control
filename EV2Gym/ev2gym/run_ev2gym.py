#!/usr/bin/env python3
"""
EV2Gym - Script de Lancement Rapide

Script principal pour lancer rapidement EV2Gym avec différentes interfaces.
Point d'entrée unique pour tous les outils.

Usage:
    python run_ev2gym.py demo --config V2GProfitMax --agent smart
    python run_ev2gym.py cli
    python run_ev2gym.py web
    python run_ev2gym.py notebook
    python run_ev2gym.py analyze --compare_agents
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path


def display_banner():
    """Affiche la bannière principale"""
    print("=" * 60)
    print("🚗⚡ EV2Gym - Simulateur de Recharge Intelligente V2G")
    print("=" * 60)
    print("Plateforme de simulation pour la recherche en recharge intelligente")
    print()


def check_installation():
    """Vérifie que EV2Gym est correctement installé"""
    try:
        import ev2gym
        from ev2gym.models.ev2gym_env import EV2Gym
        return True
    except ImportError:
        print("❌ EV2Gym n'est pas installé ou mal configuré")
        print("   Lancez: python install.py")
        return False


def run_demo(args):
    """Lance le script de démonstration"""
    print("🎯 Lancement du script de démonstration...")
    
    cmd = [sys.executable, "tools/demo.py"]
    
    if args.config:
        cmd.extend(["--config", args.config])
    if args.agent:
        cmd.extend(["--agent", args.agent])
    if args.steps:
        cmd.extend(["--steps", str(args.steps)])
    if args.visualize:
        cmd.append("--visualize")
    if args.save:
        cmd.append("--save")
    
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur lors de l'exécution: {e}")
    except FileNotFoundError:
        print("❌ Script de démonstration non trouvé")


def run_cli(args):
    """Lance l'interface CLI"""
    print("🖥️  Lancement de l'interface CLI...")
    
    cmd = [sys.executable, "tools/cli.py"]
    
    if args.batch:
        cmd.append("--batch")
    
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur lors de l'exécution: {e}")
    except FileNotFoundError:
        print("❌ Interface CLI non trouvée")


def run_web(args):
    """Lance l'interface web Streamlit"""
    print("🌐 Lancement de l'interface web...")
    print("   L'interface s'ouvrira dans votre navigateur")
    
    try:
        # Vérifier que Streamlit est installé
        subprocess.run([sys.executable, "-c", "import streamlit"], 
                      check=True, capture_output=True)
        
        # Lancer Streamlit
        cmd = ["streamlit", "run", "tools/web_app.py"]
        subprocess.run(cmd, check=True)
        
    except subprocess.CalledProcessError:
        print("❌ Streamlit n'est pas installé")
        print("   Installez-le avec: pip install streamlit")
    except FileNotFoundError:
        print("❌ Interface web non trouvée ou Streamlit non installé")


def run_notebook(args):
    """Lance le notebook Jupyter"""
    print("📓 Lancement du notebook Jupyter...")
    
    try:
        # Vérifier que Jupyter est installé
        subprocess.run([sys.executable, "-c", "import jupyter"], 
                      check=True, capture_output=True)
        
        # Lancer Jupyter
        notebook_path = "notebooks/EV2Gym_Demo.ipynb"
        if os.path.exists(notebook_path):
            cmd = ["jupyter", "notebook", notebook_path]
            subprocess.run(cmd, check=True)
        else:
            print("❌ Notebook de démonstration non trouvé")
            print("   Lancez: jupyter notebook")
            
    except subprocess.CalledProcessError:
        print("❌ Jupyter n'est pas installé")
        print("   Installez-le avec: pip install jupyter")
    except FileNotFoundError:
        print("❌ Jupyter non trouvé")


def run_analysis(args):
    """Lance les outils d'analyse"""
    print("📊 Lancement des outils d'analyse...")
    
    cmd = [sys.executable, "tools/analysis.py"]
    
    if args.replay_path:
        cmd.extend(["--replay_path", args.replay_path])
    if args.compare_agents:
        cmd.append("--compare_agents")
    if args.config:
        cmd.extend(["--config", args.config])
    if args.agents:
        cmd.extend(["--agents"] + args.agents)
    if args.generate_report:
        cmd.append("--generate_report")
    
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur lors de l'analyse: {e}")
    except FileNotFoundError:
        print("❌ Outils d'analyse non trouvés")


def show_help():
    """Affiche l'aide générale"""
    print("🚀 Commandes disponibles:")
    print()
    print("📋 INTERFACES:")
    print("  demo      - Script de démonstration simple")
    print("  cli       - Interface en ligne de commande interactive")
    print("  web       - Interface web Streamlit")
    print("  notebook  - Notebook Jupyter de démonstration")
    print("  analyze   - Outils d'analyse des résultats")
    print()
    print("⚙️  UTILITAIRES:")
    print("  install   - Lancer l'installation")
    print("  test      - Tester l'installation")
    print("  help      - Afficher cette aide")
    print()
    print("📖 EXEMPLES:")
    print("  python run_ev2gym.py demo --config V2GProfitMax --agent smart")
    print("  python run_ev2gym.py cli")
    print("  python run_ev2gym.py web")
    print("  python run_ev2gym.py analyze --compare_agents")
    print()
    print("Pour plus d'aide sur une commande:")
    print("  python run_ev2gym.py <commande> --help")


def run_install():
    """Lance l'installation"""
    print("🔧 Lancement de l'installation...")
    
    try:
        subprocess.run([sys.executable, "install.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur lors de l'installation: {e}")
    except FileNotFoundError:
        print("❌ Script d'installation non trouvé")


def run_test():
    """Teste l'installation"""
    print("🧪 Test de l'installation...")
    
    if check_installation():
        print("✅ EV2Gym est correctement installé")
        
        # Test rapide
        try:
            from tools.demo import run_simulation
            print("✅ Modules de démonstration accessibles")
            
            # Test de création d'environnement
            config_file = "ev2gym/example_config_files/V2GProfitMax.yaml"
            if os.path.exists(config_file):
                print("✅ Fichiers de configuration trouvés")
                print("🎉 Installation fonctionnelle!")
            else:
                print("⚠️  Fichiers de configuration manquants")
                
        except ImportError as e:
            print(f"⚠️  Problème avec les outils: {e}")
    else:
        print("❌ Installation incomplète")


def main():
    """Fonction principale"""
    parser = argparse.ArgumentParser(
        description="EV2Gym - Script de Lancement Rapide",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Commandes disponibles")
    
    # Commande demo
    demo_parser = subparsers.add_parser("demo", help="Script de démonstration")
    demo_parser.add_argument("--config", default="V2GProfitMax",
                            choices=["V2GProfitMax", "PublicPST", "BusinessPST", "V2GProfitPlusLoads"])
    demo_parser.add_argument("--agent", default="smart",
                            choices=["random", "fast", "smart", "heuristic"])
    demo_parser.add_argument("--steps", type=int, help="Nombre d'étapes max")
    demo_parser.add_argument("--visualize", action="store_true")
    demo_parser.add_argument("--save", action="store_true")
    
    # Commande cli
    cli_parser = subparsers.add_parser("cli", help="Interface CLI")
    cli_parser.add_argument("--batch", action="store_true", help="Mode comparaison")
    
    # Commande web
    subparsers.add_parser("web", help="Interface web Streamlit")
    
    # Commande notebook
    subparsers.add_parser("notebook", help="Notebook Jupyter")
    
    # Commande analyze
    analyze_parser = subparsers.add_parser("analyze", help="Outils d'analyse")
    analyze_parser.add_argument("--replay_path", help="Chemin vers le replay")
    analyze_parser.add_argument("--compare_agents", action="store_true")
    analyze_parser.add_argument("--config", default="V2GProfitMax")
    analyze_parser.add_argument("--agents", nargs="+", default=["random", "smart"])
    analyze_parser.add_argument("--generate_report", action="store_true")
    
    # Commandes utilitaires
    subparsers.add_parser("install", help="Lancer l'installation")
    subparsers.add_parser("test", help="Tester l'installation")
    subparsers.add_parser("help", help="Afficher l'aide")
    
    args = parser.parse_args()
    
    display_banner()
    
    # Vérifier l'installation pour la plupart des commandes
    if args.command not in ["install", "help", None] and not check_installation():
        return
    
    # Router vers la bonne fonction
    if args.command == "demo":
        run_demo(args)
    elif args.command == "cli":
        run_cli(args)
    elif args.command == "web":
        run_web(args)
    elif args.command == "notebook":
        run_notebook(args)
    elif args.command == "analyze":
        run_analysis(args)
    elif args.command == "install":
        run_install()
    elif args.command == "test":
        run_test()
    elif args.command == "help":
        show_help()
    else:
        show_help()


if __name__ == "__main__":
    main()
