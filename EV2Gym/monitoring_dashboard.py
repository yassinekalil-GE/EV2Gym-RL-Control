#!/usr/bin/env python3
"""
EV2Gym Monitoring and Analytics Dashboard

Comprehensive monitoring system with real-time metrics, alerts, and performance analytics.
Provides detailed insights into simulation performance and system health.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import time
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
import json


@dataclass
class Alert:
    """Classe pour représenter une alerte"""
    id: str
    timestamp: datetime
    level: str  # "info", "warning", "error", "critical"
    title: str
    message: str
    source: str
    resolved: bool = False


class AlertManager:
    """Gestionnaire d'alertes"""
    
    def __init__(self):
        self.alerts = []
        self.alert_rules = {
            "power_limit_exceeded": {
                "threshold": 0.9,
                "level": "warning",
                "title": "Limite de puissance approchée",
                "message": "La consommation de puissance dépasse 90% de la limite"
            },
            "power_limit_critical": {
                "threshold": 0.95,
                "level": "error",
                "title": "Limite de puissance critique",
                "message": "La consommation de puissance dépasse 95% de la limite"
            },
            "low_user_satisfaction": {
                "threshold": 0.7,
                "level": "warning",
                "title": "Satisfaction utilisateur faible",
                "message": "La satisfaction utilisateur est en dessous de 70%"
            },
            "agent_timeout": {
                "threshold": 10.0,
                "level": "error",
                "title": "Timeout de l'agent",
                "message": "L'agent prend plus de 10 secondes pour calculer une action"
            },
            "simulation_stalled": {
                "threshold": 30.0,
                "level": "critical",
                "title": "Simulation bloquée",
                "message": "Aucune progression depuis plus de 30 secondes"
            }
        }
    
    def check_alerts(self, env, simulation_data: Dict[str, Any]):
        """Vérifie et génère les alertes"""
        if not env or not simulation_data:
            return
        
        current_time = datetime.now()
        
        # Vérifier la limite de puissance
        if hasattr(env, 'transformers') and env.transformers:
            total_power = sum(getattr(tr, 'current_power', 0) for tr in env.transformers)
            total_limit = sum(tr.max_power for tr in env.transformers)
            
            if total_limit > 0:
                utilization = total_power / total_limit
                
                if utilization > self.alert_rules["power_limit_critical"]["threshold"]:
                    self._create_alert("power_limit_critical", current_time, 
                                     f"Utilisation: {utilization:.1%}")
                elif utilization > self.alert_rules["power_limit_exceeded"]["threshold"]:
                    self._create_alert("power_limit_exceeded", current_time,
                                     f"Utilisation: {utilization:.1%}")
        
        # Vérifier les temps de calcul
        if simulation_data.get('step_times'):
            recent_times = simulation_data['step_times'][-5:]  # 5 dernières étapes
            avg_time = np.mean(recent_times)
            
            if avg_time > self.alert_rules["agent_timeout"]["threshold"]:
                self._create_alert("agent_timeout", current_time,
                                 f"Temps moyen: {avg_time:.2f}s")
    
    def _create_alert(self, rule_key: str, timestamp: datetime, details: str = ""):
        """Crée une nouvelle alerte"""
        rule = self.alert_rules[rule_key]
        
        # Éviter les doublons récents (moins de 5 minutes)
        recent_alerts = [a for a in self.alerts 
                        if a.source == rule_key and 
                        (timestamp - a.timestamp).seconds < 300]
        
        if not recent_alerts:
            alert = Alert(
                id=f"{rule_key}_{int(timestamp.timestamp())}",
                timestamp=timestamp,
                level=rule["level"],
                title=rule["title"],
                message=f"{rule['message']}. {details}",
                source=rule_key
            )
            self.alerts.append(alert)
    
    def get_active_alerts(self) -> List[Alert]:
        """Retourne les alertes actives"""
        return [a for a in self.alerts if not a.resolved]
    
    def resolve_alert(self, alert_id: str):
        """Marque une alerte comme résolue"""
        for alert in self.alerts:
            if alert.id == alert_id:
                alert.resolved = True
                break


