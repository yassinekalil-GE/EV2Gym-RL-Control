#!/usr/bin/env python3
"""
EV2Gym Agent Management System

Advanced agent selection, configuration, and comparison system for the EV2Gym dashboard.
Supports multiple agent types, parameter tuning, and performance comparison.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import json
import time
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime


@dataclass
class AgentPerformance:
    """Classe pour stocker les performances d'un agent"""
    agent_name: str
    total_reward: float
    avg_reward: float
    total_energy: float
    avg_power: float
    execution_time: float
    convergence_rate: float
    user_satisfaction: float
    cost_efficiency: float


class AgentManager:
    """Gestionnaire d'agents avancé"""
    
    def __init__(self):
        self.agent_history = []
        self.comparison_data = {}
        
        # Configuration des agents avec paramètres détaillés
        self.agent_configs = {
            "OCMF_V2G": {
                "class_name": "OCMF_V2G",
                "name": "OCMF V2G",
                "description": "Optimal Charging Management Framework avec V2G",
                "category": "MPC",
                "icon": "🎯",
                "complexity": "High",
                "parameters": {
                    "control_horizon": {
                        "type": "slider",
                        "min": 5,
                        "max": 50,
                        "default": 30,
                        "description": "Horizon de contrôle pour l'optimisation"
                    },
                    "verbose": {
                        "type": "checkbox",
                        "default": False,
                        "description": "Mode verbeux pour le débogage"
                    },
                    "time_limit": {
                        "type": "number",
                        "min": 10,
                        "max": 600,
                        "default": 200,
                        "description": "Limite de temps pour l'optimisation (secondes)"
                    }
                },
                "requirements": ["V2G enabled", "Gurobi license"],
                "performance_profile": {
                    "optimality": 0.95,
                    "speed": 0.6,
                    "scalability": 0.7,
                    "robustness": 0.9
                }
            },
            "OCMF_G2V": {
                "class_name": "OCMF_G2V",
                "name": "OCMF G2V",
                "description": "Optimal Charging Management Framework sans V2G",
                "category": "MPC",
                "icon": "🔋",
                "complexity": "High",
                "parameters": {
                    "control_horizon": {
                        "type": "slider",
                        "min": 5,
                        "max": 50,
                        "default": 25,
                        "description": "Horizon de contrôle pour l'optimisation"
                    },
                    "verbose": {
                        "type": "checkbox",
                        "default": False,
                        "description": "Mode verbeux pour le débogage"
                    }
                },
                "requirements": ["Gurobi license"],
                "performance_profile": {
                    "optimality": 0.9,
                    "speed": 0.7,
                    "scalability": 0.8,
                    "robustness": 0.85
                }
            },
            "eMPC_V2G": {
                "class_name": "eMPC_V2G_v2",
                "name": "eMPC V2G",
                "description": "Economic Model Predictive Control avec V2G",
                "category": "MPC",
                "icon": "💰",
                "complexity": "High",
                "parameters": {
                    "control_horizon": {
                        "type": "slider",
                        "min": 5,
                        "max": 30,
                        "default": 15,
                        "description": "Horizon de contrôle économique"
                    },
                    "verbose": {
                        "type": "checkbox",
                        "default": False,
                        "description": "Mode verbeux"
                    }
                },
                "requirements": ["V2G enabled", "Price data"],
                "performance_profile": {
                    "optimality": 0.85,
                    "speed": 0.75,
                    "scalability": 0.75,
                    "robustness": 0.8
                }
            },
            "V2GProfitMax": {
                "class_name": "V2GProfitMaxOracle",
                "name": "V2G Profit Max (Oracle)",
                "description": "Solution optimale pour maximisation des profits",
                "category": "Oracle",
                "icon": "🏆",
                "complexity": "High",
                "parameters": {
                    "verbose": {
                        "type": "checkbox",
                        "default": True,
                        "description": "Afficher les détails d'optimisation"
                    }
                },
                "requirements": ["V2G enabled", "Full information"],
                "performance_profile": {
                    "optimality": 1.0,
                    "speed": 0.4,
                    "scalability": 0.5,
                    "robustness": 0.95
                }
            },
            "ChargeAsFastAsPossible": {
                "class_name": "ChargeAsFastAsPossible",
                "name": "Charge Rapide",
                "description": "Charge les VE le plus rapidement possible",
                "category": "Heuristic",
                "icon": "⚡",
                "complexity": "Low",
                "parameters": {
                    "verbose": {
                        "type": "checkbox",
                        "default": False,
                        "description": "Mode verbeux"
                    }
                },
                "requirements": [],
                "performance_profile": {
                    "optimality": 0.6,
                    "speed": 1.0,
                    "scalability": 1.0,
                    "robustness": 0.7
                }
            },
            "RoundRobin": {
                "class_name": "RoundRobin",
                "name": "Round Robin",
                "description": "Charge les VE en rotation équitable",
                "category": "Heuristic",
                "icon": "🔄",
                "complexity": "Low",
                "parameters": {
                    "verbose": {
                        "type": "checkbox",
                        "default": False,
                        "description": "Mode verbeux"
                    }
                },
                "requirements": [],
                "performance_profile": {
                    "optimality": 0.7,
                    "speed": 0.95,
                    "scalability": 0.95,
                    "robustness": 0.8
                }
            },
            "RandomAgent": {
                "class_name": "RandomAgent",
                "name": "Agent Aléatoire",
                "description": "Actions aléatoires pour test de référence",
                "category": "Baseline",
                "icon": "🎲",
                "complexity": "Low",
                "parameters": {
                    "verbose": {
                        "type": "checkbox",
                        "default": False,
                        "description": "Mode verbeux"
                    }
                },
                "requirements": [],
                "performance_profile": {
                    "optimality": 0.3,
                    "speed": 1.0,
                    "scalability": 1.0,
                    "robustness": 0.5
                }
            }
        }
    
    def render_agent_selection_panel(self):
        """Panneau de sélection d'agent avancé"""
        st.subheader("🤖 Sélection et Configuration d'Agent")
        
        # Filtres par catégorie
        categories = list(set(config["category"] for config in self.agent_configs.values()))
        selected_categories = st.multiselect(
            "Filtrer par catégorie:",
            categories,
            default=categories,
            help="Sélectionnez les catégories d'agents à afficher"
        )
        
        # Filtrer les agents
        filtered_agents = {
            k: v for k, v in self.agent_configs.items() 
            if v["category"] in selected_categories
        }
        
        # Sélection d'agent avec informations détaillées
        col1, col2 = st.columns([2, 1])
        
        with col1:
            agent_options = {
                k: f"{v['icon']} {v['name']} ({v['category']})" 
                for k, v in filtered_agents.items()
            }
            
            selected_agent = st.selectbox(
                "Choisissez un agent:",
                options=list(agent_options.keys()),
                format_func=lambda x: agent_options[x],
                key="agent_selector"
            )
        
        with col2:
            if selected_agent:
                agent_info = self.agent_configs[selected_agent]
                complexity_color = {
                    "Low": "🟢",
                    "Medium": "🟡", 
                    "High": "🔴"
                }.get(agent_info["complexity"], "⚪")
                
                st.metric("Complexité", f"{complexity_color} {agent_info['complexity']}")
        
        # Afficher les détails de l'agent
        if selected_agent:
            self._render_agent_details(selected_agent)
            
        return selected_agent
    
    def _render_agent_details(self, agent_key: str):
        """Affiche les détails d'un agent"""
        agent_info = self.agent_configs[agent_key]
        
        # Description et exigences
        st.info(f"**{agent_info['name']}**\n\n{agent_info['description']}")
        
        if agent_info["requirements"]:
            st.warning(f"**Exigences:** {', '.join(agent_info['requirements'])}")
        
        # Profil de performance
        st.subheader("📊 Profil de Performance")
        profile = agent_info["performance_profile"]
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Optimalité", f"{profile['optimality']:.1%}")
        with col2:
            st.metric("Vitesse", f"{profile['speed']:.1%}")
        with col3:
            st.metric("Scalabilité", f"{profile['scalability']:.1%}")
        with col4:
            st.metric("Robustesse", f"{profile['robustness']:.1%}")
        
        # Graphique radar du profil
        fig = go.Figure()
        
        categories = list(profile.keys())
        values = list(profile.values())
        
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=[cat.title() for cat in categories],
            fill='toself',
            name=agent_info['name']
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 1]
                )),
            showlegend=False,
            title=f"Profil de Performance - {agent_info['name']}",
            height=300
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def render_agent_parameters(self, agent_key: str) -> Dict[str, Any]:
        """Rendu des paramètres configurables de l'agent"""
        if agent_key not in self.agent_configs:
            return {}
        
        st.subheader("⚙️ Configuration des Paramètres")
        
        agent_info = self.agent_configs[agent_key]
        parameters = agent_info["parameters"]
        
        configured_params = {}
        
        for param_name, param_config in parameters.items():
            param_type = param_config["type"]
            
            if param_type == "slider":
                configured_params[param_name] = st.slider(
                    param_name.replace("_", " ").title(),
                    min_value=param_config["min"],
                    max_value=param_config["max"],
                    value=param_config["default"],
                    help=param_config["description"]
                )
            
            elif param_type == "checkbox":
                configured_params[param_name] = st.checkbox(
                    param_name.replace("_", " ").title(),
                    value=param_config["default"],
                    help=param_config["description"]
                )
            
            elif param_type == "number":
                configured_params[param_name] = st.number_input(
                    param_name.replace("_", " ").title(),
                    min_value=param_config.get("min", 0),
                    max_value=param_config.get("max", 1000),
                    value=param_config["default"],
                    help=param_config["description"]
                )
        
        return configured_params
    
    def add_performance_record(self, agent_name: str, performance: AgentPerformance):
        """Ajoute un enregistrement de performance"""
        self.agent_history.append({
            "timestamp": datetime.now(),
            "agent_name": agent_name,
            "performance": performance
        })
    
    def render_agent_comparison(self):
        """Rendu de la comparaison d'agents"""
        st.subheader("📈 Comparaison de Performance des Agents")
        
        if not self.agent_history:
            st.info("Aucune donnée de performance disponible. Lancez des simulations pour comparer les agents.")
            return
        
        # Créer un DataFrame des performances
        performance_data = []
        for record in self.agent_history:
            perf = record["performance"]
            performance_data.append({
                "Agent": perf.agent_name,
                "Timestamp": record["timestamp"],
                "Récompense Totale": perf.total_reward,
                "Récompense Moyenne": perf.avg_reward,
                "Énergie Totale": perf.total_energy,
                "Puissance Moyenne": perf.avg_power,
                "Temps d'Exécution": perf.execution_time,
                "Satisfaction Utilisateur": perf.user_satisfaction,
                "Efficacité Coût": perf.cost_efficiency
            })
        
        df = pd.DataFrame(performance_data)
        
        # Graphique de comparaison
        metrics = ["Récompense Totale", "Récompense Moyenne", "Énergie Totale", "Satisfaction Utilisateur"]
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=metrics,
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        agents = df["Agent"].unique()
        colors = px.colors.qualitative.Set1[:len(agents)]
        
        for i, metric in enumerate(metrics):
            row = (i // 2) + 1
            col = (i % 2) + 1
            
            for j, agent in enumerate(agents):
                agent_data = df[df["Agent"] == agent]
                fig.add_trace(
                    go.Bar(
                        x=agent_data["Agent"],
                        y=agent_data[metric],
                        name=agent,
                        marker_color=colors[j],
                        showlegend=(i == 0)
                    ),
                    row=row, col=col
                )
        
        fig.update_layout(height=600, title_text="Comparaison Multi-Critères des Agents")
        st.plotly_chart(fig, use_container_width=True)
        
        # Tableau détaillé
        st.subheader("📋 Tableau de Performance Détaillé")
        st.dataframe(df, use_container_width=True)


class AgentBenchmark:
    """Système de benchmark pour agents"""
    
    def __init__(self):
        self.benchmark_scenarios = {
            "light_load": {
                "name": "Charge Légère",
                "description": "Scénario avec peu de véhicules",
                "spawn_multiplier": 1.0,
                "simulation_length": 50
            },
            "heavy_load": {
                "name": "Charge Lourde", 
                "description": "Scénario avec beaucoup de véhicules",
                "spawn_multiplier": 8.0,
                "simulation_length": 100
            },
            "variable_load": {
                "name": "Charge Variable",
                "description": "Scénario avec charge variable",
                "spawn_multiplier": 5.0,
                "simulation_length": 150
            }
        }
    
    def render_benchmark_panel(self):
        """Panneau de configuration de benchmark"""
        st.subheader("🏁 Benchmark d'Agents")
        
        # Sélection des scénarios
        selected_scenarios = st.multiselect(
            "Scénarios de test:",
            list(self.benchmark_scenarios.keys()),
            format_func=lambda x: f"{self.benchmark_scenarios[x]['name']} - {self.benchmark_scenarios[x]['description']}",
            default=list(self.benchmark_scenarios.keys())
        )
        
        # Sélection des agents à tester
        agent_manager = AgentManager()
        available_agents = list(agent_manager.agent_configs.keys())
        
        selected_agents = st.multiselect(
            "Agents à tester:",
            available_agents,
            format_func=lambda x: agent_manager.agent_configs[x]['name'],
            default=available_agents[:3]  # Sélectionner les 3 premiers par défaut
        )
        
        # Paramètres de benchmark
        col1, col2 = st.columns(2)
        with col1:
            num_runs = st.number_input("Nombre d'exécutions par test:", min_value=1, max_value=10, value=3)
        with col2:
            timeout = st.number_input("Timeout par simulation (s):", min_value=60, max_value=3600, value=300)
        
        if st.button("🚀 Lancer le Benchmark", type="primary"):
            self._run_benchmark(selected_scenarios, selected_agents, num_runs, timeout)
    
    def _run_benchmark(self, scenarios: List[str], agents: List[str], num_runs: int, timeout: int):
        """Lance le benchmark"""
        st.info("🔄 Benchmark en cours... Cette opération peut prendre plusieurs minutes.")
        
        progress_bar = st.progress(0)
        total_tests = len(scenarios) * len(agents) * num_runs
        current_test = 0
        
        results = []
        
        for scenario in scenarios:
            for agent in agents:
                for run in range(num_runs):
                    current_test += 1
                    progress_bar.progress(current_test / total_tests)
                    
                    # Simuler l'exécution du test (à remplacer par la vraie logique)
                    time.sleep(0.1)  # Simulation
                    
                    # Résultats simulés
                    result = {
                        "scenario": scenario,
                        "agent": agent,
                        "run": run + 1,
                        "reward": np.random.normal(100, 20),
                        "energy": np.random.normal(50, 10),
                        "time": np.random.normal(5, 1)
                    }
                    results.append(result)
        
        # Afficher les résultats
        self._display_benchmark_results(results)
    
    def _display_benchmark_results(self, results: List[Dict]):
        """Affiche les résultats du benchmark"""
        st.success("✅ Benchmark terminé!")
        
        df = pd.DataFrame(results)
        
        # Graphique de performance par scénario
        fig = px.box(df, x="agent", y="reward", color="scenario",
                    title="Performance par Agent et Scénario")
        st.plotly_chart(fig, use_container_width=True)
        
        # Tableau de résultats agrégés
        summary = df.groupby(["scenario", "agent"]).agg({
            "reward": ["mean", "std"],
            "energy": ["mean", "std"],
            "time": ["mean", "std"]
        }).round(2)
        
        st.subheader("📊 Résultats Agrégés")
        st.dataframe(summary, use_container_width=True)
