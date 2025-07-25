#!/usr/bin/env python3
"""
EV2Gym - Script de Démonstration

Ce script montre comment utiliser EV2Gym avec différentes configurations et agents.
Il permet de tester rapidement les fonctionnalités principales de la plateforme.

Usage:
    python tools/demo.py --config V2GProfitMax --agent heuristic --steps 100
    python tools/demo.py --config PublicPST --agent random --visualize
"""

import os
import sys
import argparse
import time
import numpy as np
from pathlib import Path

# Ajouter le répertoire parent au path pour les imports
sys.path.append(str(Path(__file__).parent.parent))

from ev2gym.models.ev2gym_env import EV2Gym
from ev2gym.rl_agent.reward import SquaredTrackingErrorReward, ProfitMax_TrPenalty_UserIncentives
from ev2gym.rl_agent.state import PublicPST, V2G_profit_max
from ev2gym.baselines.heuristics import RoundRobin, ChargeAsLateAsPossible, ChargeAsFastAsPossible


class SimpleAgents:
    """Collection d'agents simples pour la démonstration"""
    
    @staticmethod
    def random_agent(env):
        """Agent aléatoire"""
        return env.action_space.sample()
    
    @staticmethod
    def charge_fast_agent(env):
        """Agent qui charge le plus rapidement possible"""
        actions = np.zeros(env.number_of_ports)
        for i, cs in enumerate(env.charging_stations):
            for j in range(cs.n_ports):
                if cs.evs_connected[j] is not None:
                    actions[i * cs.n_ports + j] = 1.0  # Charge maximale
        return actions
    
    @staticmethod
    def smart_agent(env):
        """Agent intelligent simple basé sur les prix"""
        actions = np.zeros(env.number_of_ports)
        port_idx = 0
        
        for i, cs in enumerate(env.charging_stations):
            current_price = env.charge_prices[cs.id, env.current_step]
            discharge_price = env.discharge_prices[cs.id, env.current_step]
            
            for j in range(cs.n_ports):
                if cs.evs_connected[j] is not None:
                    ev = cs.evs_connected[j]
                    soc = ev.current_capacity / ev.battery_capacity
                    
                    # Logique simple : charger si prix bas ou SOC faible, décharger si prix élevé et SOC élevé
                    if soc < 0.2:  # SOC critique
                        actions[port_idx] = 1.0
                    elif soc > 0.8 and discharge_price > current_price * 1.2:  # Opportunité de décharge
                        actions[port_idx] = -0.5
                    elif current_price < 0.1:  # Prix très bas
                        actions[port_idx] = 0.8
                    else:
                        actions[port_idx] = 0.3  # Charge modérée
                
                port_idx += 1
        
        return actions


