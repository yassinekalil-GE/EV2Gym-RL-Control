#!/usr/bin/env python3
"""
EV2Gym Dashboard Components

Advanced visualization and monitoring components for the EV2Gym dashboard.
Includes network topology, power flow analysis, and detailed metrics visualization.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import networkx as nx
from typing import Dict, Any, List, Optional
import time


class NetworkTopologyVisualizer:
    """Visualiseur de topologie de réseau avancé"""
    
    def __init__(self):
        self.layout_cache = {}
    
    def create_3d_network_topology(self, env):
        """Crée une visualisation 3D de la topologie du réseau"""
        if not env:
            return None
        
        # Créer un graphe NetworkX
        G = nx.Graph()
        
        # Ajouter les transformateurs
        for i, transformer in enumerate(env.transformers):
            utilization = getattr(transformer, 'current_power', 0) / transformer.max_power
            G.add_node(f"T{i}", 
                      type="transformer", 
                      id=i,
                      power=getattr(transformer, 'current_power', 0),
                      limit=transformer.max_power,
                      utilization=utilization,
                      level=0)  # Niveau 0 pour transformateurs
        
        # Ajouter les stations de charge
        for i, cs in enumerate(env.charging_stations):
            evs_connected = sum(1 for ev in cs.evs_connected if ev is not None)
            power = getattr(cs, 'current_power', 0)
            
            G.add_node(f"CS{i}", 
                      type="charging_station", 
                      id=i,
                      power=power,
                      evs_connected=evs_connected,
                      utilization=evs_connected / cs.n_ports,
                      level=1)  # Niveau 1 pour stations
            
            # Connecter à un transformateur
            transformer_id = getattr(cs, 'transformer_id', i % env.number_of_transformers)
            G.add_edge(f"T{transformer_id}", f"CS{i}", weight=power)
        
        # Ajouter les VE comme nœuds
        for i, cs in enumerate(env.charging_stations):
            for j, ev in enumerate(cs.evs_connected):
                if ev is not None:
                    soc = ev.current_capacity / ev.battery_capacity
                    G.add_node(f"EV{i}_{j}",
                              type="ev",
                              id=f"{i}_{j}",
                              soc=soc,
                              capacity=ev.battery_capacity,
                              current_capacity=ev.current_capacity,
                              level=2)  # Niveau 2 pour VE
                    G.add_edge(f"CS{i}", f"EV{i}_{j}", weight=soc)
        
        # Calculer les positions 3D
        pos_2d = nx.spring_layout(G, k=2, iterations=50)
        
        # Convertir en 3D avec niveaux
        pos_3d = {}
        for node in G.nodes():
            x, y = pos_2d[node]
            z = G.nodes[node]['level'] * 2  # Espacement vertical
            pos_3d[node] = (x, y, z)
        
        return self._create_3d_plotly_figure(G, pos_3d)
    
    def _create_3d_plotly_figure(self, G, pos_3d):
        """Crée la figure Plotly 3D"""
        # Arêtes
        edge_x, edge_y, edge_z = [], [], []
        for edge in G.edges():
            x0, y0, z0 = pos_3d[edge[0]]
            x1, y1, z1 = pos_3d[edge[1]]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])
            edge_z.extend([z0, z1, None])
        
        edge_trace = go.Scatter3d(
            x=edge_x, y=edge_y, z=edge_z,
            mode='lines',
            line=dict(color='rgba(125,125,125,0.5)', width=2),
            hoverinfo='none',
            showlegend=False
        )
        
        # Nœuds par type
        traces = [edge_trace]
        
        # Transformateurs
        transformer_nodes = [n for n in G.nodes() if G.nodes[n]['type'] == 'transformer']
        if transformer_nodes:
            x_t = [pos_3d[n][0] for n in transformer_nodes]
            y_t = [pos_3d[n][1] for n in transformer_nodes]
            z_t = [pos_3d[n][2] for n in transformer_nodes]
            colors_t = [G.nodes[n]['utilization'] for n in transformer_nodes]
            text_t = [f"T{G.nodes[n]['id']}<br>Power: {G.nodes[n]['power']:.1f}kW<br>Limit: {G.nodes[n]['limit']}kW<br>Utilization: {G.nodes[n]['utilization']:.1%}" 
                     for n in transformer_nodes]
            
            traces.append(go.Scatter3d(
                x=x_t, y=y_t, z=z_t,
                mode='markers',
                marker=dict(size=15, color=colors_t, colorscale='Reds', 
                           symbol='square', showscale=True,
                           colorbar=dict(title="Utilisation", x=1.1)),
                text=text_t,
                hoverinfo='text',
                name='Transformateurs'
            ))
        
        # Stations de charge
        cs_nodes = [n for n in G.nodes() if G.nodes[n]['type'] == 'charging_station']
        if cs_nodes:
            x_cs = [pos_3d[n][0] for n in cs_nodes]
            y_cs = [pos_3d[n][1] for n in cs_nodes]
            z_cs = [pos_3d[n][2] for n in cs_nodes]
            colors_cs = [G.nodes[n]['evs_connected'] for n in cs_nodes]
            text_cs = [f"CS{G.nodes[n]['id']}<br>EVs: {G.nodes[n]['evs_connected']}<br>Power: {G.nodes[n]['power']:.1f}kW" 
                      for n in cs_nodes]
            
            traces.append(go.Scatter3d(
                x=x_cs, y=y_cs, z=z_cs,
                mode='markers',
                marker=dict(size=10, color=colors_cs, colorscale='Blues'),
                text=text_cs,
                hoverinfo='text',
                name='Stations de Charge'
            ))
        
        # Véhicules électriques
        ev_nodes = [n for n in G.nodes() if G.nodes[n]['type'] == 'ev']
        if ev_nodes:
            x_ev = [pos_3d[n][0] for n in ev_nodes]
            y_ev = [pos_3d[n][1] for n in ev_nodes]
            z_ev = [pos_3d[n][2] for n in ev_nodes]
            colors_ev = [G.nodes[n]['soc'] for n in ev_nodes]
            text_ev = [f"EV{G.nodes[n]['id']}<br>SOC: {G.nodes[n]['soc']:.1%}<br>Capacity: {G.nodes[n]['capacity']:.1f}kWh" 
                      for n in ev_nodes]
            
            traces.append(go.Scatter3d(
                x=x_ev, y=y_ev, z=z_ev,
                mode='markers',
                marker=dict(size=6, color=colors_ev, colorscale='Greens'),
                text=text_ev,
                hoverinfo='text',
                name='Véhicules Électriques'
            ))
        
        fig = go.Figure(data=traces)
        fig.update_layout(
            title='Topologie 3D du Réseau de Charge',
            scene=dict(
                xaxis_title='X',
                yaxis_title='Y',
                zaxis_title='Niveau',
                camera=dict(eye=dict(x=1.5, y=1.5, z=1.5))
            ),
            showlegend=True,
            height=600
        )
        
        return fig


class PowerFlowAnalyzer:
    """Analyseur de flux de puissance"""
    
    def create_power_flow_heatmap(self, env):
        """Crée une heatmap des flux de puissance"""
        if not env:
            return None
        
        # Créer une matrice de flux de puissance
        n_transformers = env.number_of_transformers
        n_stations = len(env.charging_stations)
        
        # Matrice transformateur -> station
        power_matrix = np.zeros((n_transformers, n_stations))
        
        for i, cs in enumerate(env.charging_stations):
            transformer_id = getattr(cs, 'transformer_id', i % n_transformers)
            power = getattr(cs, 'current_power', 0)
            power_matrix[transformer_id, i] = power
        
        # Créer la heatmap
        fig = go.Figure(data=go.Heatmap(
            z=power_matrix,
            x=[f'CS{i}' for i in range(n_stations)],
            y=[f'T{i}' for i in range(n_transformers)],
            colorscale='Viridis',
            colorbar=dict(title="Puissance (kW)")
        ))
        
        fig.update_layout(
            title='Flux de Puissance: Transformateurs → Stations',
            xaxis_title='Stations de Charge',
            yaxis_title='Transformateurs',
            height=400
        )
        
        return fig
    
    def create_load_profile_chart(self, env, simulation_data):
        """Crée un graphique de profil de charge"""
        if not simulation_data or not simulation_data.get('power_consumption'):
            return None
        
        steps = list(range(len(simulation_data['power_consumption'])))
        
        # Calculer les limites de transformateur
        transformer_limits = [tr.max_power for tr in env.transformers] if env else []
        total_limit = sum(transformer_limits) if transformer_limits else 100
        
        fig = go.Figure()
        
        # Consommation actuelle
        fig.add_trace(go.Scatter(
            x=steps,
            y=simulation_data['power_consumption'],
            mode='lines',
            name='Consommation Actuelle',
            line=dict(color='blue', width=2)
        ))
        
        # Limite de puissance
        fig.add_hline(
            y=total_limit,
            line_dash="dash",
            line_color="red",
            annotation_text=f"Limite Totale: {total_limit}kW"
        )
        
        # Zone de sécurité (80% de la limite)
        fig.add_hrect(
            y0=total_limit * 0.8,
            y1=total_limit,
            fillcolor="orange",
            opacity=0.2,
            annotation_text="Zone d'Alerte",
            annotation_position="top left"
        )
        
        fig.update_layout(
            title='Profil de Charge vs Limites du Réseau',
            xaxis_title='Étapes de Simulation',
            yaxis_title='Puissance (kW)',
            hovermode='x unified',
            height=400
        )
        
        return fig


class EVStateVisualizer:
    """Visualiseur d'état des véhicules électriques"""
    
    def create_soc_distribution(self, env):
        """Crée un histogramme de distribution des SOC"""
        if not env:
            return None
        
        soc_values = []
        for cs in env.charging_stations:
            for ev in cs.evs_connected:
                if ev is not None:
                    soc = ev.current_capacity / ev.battery_capacity
                    soc_values.append(soc * 100)  # Convertir en pourcentage
        
        if not soc_values:
            return None
        
        fig = go.Figure(data=[go.Histogram(
            x=soc_values,
            nbinsx=20,
            marker_color='green',
            opacity=0.7
        )])
        
        fig.update_layout(
            title='Distribution des États de Charge (SOC)',
            xaxis_title='État de Charge (%)',
            yaxis_title='Nombre de Véhicules',
            height=300
        )
        
        return fig
    
    def create_charging_status_pie(self, env):
        """Crée un graphique en secteurs du statut de charge"""
        if not env:
            return None
        
        charging = 0
        discharging = 0
        idle = 0
        
        for cs in env.charging_stations:
            for j, ev in enumerate(cs.evs_connected):
                if ev is not None:
                    # Obtenir l'action actuelle (simplifié)
                    port_idx = cs.id * cs.n_ports + j
                    if hasattr(env, 'last_actions') and port_idx < len(env.last_actions):
                        action = env.last_actions[port_idx]
                        if action > 0.1:
                            charging += 1
                        elif action < -0.1:
                            discharging += 1
                        else:
                            idle += 1
                    else:
                        idle += 1
        
        if charging + discharging + idle == 0:
            return None
        
        fig = go.Figure(data=[go.Pie(
            labels=['En Charge', 'En Décharge', 'Inactif'],
            values=[charging, discharging, idle],
            marker_colors=['green', 'red', 'gray']
        )])
        
        fig.update_layout(
            title='Statut de Charge des Véhicules',
            height=300
        )
        
        return fig


