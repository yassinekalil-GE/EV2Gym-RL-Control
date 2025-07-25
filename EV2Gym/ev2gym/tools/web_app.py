#!/usr/bin/env python3
"""
EV2Gym - Interface Web Streamlit

Interface web interactive pour configurer et lancer des simulations EV2Gym.
Permet une utilisation intuitive avec visualisations en temps réel.

Usage:
    streamlit run tools/web_app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import yaml
import sys
import time
from pathlib import Path
from typing import Dict, Any

# Configuration de la page
st.set_page_config(
    page_title="EV2Gym - Simulateur V2G",
    page_icon="🚗⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Ajouter le répertoire parent au path pour les imports
sys.path.append(str(Path(__file__).parent.parent))

try:
    from tools.demo import run_simulation, SimpleAgents
    from ev2gym.models.ev2gym_env import EV2Gym
    from ev2gym.rl_agent.reward import SquaredTrackingErrorReward, ProfitMax_TrPenalty_UserIncentives
    from ev2gym.rl_agent.state import PublicPST, V2G_profit_max
except ImportError as e:
    st.error(f"Erreur d'import: {e}")
    st.stop()


class EV2GymWebApp:
    """Application web Streamlit pour EV2Gym"""
    
    def __init__(self):
        self.config_templates = {
            "V2GProfitMax": {
                "path": "ev2gym/example_config_files/V2GProfitMax.yaml",
                "description": "Maximisation des profits V2G",
                "icon": "💰"
            },
            "PublicPST": {
                "path": "ev2gym/example_config_files/PublicPST.yaml", 
                "description": "Recharge publique avec suivi de consigne",
                "icon": "🏪"
            },
            "BusinessPST": {
                "path": "ev2gym/example_config_files/BusinessPST.yaml",
                "description": "Recharge en entreprise",
                "icon": "🏢"
            },
            "V2GProfitPlusLoads": {
                "path": "ev2gym/example_config_files/V2GProfitPlusLoads.yaml",
                "description": "V2G avec charges flexibles",
                "icon": "⚡"
            }
        }
        
        self.agent_types = {
            "random": {"name": "Agent Aléatoire", "icon": "🎲"},
            "fast": {"name": "Charge Rapide", "icon": "⚡"},
            "smart": {"name": "Agent Intelligent", "icon": "🧠"},
            "heuristic": {"name": "Round Robin", "icon": "🔄"}
        }
    
    def render_header(self):
        """Affiche l'en-tête de l'application"""
        st.title("🚗⚡ EV2Gym - Simulateur de Recharge Intelligente")
        st.markdown("""
        **Plateforme de simulation Vehicle-to-Grid (V2G) pour la recherche en recharge intelligente**
        
        Cette interface permet de configurer et lancer des simulations de recharge de véhicules électriques
        avec différentes stratégies de contrôle et visualisations en temps réel.
        """)
        st.divider()
    
    def render_sidebar(self):
        """Affiche la barre latérale de configuration"""
        st.sidebar.header("⚙️ Configuration")
        
        # Sélection du scénario
        st.sidebar.subheader("📋 Scénario")
        scenario_options = {k: f"{v['icon']} {k} - {v['description']}" 
                          for k, v in self.config_templates.items()}
        
        selected_scenario = st.sidebar.selectbox(
            "Choisissez un scénario:",
            options=list(scenario_options.keys()),
            format_func=lambda x: scenario_options[x],
            key="scenario"
        )
        
        # Sélection de l'agent
        st.sidebar.subheader("🤖 Agent de Contrôle")
        agent_options = {k: f"{v['icon']} {v['name']}" 
                        for k, v in self.agent_types.items()}
        
        selected_agent = st.sidebar.selectbox(
            "Choisissez un agent:",
            options=list(agent_options.keys()),
            format_func=lambda x: agent_options[x],
            key="agent"
        )
        
        # Paramètres de simulation
        st.sidebar.subheader("🎯 Paramètres")
        
        max_steps = st.sidebar.number_input(
            "Nombre d'étapes max:",
            min_value=10,
            max_value=500,
            value=100,
            step=10,
            help="Nombre maximum d'étapes de simulation"
        )
        
        visualize = st.sidebar.checkbox(
            "Affichage détaillé",
            value=False,
            help="Afficher les détails pendant la simulation"
        )
        
        save_results = st.sidebar.checkbox(
            "Sauvegarder résultats",
            value=False,
            help="Sauvegarder les résultats de simulation"
        )
        
        return {
            'scenario': selected_scenario,
            'agent': selected_agent,
            'max_steps': max_steps,
            'visualize': visualize,
            'save_results': save_results
        }
    
    def load_config_info(self, scenario: str) -> Dict[str, Any]:
        """Charge et affiche les informations de configuration"""
        config_path = self.config_templates[scenario]["path"]
        
        try:
            with open(config_path, 'r') as f:
                config = yaml.load(f, Loader=yaml.FullLoader)
            return config
        except FileNotFoundError:
            st.error(f"Fichier de configuration non trouvé: {config_path}")
            return {}
    
    def display_config_info(self, config: Dict[str, Any]):
        """Affiche les informations de configuration"""
        if not config:
            return
            
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Durée Simulation", f"{config.get('simulation_length', 'N/A')} étapes")
            st.metric("Échelle Temporelle", f"{config.get('timescale', 'N/A')} min/étape")
        
        with col2:
            st.metric("Stations de Charge", config.get('number_of_charging_stations', 'N/A'))
            st.metric("Transformateurs", config.get('number_of_transformers', 'N/A'))
        
        with col3:
            st.metric("V2G Activé", "✅" if config.get('v2g_enabled', False) else "❌")
            st.metric("Scénario", config.get('scenario', 'N/A').title())
    
    def run_simulation_ui(self, params: Dict[str, Any]):
        """Interface pour lancer une simulation"""
        config_path = self.config_templates[params['scenario']]["path"]
        
        if st.button("🚀 Lancer la Simulation", type="primary", use_container_width=True):
            
            # Placeholder pour les résultats
            progress_bar = st.progress(0)
            status_text = st.empty()
            results_container = st.empty()
            
            try:
                status_text.text("🔄 Initialisation de la simulation...")
                progress_bar.progress(10)
                
                # Lancer la simulation
                status_text.text("⚡ Simulation en cours...")
                progress_bar.progress(50)
                
                env, total_reward, total_cost = run_simulation(
                    config_file=config_path,
                    agent_type=params['agent'],
                    max_steps=params['max_steps'],
                    visualize=params['visualize'],
                    save_results=params['save_results']
                )
                
                progress_bar.progress(100)
                status_text.text("✅ Simulation terminée!")
                
                # Afficher les résultats
                self.display_results(env, total_reward, total_cost, results_container)
                
            except Exception as e:
                st.error(f"❌ Erreur lors de la simulation: {e}")
                progress_bar.empty()
                status_text.empty()
    
    def display_results(self, env, total_reward: float, total_cost: float, container):
        """Affiche les résultats de simulation"""
        with container.container():
            st.subheader("📊 Résultats de la Simulation")
            
            # Métriques principales
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Récompense Totale", f"{total_reward:.2f}")
            with col2:
                st.metric("Coût Total", f"{total_cost:.2f}")
            with col3:
                st.metric("EVs Traités", env.total_evs_spawned)
            with col4:
                st.metric("Étapes Exécutées", env.current_step)
            
            # Graphiques
            if hasattr(env, 'current_power_usage') and len(env.current_power_usage) > 0:
                self.create_power_usage_chart(env)
            
            if hasattr(env, 'cs_power') and env.cs_power.size > 0:
                self.create_charging_stations_chart(env)
            
            # Statistiques détaillées
            if env.stats:
                self.display_detailed_stats(env.stats)
    
    def create_power_usage_chart(self, env):
        """Crée le graphique de consommation d'énergie"""
        st.subheader("⚡ Évolution de la Consommation d'Énergie")
        
        time_steps = list(range(len(env.current_power_usage)))
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=time_steps,
            y=env.current_power_usage,
            mode='lines',
            name='Consommation',
            line=dict(color='blue', width=2)
        ))
        
        fig.update_layout(
            title="Consommation d'Énergie au Cours du Temps",
            xaxis_title="Étapes de Simulation",
            yaxis_title="Puissance (kW)",
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def create_charging_stations_chart(self, env):
        """Crée le graphique des stations de charge"""
        st.subheader("🔌 Activité des Stations de Charge")
        
        # Créer un DataFrame pour les données des stations
        stations_data = []
        for i in range(env.cs):
            if i < env.cs_power.shape[0]:
                power_data = env.cs_power[i, :env.current_step]
                stations_data.append({
                    'Station': f'Station {i+1}',
                    'Puissance Moyenne': np.mean(power_data),
                    'Puissance Max': np.max(power_data),
                    'Utilisation': np.sum(power_data > 0) / len(power_data) * 100
                })
        
        if stations_data:
            df_stations = pd.DataFrame(stations_data)
            
            fig = px.bar(df_stations, x='Station', y='Puissance Moyenne',
                        title="Puissance Moyenne par Station de Charge",
                        color='Utilisation',
                        color_continuous_scale='Viridis')
            
            st.plotly_chart(fig, use_container_width=True)
    
    def display_detailed_stats(self, stats: Dict[str, Any]):
        """Affiche les statistiques détaillées"""
        st.subheader("📈 Statistiques Détaillées")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if 'user_satisfaction_mean' in stats:
                st.metric("Satisfaction Utilisateur", f"{stats['user_satisfaction_mean']:.3f}")
            if 'total_energy_charged' in stats:
                st.metric("Énergie Chargée", f"{stats['total_energy_charged']:.2f} kWh")
        
        with col2:
            if 'total_energy_discharged' in stats:
                st.metric("Énergie Déchargée", f"{stats['total_energy_discharged']:.2f} kWh")
            if 'total_profits' in stats:
                st.metric("Profits Totaux", f"{stats['total_profits']:.2f} €")
    
    def run(self):
        """Lance l'application web"""
        self.render_header()
        
        # Configuration dans la barre latérale
        params = self.render_sidebar()
        
        # Informations de configuration
        st.subheader("📋 Configuration Sélectionnée")
        config = self.load_config_info(params['scenario'])
        self.display_config_info(config)
        
        st.divider()
        
        # Interface de simulation
        self.run_simulation_ui(params)


def main():
    """Fonction principale"""
    app = EV2GymWebApp()
    app.run()


if __name__ == "__main__":
    main()
