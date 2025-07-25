#!/usr/bin/env python3
"""
EV2Gym - Outils d'Analyse

Utilitaires pour analyser les résultats de simulation EV2Gym et comparer différentes stratégies.
Permet l'analyse approfondie des performances, la génération de rapports et la comparaison d'agents.

Usage:
    python tools/analysis.py --replay_path ./replay/simulation.pkl --generate_report
    python tools/analysis.py --compare_agents --config V2GProfitMax
"""

import os
import sys
import pickle
import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from typing import Dict, List, Any, Optional
import warnings
warnings.filterwarnings('ignore')

# Ajouter le répertoire parent au path pour les imports
sys.path.append(str(Path(__file__).parent.parent))

from tools.demo import run_simulation
from ev2gym.models.replay import EvCityReplay


class EV2GymAnalyzer:
    """Analyseur de résultats pour EV2Gym"""
    
    def __init__(self):
        self.results_cache = {}
        self.comparison_data = {}
    
    def load_replay(self, replay_path: str) -> Optional[EvCityReplay]:
        """Charge un fichier replay de simulation"""
        try:
            with open(replay_path, 'rb') as f:
                replay = pickle.load(f)
            print(f"✅ Replay chargé: {replay_path}")
            return replay
        except FileNotFoundError:
            print(f"❌ Fichier replay non trouvé: {replay_path}")
            return None
        except Exception as e:
            print(f"❌ Erreur lors du chargement: {e}")
            return None
    
    def analyze_single_simulation(self, env_or_replay, save_plots: bool = True) -> Dict[str, Any]:
        """Analyse une simulation unique"""
        
        # Déterminer si c'est un environnement ou un replay
        if hasattr(env_or_replay, 'replay_path'):
            # C'est un replay
            replay = env_or_replay
            env = None
        else:
            # C'est un environnement
            env = env_or_replay
            replay = None
        
        analysis = {
            'basic_metrics': self._calculate_basic_metrics(env, replay),
            'energy_analysis': self._analyze_energy_flows(env, replay),
            'temporal_analysis': self._analyze_temporal_patterns(env, replay),
            'efficiency_metrics': self._calculate_efficiency_metrics(env, replay),
            'constraint_analysis': self._analyze_constraints(env, replay)
        }
        
        if save_plots:
            self._generate_analysis_plots(analysis, env, replay)
        
        return analysis
    
    def _calculate_basic_metrics(self, env, replay) -> Dict[str, float]:
        """Calcule les métriques de base"""
        metrics = {}
        
        if env:
            metrics.update({
                'total_reward': getattr(env, 'total_reward', 0),
                'total_evs_spawned': getattr(env, 'total_evs_spawned', 0),
                'simulation_steps': getattr(env, 'current_step', 0),
                'total_ports': getattr(env, 'number_of_ports', 0),
                'charging_stations': getattr(env, 'cs', 0),
                'transformers': getattr(env, 'number_of_transformers', 0)
            })
            
            if hasattr(env, 'current_power_usage'):
                metrics['total_energy_consumed'] = np.sum(env.current_power_usage)
                metrics['avg_power_consumption'] = np.mean(env.current_power_usage)
                metrics['peak_power'] = np.max(env.current_power_usage)
            
            if env.stats:
                metrics.update({
                    'user_satisfaction': env.stats.get('user_satisfaction_mean', 0),
                    'total_profits': env.stats.get('total_profits', 0),
                    'energy_charged': env.stats.get('total_energy_charged', 0),
                    'energy_discharged': env.stats.get('total_energy_discharged', 0)
                })
        
        return metrics
    
    def _analyze_energy_flows(self, env, replay) -> Dict[str, Any]:
        """Analyse les flux d'énergie"""
        energy_analysis = {
            'charging_patterns': {},
            'v2g_utilization': {},
            'load_distribution': {}
        }
        
        if env and hasattr(env, 'cs_power'):
            # Analyse par station de charge
            for i in range(env.cs):
                if i < env.cs_power.shape[0]:
                    station_power = env.cs_power[i, :env.current_step]
                    energy_analysis['charging_patterns'][f'station_{i}'] = {
                        'total_energy': np.sum(station_power),
                        'avg_power': np.mean(station_power),
                        'utilization_rate': np.sum(station_power > 0) / len(station_power),
                        'peak_power': np.max(station_power)
                    }
            
            # Analyse V2G
            if env.config.get('v2g_enabled', False):
                negative_power = env.cs_power[env.cs_power < 0]
                if len(negative_power) > 0:
                    energy_analysis['v2g_utilization'] = {
                        'total_discharged': np.sum(np.abs(negative_power)),
                        'discharge_events': len(negative_power),
                        'avg_discharge_power': np.mean(np.abs(negative_power))
                    }
        
        return energy_analysis
    
    def _analyze_temporal_patterns(self, env, replay) -> Dict[str, Any]:
        """Analyse les patterns temporels"""
        temporal_analysis = {
            'hourly_patterns': {},
            'peak_periods': {},
            'load_curves': {}
        }
        
        if env and hasattr(env, 'current_power_usage'):
            power_data = env.current_power_usage[:env.current_step]
            
            # Identifier les périodes de pointe
            threshold = np.percentile(power_data, 90)
            peak_indices = np.where(power_data > threshold)[0]
            
            temporal_analysis['peak_periods'] = {
                'peak_threshold': threshold,
                'peak_count': len(peak_indices),
                'peak_percentage': len(peak_indices) / len(power_data) * 100,
                'avg_peak_power': np.mean(power_data[peak_indices]) if len(peak_indices) > 0 else 0
            }
            
            # Courbe de charge
            temporal_analysis['load_curves'] = {
                'power_profile': power_data.tolist(),
                'smoothed_profile': self._smooth_signal(power_data, window=5).tolist()
            }
        
        return temporal_analysis
    
    def _calculate_efficiency_metrics(self, env, replay) -> Dict[str, float]:
        """Calcule les métriques d'efficacité"""
        efficiency = {}
        
        if env:
            # Efficacité énergétique
            if hasattr(env, 'current_power_usage') and env.total_evs_spawned > 0:
                total_energy = np.sum(env.current_power_usage)
                efficiency['energy_per_ev'] = total_energy / env.total_evs_spawned
                efficiency['port_utilization'] = env.total_evs_spawned / (env.number_of_ports * env.current_step)
            
            # Efficacité économique
            if env.stats and 'total_profits' in env.stats and 'total_energy_charged' in env.stats:
                if env.stats['total_energy_charged'] > 0:
                    efficiency['profit_per_kwh'] = env.stats['total_profits'] / env.stats['total_energy_charged']
            
            # Satisfaction utilisateur
            if env.stats and 'user_satisfaction_mean' in env.stats:
                efficiency['user_satisfaction'] = env.stats['user_satisfaction_mean']
        
        return efficiency
    
    def _analyze_constraints(self, env, replay) -> Dict[str, Any]:
        """Analyse les violations de contraintes"""
        constraints = {
            'transformer_overloads': {},
            'voltage_violations': {},
            'power_limits': {}
        }
        
        if env and hasattr(env, 'tr_overload'):
            # Analyse des surcharges de transformateurs
            for i in range(env.number_of_transformers):
                if i < env.tr_overload.shape[0]:
                    overload_data = env.tr_overload[i, :env.current_step]
                    violations = overload_data > 0
                    
                    constraints['transformer_overloads'][f'transformer_{i}'] = {
                        'violation_count': np.sum(violations),
                        'violation_percentage': np.sum(violations) / len(violations) * 100,
                        'max_overload': np.max(overload_data),
                        'avg_overload': np.mean(overload_data[violations]) if np.any(violations) else 0
                    }
        
        return constraints
    
    def _smooth_signal(self, signal: np.ndarray, window: int = 5) -> np.ndarray:
        """Lisse un signal avec une moyenne mobile"""
        if len(signal) < window:
            return signal
        return np.convolve(signal, np.ones(window)/window, mode='same')
    
    def _generate_analysis_plots(self, analysis: Dict[str, Any], env, replay):
        """Génère les graphiques d'analyse"""
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle('Analyse de Simulation EV2Gym', fontsize=16, fontweight='bold')
        
        # Graphique 1: Consommation d'énergie
        if 'load_curves' in analysis['temporal_analysis'] and analysis['temporal_analysis']['load_curves']:
            power_profile = analysis['temporal_analysis']['load_curves']['power_profile']
            axes[0,0].plot(power_profile, 'b-', linewidth=1, alpha=0.7, label='Puissance')
            
            if 'smoothed_profile' in analysis['temporal_analysis']['load_curves']:
                smoothed = analysis['temporal_analysis']['load_curves']['smoothed_profile']
                axes[0,0].plot(smoothed, 'r-', linewidth=2, label='Tendance')
            
            axes[0,0].set_title('Profil de Consommation')
            axes[0,0].set_xlabel('Étapes de Simulation')
            axes[0,0].set_ylabel('Puissance (kW)')
            axes[0,0].legend()
            axes[0,0].grid(True, alpha=0.3)
        
        # Graphique 2: Utilisation des stations
        if 'charging_patterns' in analysis['energy_analysis']:
            stations = list(analysis['energy_analysis']['charging_patterns'].keys())
            utilization = [analysis['energy_analysis']['charging_patterns'][s]['utilization_rate'] 
                          for s in stations]
            
            axes[0,1].bar(range(len(stations)), utilization, color='skyblue')
            axes[0,1].set_title('Taux d\'Utilisation des Stations')
            axes[0,1].set_xlabel('Stations de Charge')
            axes[0,1].set_ylabel('Taux d\'Utilisation')
            axes[0,1].set_xticks(range(len(stations)))
            axes[0,1].set_xticklabels([f'S{i+1}' for i in range(len(stations))])
        
        # Graphique 3: Métriques d'efficacité
        if analysis['efficiency_metrics']:
            metrics = analysis['efficiency_metrics']
            metric_names = list(metrics.keys())
            metric_values = list(metrics.values())
            
            axes[1,0].barh(metric_names, metric_values, color='lightgreen')
            axes[1,0].set_title('Métriques d\'Efficacité')
            axes[1,0].set_xlabel('Valeur')
        
        # Graphique 4: Violations de contraintes
        if 'transformer_overloads' in analysis['constraint_analysis']:
            overloads = analysis['constraint_analysis']['transformer_overloads']
            transformers = list(overloads.keys())
            violations = [overloads[t]['violation_percentage'] for t in transformers]
            
            axes[1,1].bar(range(len(transformers)), violations, color='lightcoral')
            axes[1,1].set_title('Violations de Contraintes (%)')
            axes[1,1].set_xlabel('Transformateurs')
            axes[1,1].set_ylabel('Pourcentage de Violations')
            axes[1,1].set_xticks(range(len(transformers)))
            axes[1,1].set_xticklabels([f'T{i+1}' for i in range(len(transformers))])
        
        plt.tight_layout()
        
        # Sauvegarder le graphique
        os.makedirs('./analysis_results', exist_ok=True)
        plt.savefig('./analysis_results/simulation_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        print("📊 Graphiques d'analyse sauvegardés dans: ./analysis_results/")
    
    def compare_agents(self, config_file: str, agents: List[str], max_steps: int = 100) -> pd.DataFrame:
        """Compare les performances de plusieurs agents"""
        print(f"🔬 Comparaison de {len(agents)} agents...")
        
        results = []
        
        for agent_type in agents:
            print(f"   Testing {agent_type}...", end=" ")
            
            try:
                env, reward, cost = run_simulation(
                    config_file=config_file,
                    agent_type=agent_type,
                    max_steps=max_steps,
                    visualize=False,
                    save_results=False
                )
                
                analysis = self.analyze_single_simulation(env, save_plots=False)
                
                result = {
                    'Agent': agent_type,
                    'Récompense': reward,
                    'Coût': cost,
                    'EVs Servis': env.total_evs_spawned,
                    'Énergie Totale': analysis['basic_metrics'].get('total_energy_consumed', 0),
                    'Satisfaction': analysis['basic_metrics'].get('user_satisfaction', 0),
                    'Efficacité Énergétique': analysis['efficiency_metrics'].get('energy_per_ev', 0),
                    'Utilisation Ports': analysis['efficiency_metrics'].get('port_utilization', 0)
                }
                
                results.append(result)
                print("✅")
                
            except Exception as e:
                print(f"❌ ({e})")
                results.append({
                    'Agent': agent_type,
                    'Récompense': 0,
                    'Coût': float('inf'),
                    'EVs Servis': 0,
                    'Énergie Totale': 0,
                    'Satisfaction': 0,
                    'Efficacité Énergétique': 0,
                    'Utilisation Ports': 0
                })
        
        df_comparison = pd.DataFrame(results)
        
        # Sauvegarder les résultats
        os.makedirs('./analysis_results', exist_ok=True)
        df_comparison.to_csv('./analysis_results/agent_comparison.csv', index=False)
        
        print(f"\n📊 Résultats de comparaison sauvegardés dans: ./analysis_results/agent_comparison.csv")
        
        return df_comparison
    
    def generate_report(self, analysis: Dict[str, Any], output_path: str = './analysis_results/report.txt'):
        """Génère un rapport d'analyse textuel"""
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("=" * 60 + "\n")
            f.write("RAPPORT D'ANALYSE EV2GYM\n")
            f.write("=" * 60 + "\n\n")
            
            # Métriques de base
            f.write("📊 MÉTRIQUES DE BASE\n")
            f.write("-" * 30 + "\n")
            for key, value in analysis['basic_metrics'].items():
                f.write(f"{key.replace('_', ' ').title()}: {value:.2f}\n")
            f.write("\n")
            
            # Analyse énergétique
            f.write("⚡ ANALYSE ÉNERGÉTIQUE\n")
            f.write("-" * 30 + "\n")
            if 'charging_patterns' in analysis['energy_analysis']:
                for station, data in analysis['energy_analysis']['charging_patterns'].items():
                    f.write(f"{station.replace('_', ' ').title()}:\n")
                    for metric, value in data.items():
                        f.write(f"  - {metric.replace('_', ' ').title()}: {value:.2f}\n")
                f.write("\n")
            
            # Efficacité
            f.write("📈 MÉTRIQUES D'EFFICACITÉ\n")
            f.write("-" * 30 + "\n")
            for key, value in analysis['efficiency_metrics'].items():
                f.write(f"{key.replace('_', ' ').title()}: {value:.3f}\n")
            f.write("\n")
            
            # Contraintes
            f.write("⚠️  ANALYSE DES CONTRAINTES\n")
            f.write("-" * 30 + "\n")
            if 'transformer_overloads' in analysis['constraint_analysis']:
                for transformer, data in analysis['constraint_analysis']['transformer_overloads'].items():
                    f.write(f"{transformer.replace('_', ' ').title()}:\n")
                    for metric, value in data.items():
                        f.write(f"  - {metric.replace('_', ' ').title()}: {value:.2f}\n")
        
        print(f"📄 Rapport généré: {output_path}")


def main():
    """Fonction principale"""
    parser = argparse.ArgumentParser(description="EV2Gym - Outils d'Analyse")
    
    parser.add_argument("--replay_path", type=str,
                       help="Chemin vers le fichier replay à analyser")
    
    parser.add_argument("--compare_agents", action="store_true",
                       help="Comparer différents agents")
    
    parser.add_argument("--config", default="V2GProfitMax",
                       choices=["V2GProfitMax", "PublicPST", "BusinessPST", "V2GProfitPlusLoads"],
                       help="Configuration pour la comparaison d'agents")
    
    parser.add_argument("--agents", nargs="+", 
                       default=["random", "fast", "smart", "heuristic"],
                       help="Agents à comparer")
    
    parser.add_argument("--max_steps", type=int, default=100,
                       help="Nombre maximum d'étapes pour la comparaison")
    
    parser.add_argument("--generate_report", action="store_true",
                       help="Générer un rapport d'analyse")
    
    args = parser.parse_args()
    
    analyzer = EV2GymAnalyzer()
    
    if args.replay_path:
        # Analyser un replay existant
        replay = analyzer.load_replay(args.replay_path)
        if replay:
            analysis = analyzer.analyze_single_simulation(replay)
            if args.generate_report:
                analyzer.generate_report(analysis)
    
    elif args.compare_agents:
        # Comparer des agents
        config_path = f"ev2gym/example_config_files/{args.config}.yaml"
        df_comparison = analyzer.compare_agents(config_path, args.agents, args.max_steps)
        
        print("\n📊 Résultats de la comparaison:")
        print(df_comparison.round(3))
        
        # Identifier le meilleur agent
        best_agent = df_comparison.loc[df_comparison['Récompense'].idxmax(), 'Agent']
        print(f"\n🏆 Meilleur agent: {best_agent}")
    
    else:
        print("❌ Veuillez spécifier --replay_path ou --compare_agents")


if __name__ == "__main__":
    main()