class PerformanceAnalyzer:
    """Analyseur de performance avancé"""
    
    def create_efficiency_metrics(self, simulation_data):
        """Crée des métriques d'efficacité"""
        if not simulation_data or not simulation_data.get('rewards'):
            return {}
        
        rewards = simulation_data['rewards']
        power_consumption = simulation_data.get('power_consumption', [])
        
        metrics = {
            'total_reward': sum(rewards),
            'avg_reward': np.mean(rewards),
            'reward_std': np.std(rewards),
            'total_energy': sum(power_consumption) if power_consumption else 0,
            'avg_power': np.mean(power_consumption) if power_consumption else 0,
            'power_efficiency': sum(rewards) / sum(power_consumption) if power_consumption and sum(power_consumption) > 0 else 0
        }
        
        return metrics
    
    def create_performance_radar(self, metrics):
        """Crée un graphique radar de performance"""
        if not metrics:
            return None
        
        categories = ['Récompense Totale', 'Récompense Moyenne', 'Stabilité', 
                     'Efficacité Énergétique', 'Utilisation Réseau']
        
        # Normaliser les valeurs (0-1)
        values = [
            min(metrics.get('total_reward', 0) / 1000, 1),  # Normaliser sur 1000
            min(metrics.get('avg_reward', 0) / 10, 1),      # Normaliser sur 10
            max(0, 1 - metrics.get('reward_std', 1)),       # Inverser la std
            min(metrics.get('power_efficiency', 0), 1),     # Déjà entre 0-1
            min(metrics.get('avg_power', 0) / 100, 1)       # Normaliser sur 100kW
        ]
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name='Performance Actuelle'
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 1]
                )),
            showlegend=True,
            title="Analyse de Performance Multi-Critères",
            height=400
        )
        
        return fig