def run_simulation(config_file, agent_type, max_steps=None, visualize=False, save_results=False):
    """
    Lance une simulation avec les paramètres spécifiés
    
    Args:
        config_file: Chemin vers le fichier de configuration
        agent_type: Type d'agent ('random', 'fast', 'smart', 'heuristic')
        max_steps: Nombre maximum d'étapes (None = utilise la config)
        visualize: Afficher la visualisation en temps réel
        save_results: Sauvegarder les résultats
    """
    
    print(f"🚗 Initialisation de EV2Gym...")
    print(f"   Configuration: {config_file}")
    print(f"   Agent: {agent_type}")
    
    # Déterminer les fonctions de state et reward selon la config
    if "Profit" in config_file:
        state_function = V2G_profit_max
        reward_function = ProfitMax_TrPenalty_UserIncentives
    else:
        state_function = PublicPST
        reward_function = SquaredTrackingErrorReward
    
    # Créer l'environnement
    env = EV2Gym(
        config_file=config_file,
        generate_rnd_game=True,
        state_function=state_function,
        reward_function=reward_function,
        save_replay=save_results,
        save_plots=save_results,
        verbose=visualize
    )
    
    # Initialiser l'agent
    if agent_type == "random":
        agent_func = SimpleAgents.random_agent
    elif agent_type == "fast":
        agent_func = SimpleAgents.charge_fast_agent
    elif agent_type == "smart":
        agent_func = SimpleAgents.smart_agent
    elif agent_type == "heuristic":
        agent_func = lambda env: RoundRobin().get_action(env)
    else:
        raise ValueError(f"Type d'agent non reconnu: {agent_type}")
    
    print(f"   Ports de charge: {env.number_of_ports}")
    print(f"   Stations: {env.cs}")
    print(f"   Transformateurs: {env.number_of_transformers}")
    print(f"   Durée simulation: {env.simulation_length} étapes")
    
    # Reset de l'environnement
    obs, info = env.reset()
    
    total_reward = 0
    total_cost = 0
    step_count = 0
    start_time = time.time()
    
    print(f"\n🔋 Démarrage de la simulation...")
    
    # Boucle principale de simulation
    while not env.done:
        if max_steps and step_count >= max_steps:
            break
            
        # Obtenir l'action de l'agent
        action = agent_func(env)
        
        # Exécuter l'étape
        obs, reward, done, truncated, info = env.step(action)
        
        total_reward += reward
        if 'cost' in info and info['cost'] is not None:
            total_cost += info['cost']
        
        step_count += 1
        
        # Affichage périodique
        if visualize and step_count % 10 == 0:
            print(f"   Étape {step_count:3d} | Récompense: {reward:6.2f} | EVs: {env.current_evs_parked:2d}")
    
    # Résultats finaux
    simulation_time = time.time() - start_time
    
    print(f"\n📊 Résultats de la simulation:")
    print(f"   Étapes exécutées: {step_count}")
    print(f"   Temps de simulation: {simulation_time:.2f}s")
    print(f"   Récompense totale: {total_reward:.2f}")
    print(f"   Coût total: {total_cost:.2f}")
    print(f"   EVs traités: {env.total_evs_spawned}")
    
    if env.stats:
        print(f"   Satisfaction utilisateur: {env.stats.get('user_satisfaction_mean', 'N/A'):.3f}")
        print(f"   Utilisation énergie: {env.stats.get('total_energy_charged', 'N/A'):.2f} kWh")
    
    return env, total_reward, total_cost


def main():
    """Fonction principale"""
    parser = argparse.ArgumentParser(description="EV2Gym - Script de Démonstration")
    
    parser.add_argument("--config", default="V2GProfitMax", 
                       choices=["V2GProfitMax", "PublicPST", "BusinessPST", "V2GProfitPlusLoads"],
                       help="Configuration à utiliser")
    
    parser.add_argument("--agent", default="smart",
                       choices=["random", "fast", "smart", "heuristic"],
                       help="Type d'agent à utiliser")
    
    parser.add_argument("--steps", type=int, default=None,
                       help="Nombre maximum d'étapes (défaut: utilise la config)")
    
    parser.add_argument("--visualize", action="store_true",
                       help="Afficher la visualisation en temps réel")
    
    parser.add_argument("--save", action="store_true",
                       help="Sauvegarder les résultats")
    
    args = parser.parse_args()
    
    # Construire le chemin du fichier de configuration
    config_path = f"ev2gym/example_config_files/{args.config}.yaml"
    
    if not os.path.exists(config_path):
        print(f"❌ Fichier de configuration non trouvé: {config_path}")
        return
    
    try:
        # Lancer la simulation
        env, reward, cost = run_simulation(
            config_file=config_path,
            agent_type=args.agent,
            max_steps=args.steps,
            visualize=args.visualize,
            save_results=args.save
        )
        
        print(f"\n✅ Simulation terminée avec succès!")
        
        if args.save:
            print(f"   Résultats sauvegardés dans: ./results/{env.sim_name}/")
            
    except Exception as e:
        print(f"❌ Erreur lors de la simulation: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
