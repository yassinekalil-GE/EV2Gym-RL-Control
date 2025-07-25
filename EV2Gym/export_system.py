#!/usr/bin/env python3
"""
EV2Gym Export and Reporting System

Comprehensive data export, report generation, and result comparison system.
Supports multiple formats and detailed analytics reports.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import json
import csv
import io
import zipfile
from datetime import datetime
from typing import Dict, Any, List, Optional
import base64
from pathlib import Path


class DataExporter:
    """Système d'export de données"""
    
    def __init__(self):
        self.export_formats = {
            "csv": {"name": "CSV", "extension": ".csv", "mime": "text/csv"},
            "json": {"name": "JSON", "extension": ".json", "mime": "application/json"},
            "excel": {"name": "Excel", "extension": ".xlsx", "mime": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"},
            "parquet": {"name": "Parquet", "extension": ".parquet", "mime": "application/octet-stream"}
        }
    
    def render_export_panel(self, env, simulation_data: Dict[str, Any]):
        """Panneau d'export de données"""
        st.subheader("📤 Export de Données")
        
        if not simulation_data or not simulation_data.get('rewards'):
            st.info("Aucune donnée de simulation à exporter")
            return
        
        # Sélection des données à exporter
        st.write("**Sélectionnez les données à exporter:**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            export_simulation = st.checkbox("Données de simulation", value=True)
            export_network = st.checkbox("Topologie du réseau", value=True)
            export_agents = st.checkbox("Configuration des agents", value=True)
        
        with col2:
            export_performance = st.checkbox("Métriques de performance", value=True)
            export_alerts = st.checkbox("Historique des alertes", value=False)
            export_config = st.checkbox("Configuration complète", value=True)
        
        # Sélection du format
        format_options = {k: v["name"] for k, v in self.export_formats.items()}
        selected_format = st.selectbox(
            "Format d'export:",
            options=list(format_options.keys()),
            format_func=lambda x: format_options[x]
        )
        
        # Options d'export
        with st.expander("Options avancées"):
            include_metadata = st.checkbox("Inclure les métadonnées", value=True)
            compress_data = st.checkbox("Compresser les données", value=False)
            timestamp_suffix = st.checkbox("Ajouter timestamp au nom", value=True)
        
        # Bouton d'export
        if st.button("📥 Exporter les Données", type="primary"):
            self._export_data(
                env, simulation_data,
                {
                    "simulation": export_simulation,
                    "network": export_network,
                    "agents": export_agents,
                    "performance": export_performance,
                    "alerts": export_alerts,
                    "config": export_config
                },
                selected_format,
                {
                    "metadata": include_metadata,
                    "compress": compress_data,
                    "timestamp": timestamp_suffix
                }
            )
    
    def _export_data(self, env, simulation_data: Dict[str, Any], 
                    data_selection: Dict[str, bool], format_type: str, 
                    options: Dict[str, bool]):
        """Exporte les données sélectionnées"""
        
        export_data = {}
        
        # Données de simulation
        if data_selection["simulation"]:
            export_data["simulation_metrics"] = {
                "rewards": simulation_data.get('rewards', []),
                "power_consumption": simulation_data.get('power_consumption', []),
                "ev_counts": simulation_data.get('ev_counts', []),
                "step_times": simulation_data.get('step_times', []),
                "total_reward": simulation_data.get('total_reward', 0),
                "total_cost": simulation_data.get('total_cost', 0)
            }
        
        # Topologie du réseau
        if data_selection["network"] and env:
            network_data = {
                "transformers": [],
                "charging_stations": [],
                "connected_evs": []
            }
            
            # Transformateurs
            for i, tr in enumerate(env.transformers):
                network_data["transformers"].append({
                    "id": i,
                    "max_power": tr.max_power,
                    "current_power": getattr(tr, 'current_power', 0)
                })
            
            # Stations de charge
            for i, cs in enumerate(env.charging_stations):
                cs_data = {
                    "id": i,
                    "n_ports": cs.n_ports,
                    "transformer_id": getattr(cs, 'transformer_id', i % env.number_of_transformers),
                    "current_power": getattr(cs, 'current_power', 0),
                    "connected_evs": []
                }
                
                # VE connectés
                for j, ev in enumerate(cs.evs_connected):
                    if ev is not None:
                        ev_data = {
                            "port_id": j,
                            "battery_capacity": ev.battery_capacity,
                            "current_capacity": ev.current_capacity,
                            "soc": ev.current_capacity / ev.battery_capacity,
                            "arrival_time": getattr(ev, 'arrival_time', None),
                            "departure_time": getattr(ev, 'departure_time', None)
                        }
                        cs_data["connected_evs"].append(ev_data)
                        network_data["connected_evs"].append({**ev_data, "station_id": i})
                
                network_data["charging_stations"].append(cs_data)
            
            export_data["network_topology"] = network_data
        
        # Métriques de performance
        if data_selection["performance"]:
            if hasattr(st.session_state, 'performance_monitor'):
                monitor = st.session_state.performance_monitor
                export_data["performance_metrics"] = {
                    "kpi_history": monitor.metrics_history,
                    "kpi_targets": monitor.kpi_targets
                }
        
        # Métadonnées
        if options["metadata"]:
            export_data["metadata"] = {
                "export_timestamp": datetime.now().isoformat(),
                "simulation_start": getattr(env, 'sim_starting_date', None),
                "current_step": getattr(env, 'current_step', 0),
                "simulation_length": getattr(env, 'simulation_length', 0),
                "number_of_stations": getattr(env, 'cs', 0),
                "number_of_transformers": getattr(env, 'number_of_transformers', 0),
                "v2g_enabled": getattr(env, 'v2g_enabled', False)
            }
        
        # Générer le fichier
        self._generate_export_file(export_data, format_type, options)
    
    def _generate_export_file(self, data: Dict[str, Any], format_type: str, options: Dict[str, bool]):
        """Génère le fichier d'export"""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_name = f"ev2gym_export"
        
        if options["timestamp"]:
            filename = f"{base_name}_{timestamp}"
        else:
            filename = base_name
        
        format_info = self.export_formats[format_type]
        
        if format_type == "json":
            # Export JSON
            json_str = json.dumps(data, indent=2, default=str)
            
            st.download_button(
                label=f"📥 Télécharger {format_info['name']}",
                data=json_str,
                file_name=f"{filename}{format_info['extension']}",
                mime=format_info['mime']
            )
        
        elif format_type == "csv":
            # Export CSV (données de simulation uniquement)
            if "simulation_metrics" in data:
                df = pd.DataFrame(data["simulation_metrics"])
                csv_buffer = io.StringIO()
                df.to_csv(csv_buffer, index=False)
                
                st.download_button(
                    label=f"📥 Télécharger {format_info['name']}",
                    data=csv_buffer.getvalue(),
                    file_name=f"{filename}{format_info['extension']}",
                    mime=format_info['mime']
                )
            else:
                st.error("Aucune donnée de simulation disponible pour l'export CSV")
        
        elif format_type == "excel":
            # Export Excel avec plusieurs feuilles
            excel_buffer = io.BytesIO()
            
            with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                
                # Feuille des métriques de simulation
                if "simulation_metrics" in data:
                    sim_df = pd.DataFrame(data["simulation_metrics"])
                    sim_df.to_excel(writer, sheet_name='Simulation_Metrics', index=False)
                
                # Feuille de la topologie
                if "network_topology" in data:
                    # Transformateurs
                    if data["network_topology"]["transformers"]:
                        tr_df = pd.DataFrame(data["network_topology"]["transformers"])
                        tr_df.to_excel(writer, sheet_name='Transformers', index=False)
                    
                    # Stations de charge
                    if data["network_topology"]["charging_stations"]:
                        cs_df = pd.DataFrame(data["network_topology"]["charging_stations"])
                        cs_df.to_excel(writer, sheet_name='Charging_Stations', index=False)
                    
                    # VE connectés
                    if data["network_topology"]["connected_evs"]:
                        ev_df = pd.DataFrame(data["network_topology"]["connected_evs"])
                        ev_df.to_excel(writer, sheet_name='Connected_EVs', index=False)
                
                # Métadonnées
                if "metadata" in data:
                    meta_df = pd.DataFrame([data["metadata"]])
                    meta_df.to_excel(writer, sheet_name='Metadata', index=False)
            
            st.download_button(
                label=f"📥 Télécharger {format_info['name']}",
                data=excel_buffer.getvalue(),
                file_name=f"{filename}{format_info['extension']}",
                mime=format_info['mime']
            )


class ReportGenerator:
    """Générateur de rapports"""
    
    def __init__(self):
        self.report_templates = {
            "executive_summary": {
                "name": "Résumé Exécutif",
                "description": "Rapport de haut niveau avec KPI principaux"
            },
            "technical_analysis": {
                "name": "Analyse Technique",
                "description": "Rapport détaillé avec analyses techniques"
            },
            "performance_comparison": {
                "name": "Comparaison de Performance",
                "description": "Comparaison entre différents agents/configurations"
            },
            "network_analysis": {
                "name": "Analyse du Réseau",
                "description": "Analyse détaillée de la topologie et des flux"
            }
        }
    
    def render_report_panel(self, env, simulation_data: Dict[str, Any]):
        """Panneau de génération de rapports"""
        st.subheader("📊 Génération de Rapports")
        
        # Sélection du type de rapport
        template_options = {k: f"{v['name']} - {v['description']}" 
                          for k, v in self.report_templates.items()}
        
        selected_template = st.selectbox(
            "Type de rapport:",
            options=list(template_options.keys()),
            format_func=lambda x: template_options[x]
        )
        
        # Options de rapport
        with st.expander("Options de rapport"):
            include_charts = st.checkbox("Inclure les graphiques", value=True)
            include_raw_data = st.checkbox("Inclure les données brutes", value=False)
            detailed_analysis = st.checkbox("Analyse détaillée", value=True)
        
        # Génération du rapport
        if st.button("📋 Générer le Rapport", type="primary"):
            self._generate_report(
                env, simulation_data, selected_template,
                {
                    "charts": include_charts,
                    "raw_data": include_raw_data,
                    "detailed": detailed_analysis
                }
            )
    
    def _generate_report(self, env, simulation_data: Dict[str, Any], 
                        template: str, options: Dict[str, bool]):
        """Génère un rapport selon le template sélectionné"""
        
        st.subheader(f"📋 {self.report_templates[template]['name']}")
        
        if template == "executive_summary":
            self._generate_executive_summary(env, simulation_data, options)
        elif template == "technical_analysis":
            self._generate_technical_analysis(env, simulation_data, options)
        elif template == "performance_comparison":
            self._generate_performance_comparison(env, simulation_data, options)
        elif template == "network_analysis":
            self._generate_network_analysis(env, simulation_data, options)
    
    def _generate_executive_summary(self, env, simulation_data: Dict[str, Any], options: Dict[str, bool]):
        """Génère un résumé exécutif"""
        
        st.markdown("## Résumé Exécutif - Simulation EV2Gym")
        st.markdown(f"**Date du rapport:** {datetime.now().strftime('%d/%m/%Y %H:%M')}")
        
        if not simulation_data or not simulation_data.get('rewards'):
            st.warning("Données de simulation insuffisantes pour générer le rapport")
            return
        
        # KPI principaux
        st.markdown("### 📊 Indicateurs Clés de Performance")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_reward = simulation_data.get('total_reward', 0)
            st.metric("Récompense Totale", f"{total_reward:.2f}")
        
        with col2:
            avg_reward = np.mean(simulation_data.get('rewards', [0]))
            st.metric("Récompense Moyenne", f"{avg_reward:.3f}")
        
        with col3:
            total_energy = sum(simulation_data.get('power_consumption', [0]))
            st.metric("Énergie Totale", f"{total_energy:.1f} kWh")
        
        with col4:
            if env:
                efficiency = total_reward / total_energy if total_energy > 0 else 0
                st.metric("Efficacité", f"{efficiency:.3f}")
        
        # Résumé de la simulation
        st.markdown("### 🎯 Résumé de la Simulation")
        
        if env:
            st.write(f"- **Durée:** {env.current_step} étapes sur {env.simulation_length}")
            st.write(f"- **Stations de charge:** {len(env.charging_stations)}")
            st.write(f"- **Transformateurs:** {env.number_of_transformers}")
            st.write(f"- **V2G activé:** {'Oui' if getattr(env, 'v2g_enabled', False) else 'Non'}")
            st.write(f"- **VE connectés:** {env.current_evs_parked}")
        
        # Graphique de performance
        if options["charts"] and simulation_data.get('rewards'):
            st.markdown("### 📈 Évolution de la Performance")
            
            fig = go.Figure()
            steps = list(range(len(simulation_data['rewards'])))
            
            fig.add_trace(go.Scatter(
                x=steps,
                y=simulation_data['rewards'],
                mode='lines',
                name='Récompense par Étape',
                line=dict(color='blue')
            ))
            
            fig.update_layout(
                title="Évolution de la Récompense",
                xaxis_title="Étapes",
                yaxis_title="Récompense",
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Recommandations
        st.markdown("### 💡 Recommandations")
        
        if avg_reward < 0:
            st.write("- ⚠️ Performance négative détectée - réviser la stratégie de l'agent")
        
        if env and hasattr(env, 'transformers'):
            total_power = sum(getattr(tr, 'current_power', 0) for tr in env.transformers)
            total_limit = sum(tr.max_power for tr in env.transformers)
            utilization = total_power / total_limit if total_limit > 0 else 0
            
            if utilization > 0.8:
                st.write("- ⚠️ Utilisation élevée du réseau - considérer l'ajout de capacité")
            else:
                st.write("- ✅ Utilisation du réseau dans les limites acceptables")
        
        if simulation_data.get('step_times'):
            avg_time = np.mean(simulation_data['step_times'])
            if avg_time > 2.0:
                st.write("- ⚠️ Temps de calcul élevé - optimiser l'algorithme de l'agent")
            else:
                st.write("- ✅ Performance de calcul satisfaisante")
    
    def _generate_technical_analysis(self, env, simulation_data: Dict[str, Any], options: Dict[str, bool]):
        """Génère une analyse technique détaillée"""
        
        st.markdown("## Analyse Technique Détaillée")
        
        # Analyse des performances
        st.markdown("### 🔬 Analyse des Performances")
        
        if simulation_data.get('rewards'):
            rewards = simulation_data['rewards']
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Statistiques des Récompenses:**")
                st.write(f"- Moyenne: {np.mean(rewards):.4f}")
                st.write(f"- Médiane: {np.median(rewards):.4f}")
                st.write(f"- Écart-type: {np.std(rewards):.4f}")
                st.write(f"- Min: {np.min(rewards):.4f}")
                st.write(f"- Max: {np.max(rewards):.4f}")
            
            with col2:
                # Histogramme des récompenses
                fig = go.Figure(data=[go.Histogram(x=rewards, nbinsx=20)])
                fig.update_layout(
                    title="Distribution des Récompenses",
                    xaxis_title="Récompense",
                    yaxis_title="Fréquence",
                    height=300
                )
                st.plotly_chart(fig, use_container_width=True)
        
        # Analyse de la consommation d'énergie
        if simulation_data.get('power_consumption'):
            st.markdown("### ⚡ Analyse de la Consommation d'Énergie")
            
            power_data = simulation_data['power_consumption']
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Statistiques de Puissance:**")
                st.write(f"- Puissance moyenne: {np.mean(power_data):.2f} kW")
                st.write(f"- Puissance max: {np.max(power_data):.2f} kW")
                st.write(f"- Énergie totale: {sum(power_data):.2f} kWh")
                
                if env and hasattr(env, 'transformers'):
                    total_limit = sum(tr.max_power for tr in env.transformers)
                    peak_utilization = np.max(power_data) / total_limit if total_limit > 0 else 0
                    st.write(f"- Utilisation pic: {peak_utilization:.1%}")
            
            with col2:
                # Graphique de consommation
                fig = go.Figure()
                steps = list(range(len(power_data)))
                
                fig.add_trace(go.Scatter(
                    x=steps,
                    y=power_data,
                    mode='lines',
                    name='Consommation',
                    line=dict(color='red')
                ))
                
                if env and hasattr(env, 'transformers'):
                    total_limit = sum(tr.max_power for tr in env.transformers)
                    fig.add_hline(y=total_limit, line_dash="dash", 
                                 annotation_text="Limite Réseau")
                
                fig.update_layout(
                    title="Profil de Consommation",
                    xaxis_title="Étapes",
                    yaxis_title="Puissance (kW)",
                    height=300
                )
                st.plotly_chart(fig, use_container_width=True)
    
    def _generate_performance_comparison(self, env, simulation_data: Dict[str, Any], options: Dict[str, bool]):
        """Génère un rapport de comparaison de performance"""
        st.markdown("## Comparaison de Performance")
        st.info("Fonctionnalité de comparaison en développement - nécessite plusieurs simulations")
    
    def _generate_network_analysis(self, env, simulation_data: Dict[str, Any], options: Dict[str, bool]):
        """Génère une analyse du réseau"""
        st.markdown("## Analyse du Réseau de Charge")
        
        if not env:
            st.warning("Environnement non disponible pour l'analyse du réseau")
            return
        
        # Statistiques du réseau
        st.markdown("### 🌐 Statistiques du Réseau")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Stations de Charge", len(env.charging_stations))
            st.metric("Transformateurs", env.number_of_transformers)
        
        with col2:
            total_ports = sum(cs.n_ports for cs in env.charging_stations)
            st.metric("Ports Totaux", total_ports)
            st.metric("VE Connectés", env.current_evs_parked)
        
        with col3:
            utilization = env.current_evs_parked / total_ports if total_ports > 0 else 0
            st.metric("Taux d'Occupation", f"{utilization:.1%}")
        
        # Analyse par transformateur
        st.markdown("### 🔌 Analyse par Transformateur")
        
        transformer_data = []
        for i, tr in enumerate(env.transformers):
            # Compter les stations connectées
            connected_stations = sum(1 for cs in env.charging_stations 
                                   if getattr(cs, 'transformer_id', cs.id % env.number_of_transformers) == i)
            
            transformer_data.append({
                "Transformateur": f"T{i}",
                "Puissance Max (kW)": tr.max_power,
                "Puissance Actuelle (kW)": getattr(tr, 'current_power', 0),
                "Utilisation (%)": (getattr(tr, 'current_power', 0) / tr.max_power * 100) if tr.max_power > 0 else 0,
                "Stations Connectées": connected_stations
            })
        
        df_transformers = pd.DataFrame(transformer_data)
        st.dataframe(df_transformers, use_container_width=True)


class ExportReportSystem:
    """Système complet d'export et de rapports"""
    
    def __init__(self):
        self.data_exporter = DataExporter()
        self.report_generator = ReportGenerator()
    
    def render_export_report_panel(self, env, simulation_data: Dict[str, Any]):
        """Panneau principal d'export et rapports"""
        
        tab1, tab2 = st.tabs(["📤 Export de Données", "📊 Génération de Rapports"])
        
        with tab1:
            self.data_exporter.render_export_panel(env, simulation_data)
        
        with tab2:
            self.report_generator.render_report_panel(env, simulation_data)
