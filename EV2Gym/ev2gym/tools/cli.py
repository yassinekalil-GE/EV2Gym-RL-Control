#!/usr/bin/env python3
"""
EV2Gym - Interface CLI Interactive

Interface en ligne de commande interactive pour configurer et lancer des simulations EV2Gym.
Permet de modifier les paramètres de simulation de manière intuitive.

Usage:
    python tools/cli.py
"""

import os
import sys
import yaml
import argparse
from pathlib import Path
from typing import Dict, Any

# Ajouter le répertoire parent au path pour les imports
sys.path.append(str(Path(__file__).parent.parent))

from tools.demo import run_simulation


class EV2GymCLI:
    """Interface CLI interactive pour EV2Gym"""
    
    def __init__(self):
        self.config_templates = {
            "V2GProfitMax": "ev2gym/example_config_files/V2GProfitMax.yaml",
            "PublicPST": "ev2gym/example_config_files/PublicPST.yaml", 
            "BusinessPST": "ev2gym/example_config_files/BusinessPST.yaml",
            "V2GProfitPlusLoads": "ev2gym/example_config_files/V2GProfitPlusLoads.yaml"
        }
        
        self.agent_types = {
            "1": ("random", "Agent aléatoire"),
            "2": ("fast", "Charge rapide"),
            "3": ("smart", "Agent intelligent simple"),
            "4": ("heuristic", "Heuristique Round Robin")
        }
    
    def display_banner(self):
        """Affiche la bannière de l'application"""
        print("=" * 60)
        print("🚗⚡ EV2Gym - Simulateur de Recharge Intelligente")
        print("=" * 60)
        print("Interface CLI Interactive pour la simulation V2G")
        print()
    
    def select_config_template(self) -> str:
        """Permet à l'utilisateur de sélectionner un template de configuration"""
        print("📋 Sélection du scénario de simulation:")
        print()
        
        templates_info = {
            "V2GProfitMax": "Maximisation des profits V2G",
            "PublicPST": "Recharge publique avec suivi de consigne",
            "BusinessPST": "Recharge en entreprise",
            "V2GProfitPlusLoads": "V2G avec charges flexibles"
        }
        
        for i, (key, desc) in enumerate(templates_info.items(), 1):
            print(f"  {i}. {key}: {desc}")
        
        while True:
            try:
                choice = input(f"\nChoisissez un scénario (1-{len(templates_info)}): ").strip()
                idx = int(choice) - 1
                if 0 <= idx < len(templates_info):
                    selected = list(templates_info.keys())[idx]
                    print(f"✅ Scénario sélectionné: {selected}")
                    return self.config_templates[selected]
                else:
                    print("❌ Choix invalide, veuillez réessayer.")
            except ValueError:
                print("❌ Veuillez entrer un nombre valide.")
    
    def select_agent(self) -> str:
        """Permet à l'utilisateur de sélectionner un type d'agent"""
        print("\n🤖 Sélection de l'agent de contrôle:")
        print()
        
        for key, (agent_type, desc) in self.agent_types.items():
            print(f"  {key}. {desc}")
        
        while True:
            choice = input(f"\nChoisissez un agent (1-{len(self.agent_types)}): ").strip()
            if choice in self.agent_types:
                agent_type, desc = self.agent_types[choice]
                print(f"✅ Agent sélectionné: {desc}")
                return agent_type
            else:
                print("❌ Choix invalide, veuillez réessayer.")
    
    def configure_simulation(self, config_path: str) -> Dict[str, Any]:
        """Configure les paramètres de simulation"""
        print("\n⚙️  Configuration de la simulation:")
        print()
        
        # Charger la configuration par défaut
        with open(config_path, 'r') as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
        
        # Afficher les paramètres actuels
        print("Paramètres actuels:")
        print(f"  - Durée: {config['simulation_length']} étapes")
        print(f"  - Échelle temporelle: {config['timescale']} minutes/étape")
        print(f"  - Stations de charge: {config['number_of_charging_stations']}")
        print(f"  - Transformateurs: {config['number_of_transformers']}")
        print(f"  - V2G activé: {config['v2g_enabled']}")
        
        # Demander modifications
        modify = input("\nVoulez-vous modifier ces paramètres? (o/N): ").strip().lower()
        
        if modify in ['o', 'oui', 'y', 'yes']:
            # Durée de simulation
            try:
                new_duration = input(f"Durée de simulation ({config['simulation_length']}): ").strip()
                if new_duration:
                    config['simulation_length'] = int(new_duration)
            except ValueError:
                print("⚠️  Valeur invalide, conservation de la valeur par défaut")
            
            # Nombre de stations
            try:
                new_stations = input(f"Nombre de stations ({config['number_of_charging_stations']}): ").strip()
                if new_stations:
                    config['number_of_charging_stations'] = int(new_stations)
            except ValueError:
                print("⚠️  Valeur invalide, conservation de la valeur par défaut")
            
            # V2G
            v2g_choice = input(f"Activer V2G? (O/n): ").strip().lower()
            if v2g_choice in ['n', 'non', 'no']:
                config['v2g_enabled'] = False
            elif v2g_choice in ['o', 'oui', 'y', 'yes']:
                config['v2g_enabled'] = True
        
        # Options d'exécution
        print("\n🎯 Options d'exécution:")
        
        max_steps = input("Nombre maximum d'étapes (vide = complet): ").strip()
        max_steps = int(max_steps) if max_steps else None
        
        visualize = input("Affichage en temps réel? (o/N): ").strip().lower() in ['o', 'oui', 'y', 'yes']
        save_results = input("Sauvegarder les résultats? (o/N): ").strip().lower() in ['o', 'oui', 'y', 'yes']
        
        return {
            'config': config,
            'max_steps': max_steps,
            'visualize': visualize,
            'save_results': save_results
        }
    
    def save_custom_config(self, config: Dict[str, Any]) -> str:
        """Sauvegarde une configuration personnalisée"""
        custom_config_path = "custom_config.yaml"
        
        with open(custom_config_path, 'w') as f:
            yaml.dump(config, f, default_flow_style=False)
        
        print(f"📁 Configuration sauvegardée: {custom_config_path}")
        return custom_config_path
    
    def run_interactive_simulation(self):
        """Lance une simulation interactive"""
        self.display_banner()
        
        try:
            # Sélection du template
            config_path = self.select_config_template()
            
            # Sélection de l'agent
            agent_type = self.select_agent()
            
            # Configuration
            sim_config = self.configure_simulation(config_path)
            
            # Sauvegarder la config personnalisée si modifiée
            if sim_config['config']:
                config_path = self.save_custom_config(sim_config['config'])
            
            print("\n🚀 Lancement de la simulation...")
            print("-" * 40)
            
            # Lancer la simulation
            env, total_reward, total_cost = run_simulation(
                config_file=config_path,
                agent_type=agent_type,
                max_steps=sim_config['max_steps'],
                visualize=sim_config['visualize'],
                save_results=sim_config['save_results']
            )
            
            # Proposer une nouvelle simulation
            print("\n" + "=" * 60)
            again = input("Voulez-vous lancer une autre simulation? (o/N): ").strip().lower()
            if again in ['o', 'oui', 'y', 'yes']:
                self.run_interactive_simulation()
            else:
                print("👋 Merci d'avoir utilisé EV2Gym!")
                
        except KeyboardInterrupt:
            print("\n\n⏹️  Simulation interrompue par l'utilisateur")
        except Exception as e:
            print(f"\n❌ Erreur: {e}")
            import traceback
            traceback.print_exc()
    
    def run_batch_comparison(self):
        """Lance une comparaison de plusieurs agents"""
        print("\n🔬 Mode Comparaison d'Agents")
        print("-" * 40)
        
        config_path = self.select_config_template()
        
        agents_to_test = []
        print("\nSélectionnez les agents à comparer (séparés par des virgules):")
        for key, (agent_type, desc) in self.agent_types.items():
            print(f"  {key}. {desc}")
        
        choices = input("\nVotre sélection (ex: 1,2,3): ").strip().split(',')
        
        for choice in choices:
            choice = choice.strip()
            if choice in self.agent_types:
                agents_to_test.append(self.agent_types[choice][0])
        
        if not agents_to_test:
            print("❌ Aucun agent sélectionné")
            return
        
        print(f"\n🏁 Comparaison de {len(agents_to_test)} agents...")
        
        results = {}
        for agent_type in agents_to_test:
            print(f"\n--- Test de l'agent: {agent_type} ---")
            try:
                env, reward, cost = run_simulation(
                    config_file=config_path,
                    agent_type=agent_type,
                    max_steps=100,  # Simulation courte pour comparaison
                    visualize=False,
                    save_results=False
                )
                results[agent_type] = {'reward': reward, 'cost': cost}
            except Exception as e:
                print(f"❌ Erreur avec {agent_type}: {e}")
                results[agent_type] = {'reward': 0, 'cost': float('inf')}
        
        # Afficher les résultats comparatifs
        print("\n📊 Résultats de la comparaison:")
        print("-" * 50)
        print(f"{'Agent':<15} {'Récompense':<12} {'Coût':<10}")
        print("-" * 50)
        
        for agent, result in results.items():
            print(f"{agent:<15} {result['reward']:<12.2f} {result['cost']:<10.2f}")
        
        # Meilleur agent
        best_agent = max(results.keys(), key=lambda x: results[x]['reward'])
        print(f"\n🏆 Meilleur agent: {best_agent}")


def main():
    """Fonction principale"""
    parser = argparse.ArgumentParser(description="EV2Gym CLI Interactive")
    parser.add_argument("--batch", action="store_true", 
                       help="Mode comparaison d'agents")
    
    args = parser.parse_args()
    
    cli = EV2GymCLI()
    
    if args.batch:
        cli.run_batch_comparison()
    else:
        cli.run_interactive_simulation()


if __name__ == "__main__":
    main()