class PerformanceMonitor:
    """Moniteur de performance en temps réel"""
    
    def __init__(self):
        self.metrics_history = []
        self.kpi_targets = {
            "user_satisfaction": 0.8,
            "power_efficiency": 0.7,
            "cost_efficiency": 0.75,
            "response_time": 2.0
        }
    
    def calculate_kpis(self, env, simulation_data: Dict[str, Any]) -> Dict[str, float]:
        """Calcule les KPI en temps réel"""
        kpis = {}
        
        if not env or not simulation_data:
            return kpis
        
        # Satisfaction utilisateur (simulée)
        if hasattr(env, 'current_evs_parked') and env.current_evs_parked > 0:
            # Calcul simplifié basé sur le SOC moyen
            total_soc = 0
            ev_count = 0
            for cs in env.charging_stations:
                for ev in cs.evs_connected:
                    if ev is not None:
                        total_soc += ev.current_capacity / ev.battery_capacity
                        ev_count += 1
            
            kpis["user_satisfaction"] = total_soc / ev_count if ev_count > 0 else 0
        else:
            kpis["user_satisfaction"] = 0
        
        # Efficacité énergétique
        if simulation_data.get('power_consumption') and simulation_data.get('rewards'):
            total_power = sum(simulation_data['power_consumption'])
            total_reward = sum(simulation_data['rewards'])
            kpis["power_efficiency"] = total_reward / total_power if total_power > 0 else 0
        else:
            kpis["power_efficiency"] = 0
        
        # Efficacité des coûts
        if hasattr(env, 'total_cost') and simulation_data.get('rewards'):
            total_reward = sum(simulation_data['rewards'])
            kpis["cost_efficiency"] = total_reward / abs(env.total_cost) if env.total_cost != 0 else 0
        else:
            kpis["cost_efficiency"] = 0
        
        # Temps de réponse
        if simulation_data.get('step_times'):
            kpis["response_time"] = np.mean(simulation_data['step_times'][-10:])  # Moyenne des 10 dernières
        else:
            kpis["response_time"] = 0
        
        # Sauvegarder l'historique
        self.metrics_history.append({
            "timestamp": datetime.now(),
            "kpis": kpis.copy()
        })
        
        # Garder seulement les 100 dernières mesures
        if len(self.metrics_history) > 100:
            self.metrics_history = self.metrics_history[-100:]
        
        return kpis
    
    def render_kpi_dashboard(self, kpis: Dict[str, float]):
        """Affiche le dashboard des KPI"""
        st.subheader("📊 Indicateurs de Performance Clés (KPI)")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            satisfaction = kpis.get("user_satisfaction", 0)
            target = self.kpi_targets["user_satisfaction"]
            delta = satisfaction - target
            st.metric(
                "Satisfaction Utilisateur",
                f"{satisfaction:.1%}",
                delta=f"{delta:+.1%}",
                delta_color="normal"
            )
        
        with col2:
            power_eff = kpis.get("power_efficiency", 0)
            target = self.kpi_targets["power_efficiency"]
            delta = power_eff - target
            st.metric(
                "Efficacité Énergétique",
                f"{power_eff:.2f}",
                delta=f"{delta:+.2f}",
                delta_color="normal"
            )
        
        with col3:
            cost_eff = kpis.get("cost_efficiency", 0)
            target = self.kpi_targets["cost_efficiency"]
            delta = cost_eff - target
            st.metric(
                "Efficacité des Coûts",
                f"{cost_eff:.2f}",
                delta=f"{delta:+.2f}",
                delta_color="normal"
            )
        
        with col4:
            response_time = kpis.get("response_time", 0)
            target = self.kpi_targets["response_time"]
            delta = response_time - target
            st.metric(
                "Temps de Réponse",
                f"{response_time:.2f}s",
                delta=f"{delta:+.2f}s",
                delta_color="inverse"
            )
    
    def render_kpi_trends(self):
        """Affiche les tendances des KPI"""
        if len(self.metrics_history) < 2:
            st.info("Pas assez de données pour afficher les tendances")
            return
        
        st.subheader("📈 Tendances des KPI")
        
        # Préparer les données
        timestamps = [record["timestamp"] for record in self.metrics_history]
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=["Satisfaction Utilisateur", "Efficacité Énergétique", 
                          "Efficacité des Coûts", "Temps de Réponse"],
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        kpi_names = ["user_satisfaction", "power_efficiency", "cost_efficiency", "response_time"]
        
        for i, kpi_name in enumerate(kpi_names):
            row = (i // 2) + 1
            col = (i % 2) + 1
            
            values = [record["kpis"].get(kpi_name, 0) for record in self.metrics_history]
            target = self.kpi_targets[kpi_name]
            
            # Ligne des valeurs
            fig.add_trace(
                go.Scatter(
                    x=timestamps,
                    y=values,
                    mode='lines+markers',
                    name=kpi_name.replace("_", " ").title(),
                    showlegend=False
                ),
                row=row, col=col
            )
            
            # Ligne de cible
            fig.add_hline(
                y=target,
                line_dash="dash",
                line_color="red",
                row=row, col=col
            )
        
        fig.update_layout(height=600, title_text="Évolution des KPI dans le Temps")
        st.plotly_chart(fig, use_container_width=True)


class SystemHealthMonitor:
    """Moniteur de santé du système"""
    
    def __init__(self):
        self.health_metrics = {}
    
    def check_system_health(self, env, simulation_data: Dict[str, Any]) -> Dict[str, Any]:
        """Vérifie la santé du système"""
        health = {
            "overall_status": "healthy",
            "components": {},
            "issues": []
        }
        
        if not env:
            health["overall_status"] = "error"
            health["issues"].append("Environnement non initialisé")
            return health
        
        # Vérifier l'environnement
        env_health = self._check_environment_health(env)
        health["components"]["environment"] = env_health
        
        # Vérifier les données de simulation
        data_health = self._check_simulation_data_health(simulation_data)
        health["components"]["simulation_data"] = data_health
        
        # Vérifier les performances
        perf_health = self._check_performance_health(simulation_data)
        health["components"]["performance"] = perf_health
        
        # Déterminer le statut global
        component_statuses = [comp["status"] for comp in health["components"].values()]
        if "error" in component_statuses:
            health["overall_status"] = "error"
        elif "warning" in component_statuses:
            health["overall_status"] = "warning"
        
        return health
    
    def _check_environment_health(self, env) -> Dict[str, Any]:
        """Vérifie la santé de l'environnement"""
        health = {"status": "healthy", "metrics": {}, "issues": []}
        
        try:
            # Vérifier les transformateurs
            if hasattr(env, 'transformers') and env.transformers:
                total_power = sum(getattr(tr, 'current_power', 0) for tr in env.transformers)
                total_limit = sum(tr.max_power for tr in env.transformers)
                utilization = total_power / total_limit if total_limit > 0 else 0
                
                health["metrics"]["transformer_utilization"] = utilization
                
                if utilization > 0.95:
                    health["status"] = "error"
                    health["issues"].append("Utilisation transformateur critique")
                elif utilization > 0.8:
                    health["status"] = "warning"
                    health["issues"].append("Utilisation transformateur élevée")
            
            # Vérifier les stations de charge
            if hasattr(env, 'charging_stations'):
                active_stations = sum(1 for cs in env.charging_stations 
                                    if any(ev is not None for ev in cs.evs_connected))
                total_stations = len(env.charging_stations)
                
                health["metrics"]["active_stations_ratio"] = active_stations / total_stations if total_stations > 0 else 0
            
            # Vérifier les VE
            if hasattr(env, 'current_evs_parked'):
                health["metrics"]["connected_evs"] = env.current_evs_parked
        
        except Exception as e:
            health["status"] = "error"
            health["issues"].append(f"Erreur lors de la vérification: {str(e)}")
        
        return health
    
    def _check_simulation_data_health(self, simulation_data: Dict[str, Any]) -> Dict[str, Any]:
        """Vérifie la santé des données de simulation"""
        health = {"status": "healthy", "metrics": {}, "issues": []}
        
        if not simulation_data:
            health["status"] = "warning"
            health["issues"].append("Aucune donnée de simulation")
            return health
        
        # Vérifier la cohérence des données
        data_lengths = {
            key: len(value) for key, value in simulation_data.items() 
            if isinstance(value, list)
        }
        
        if data_lengths:
            max_length = max(data_lengths.values())
            min_length = min(data_lengths.values())
            
            health["metrics"]["data_consistency"] = min_length / max_length if max_length > 0 else 0
            
            if min_length / max_length < 0.9:
                health["status"] = "warning"
                health["issues"].append("Incohérence dans les longueurs de données")
        
        return health
    
    def _check_performance_health(self, simulation_data: Dict[str, Any]) -> Dict[str, Any]:
        """Vérifie la santé des performances"""
        health = {"status": "healthy", "metrics": {}, "issues": []}
        
        if not simulation_data or not simulation_data.get('step_times'):
            return health
        
        step_times = simulation_data['step_times']
        
        if step_times:
            avg_time = np.mean(step_times[-10:])  # Moyenne des 10 dernières
            max_time = max(step_times[-10:])
            
            health["metrics"]["avg_step_time"] = avg_time
            health["metrics"]["max_step_time"] = max_time
            
            if avg_time > 5.0:
                health["status"] = "error"
                health["issues"].append("Temps de calcul très élevé")
            elif avg_time > 2.0:
                health["status"] = "warning"
                health["issues"].append("Temps de calcul élevé")
        
        return health
    
    def render_health_dashboard(self, health: Dict[str, Any]):
        """Affiche le dashboard de santé du système"""
        st.subheader("🏥 Santé du Système")
        
        # Statut global
        status_colors = {
            "healthy": "🟢",
            "warning": "🟡",
            "error": "🔴"
        }
        
        status_icon = status_colors.get(health["overall_status"], "⚪")
        st.metric("Statut Global", f"{status_icon} {health['overall_status'].title()}")
        
        # Détails par composant
        if health.get("components"):
            st.subheader("🔧 État des Composants")
            
            for component, comp_health in health["components"].items():
                with st.expander(f"{component.replace('_', ' ').title()} - {status_colors.get(comp_health['status'], '⚪')}"):
                    
                    # Métriques
                    if comp_health.get("metrics"):
                        st.write("**Métriques:**")
                        for metric, value in comp_health["metrics"].items():
                            if isinstance(value, float):
                                st.write(f"- {metric.replace('_', ' ').title()}: {value:.3f}")
                            else:
                                st.write(f"- {metric.replace('_', ' ').title()}: {value}")
                    
                    # Problèmes
                    if comp_health.get("issues"):
                        st.write("**Problèmes détectés:**")
                        for issue in comp_health["issues"]:
                            st.warning(f"⚠️ {issue}")


class MonitoringDashboard:
    """Dashboard de monitoring principal"""
    
    def __init__(self):
        self.alert_manager = AlertManager()
        self.performance_monitor = PerformanceMonitor()
        self.health_monitor = SystemHealthMonitor()
    
    def render_monitoring_panel(self, env, simulation_data: Dict[str, Any]):
        """Rendu du panneau de monitoring complet"""
        
        # Vérifier les alertes
        self.alert_manager.check_alerts(env, simulation_data)
        
        # Calculer les KPI
        kpis = self.performance_monitor.calculate_kpis(env, simulation_data)
        
        # Vérifier la santé du système
        health = self.health_monitor.check_system_health(env, simulation_data)
        
        # Afficher les alertes actives
        active_alerts = self.alert_manager.get_active_alerts()
        if active_alerts:
            st.subheader("🚨 Alertes Actives")
            for alert in active_alerts[-5:]:  # Afficher les 5 dernières
                alert_color = {
                    "info": "info",
                    "warning": "warning", 
                    "error": "error",
                    "critical": "error"
                }.get(alert.level, "info")
                
                with st.container():
                    st.write(f"**{alert.title}** ({alert.level.upper()})")
                    st.write(f"{alert.message}")
                    st.write(f"*{alert.timestamp.strftime('%H:%M:%S')}*")
                    if st.button(f"Résoudre", key=f"resolve_{alert.id}"):
                        self.alert_manager.resolve_alert(alert.id)
                        st.rerun()
                st.divider()
        
        # Dashboard des KPI
        self.performance_monitor.render_kpi_dashboard(kpis)
        
        # Tendances des KPI
        self.performance_monitor.render_kpi_trends()
        
        # Santé du système
        self.health_monitor.render_health_dashboard(health)
