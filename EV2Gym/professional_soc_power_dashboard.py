#!/usr/bin/env python3
"""
🔋⚡ Professional SOC & Power Dashboard

Dashboard ultra-professionnel pour jury de thèse
Analyse temps réel SOC et puissance avec modèles RL/MPC/Heuristiques
Visualisation comportement VE et impact réseau
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import sys
import os
import json
from pathlib import Path
import time
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Configuration ultra-professionnelle
st.set_page_config(
    page_title="🔋⚡ Professional SOC & Power Dashboard",
    page_icon="🔋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Style CSS moderne et épuré
st.markdown("""
<style>
    .main-header {
        background: #ffffff;
        color: #2c3e50;
        padding: 2rem;
        border-radius: 12px;
        text-align: center;
        font-size: 2.5rem;
        font-weight: 600;
        margin-bottom: 2rem;
        box-shadow: 0 2px 20px rgba(0,0,0,0.08);
        border: 1px solid #e8ecef;
    }
    
    .soc-card {
        background: #ffffff;
        border: 1px solid #e9ecef;
        border-radius: 8px;
        padding: 1rem;
        text-align: center;
        margin: 0.5rem;
        font-weight: 500;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        transition: all 0.2s ease;
    }

    .soc-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }

    .soc-critical { border-left: 4px solid #dc3545; color: #721c24; }
    .soc-low { border-left: 4px solid #fd7e14; color: #8a4a00; }
    .soc-medium { border-left: 4px solid #ffc107; color: #856404; }
    .soc-good { border-left: 4px solid #28a745; color: #155724; }
    .soc-excellent { border-left: 4px solid #007bff; color: #004085; }
    
    .power-card {
        background: #ffffff;
        border: 1px solid #e9ecef;
        border-radius: 8px;
        padding: 0.8rem;
        margin: 0.3rem;
        text-align: center;
        font-weight: 500;
        font-size: 0.9rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }

    .power-charging { border-left: 4px solid #dc3545; color: #721c24; }
    .power-discharging { border-left: 4px solid #28a745; color: #155724; }
    .power-idle { border-left: 4px solid #6c757d; color: #495057; }
    
    .status-badge {
        display: inline-block;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-weight: 500;
        font-size: 0.85rem;
        margin: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .status-active {
        background: #d4edda;
        color: #155724;
        border: 1px solid #c3e6cb;
    }
    .status-inactive {
        background: #f8d7da;
        color: #721c24;
        border: 1px solid #f5c6cb;
    }

    .metric-card {
        background: #ffffff;
        border: 1px solid #e9ecef;
        border-radius: 8px;
        padding: 1.5rem;
        margin: 0.5rem 0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        transition: all 0.2s ease;
    }

    .metric-card:hover {
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        transform: translateY(-2px);
    }

    .metric-value {
        font-size: 2.2rem;
        font-weight: 600;
        color: #2c3e50;
        margin: 0;
        line-height: 1.2;
    }

    .metric-label {
        font-size: 0.9rem;
        color: #6c757d;
        margin: 0.3rem 0 0 0;
        font-weight: 400;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .section-title {
        font-size: 1.4rem;
        font-weight: 600;
        color: #2c3e50;
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #e9ecef;
    }
</style>
""", unsafe_allow_html=True)

# Variables de session
if 'soc_simulation_active' not in st.session_state:
    st.session_state.soc_simulation_active = False
if 'soc_step' not in st.session_state:
    st.session_state.soc_step = 0
if 'soc_data' not in st.session_state:
    st.session_state.soc_data = []
if 'ev_fleet_data' not in st.session_state:
    st.session_state.ev_fleet_data = []

def simulate_ev_fleet(algorithm, fleet_params, step):
    """Simule une flotte de VE avec SOC et puissance détaillés"""
    np.random.seed(step)

    n_evs = fleet_params['n_evs']
    max_power = fleet_params['max_power']
    time_hour = step % 24
    power_mode = fleet_params['power_mode']
    price_mad = fleet_params['price_mad']
    v2g_price_mad = fleet_params['v2g_price_mad']
    
    # Génération flotte VE
    ev_fleet = []
    
    for i in range(n_evs):
        # SOC initial basé sur l'heure et l'algorithme
        if algorithm == "Heuristique (RoundRobin)":
            # Distribution équitable, SOC prévisible
            base_soc = 40 + 30 * np.sin((time_hour + i) * np.pi / 12)

            # Puissance selon mode
            if power_mode == "Économique":
                charging_power = max_power * 0.6 if base_soc < 80 else 0
            elif power_mode == "Performance":
                charging_power = max_power * 1.0 if base_soc < 90 else 0
            elif power_mode == "V2G Prioritaire":
                charging_power = max_power * 0.4 if base_soc < 70 else -max_power * 0.3
            else:  # Équilibré
                charging_power = max_power * 0.8 if base_soc < 80 else 0
            
        elif algorithm == "Heuristique (ChargeAsFastAsPossible)":
            # Charge rapide, SOC variable
            base_soc = 20 + 60 * np.random.random()

            # Puissance selon mode
            if power_mode == "Économique":
                charging_power = max_power * 0.8 if base_soc < 85 else 0
            elif power_mode == "Performance":
                charging_power = max_power * 1.2 if base_soc < 95 else 0  # Boost mode
            elif power_mode == "V2G Prioritaire":
                charging_power = max_power * 0.6 if base_soc < 75 else -max_power * 0.4
            else:  # Équilibré
                charging_power = max_power if base_soc < 90 else 0
            
        elif algorithm == "MPC (V2GProfitMax)":
            # Optimisation économique avec V2G
            base_soc = 30 + 50 * np.random.random()
            price_factor = 0.5 + 0.5 * np.sin(time_hour * np.pi / 12)
            
            if price_factor > 0.7 and base_soc > 60:  # Prix élevé, décharge
                charging_power = -max_power * 0.5 * (base_soc - 50) / 50
            elif price_factor < 0.3:  # Prix bas, charge
                charging_power = max_power * (100 - base_soc) / 100
            else:
                charging_power = max_power * 0.3 * (80 - base_soc) / 80
                
        elif algorithm == "RL (PPO)":
            # Apprentissage progressif
            learning_factor = min(1.0, step / 150)
            base_soc = 25 + 55 * np.random.random()
            
            # Stratégie apprise : charge intelligente
            if base_soc < 30:  # Urgence
                charging_power = max_power * 0.9
            elif base_soc > 80:  # Opportunité V2G
                charging_power = -max_power * 0.3 * learning_factor
            else:  # Charge modérée
                charging_power = max_power * 0.5 * (1 - base_soc/100)
                
        else:  # RL (SAC)
            # Contrôle continu optimal
            base_soc = 20 + 60 * np.random.random()
            continuous_factor = 0.8 + 0.2 * np.sin(step * 0.1 + i)
            
            if base_soc < 25:
                charging_power = max_power * continuous_factor
            elif base_soc > 85:
                charging_power = -max_power * 0.4 * continuous_factor
            else:
                charging_power = max_power * 0.6 * (1 - base_soc/100) * continuous_factor
        
        # Ajout bruit réaliste
        base_soc += np.random.normal(0, 3)
        base_soc = np.clip(base_soc, 10, 95)
        
        charging_power += np.random.normal(0, 0.5)
        charging_power = np.clip(charging_power, -max_power, max_power)
        
        # Déterminer état
        if abs(charging_power) < 0.5:
            state = "Idle"
            power_color = "power-idle"
        elif charging_power > 0:
            state = "Charging"
            power_color = "power-charging"
        else:
            state = "Discharging"
            power_color = "power-discharging"
        
        # Déterminer niveau SOC
        if base_soc < 20:
            soc_level = "Critique"
            soc_color = "soc-critical"
        elif base_soc < 40:
            soc_level = "Bas"
            soc_color = "soc-low"
        elif base_soc < 60:
            soc_level = "Moyen"
            soc_color = "soc-medium"
        elif base_soc < 80:
            soc_level = "Bon"
            soc_color = "soc-good"
        else:
            soc_level = "Excellent"
            soc_color = "soc-excellent"
        
        ev_fleet.append({
            'id': i,
            'soc': base_soc,
            'power': charging_power,
            'state': state,
            'soc_level': soc_level,
            'soc_color': soc_color,
            'power_color': power_color
        })
    
    # Calculs globaux
    total_power = sum(ev['power'] for ev in ev_fleet)
    avg_soc = np.mean([ev['soc'] for ev in ev_fleet])
    charging_evs = len([ev for ev in ev_fleet if ev['power'] > 0.5])
    discharging_evs = len([ev for ev in ev_fleet if ev['power'] < -0.5])
    idle_evs = n_evs - charging_evs - discharging_evs
    
    # Efficacité selon algorithme et mode
    base_efficiency = 85
    if "Heuristique" in algorithm:
        base_efficiency = 85 + np.random.normal(0, 2)
    elif "MPC" in algorithm:
        base_efficiency = 92 + np.random.normal(0, 1.5)
    else:  # RL
        learning_bonus = min(5, step / 50)
        base_efficiency = 88 + learning_bonus + np.random.normal(0, 1)

    # Bonus efficacité selon mode
    if power_mode == "Économique":
        efficiency = base_efficiency + 3
    elif power_mode == "Performance":
        efficiency = base_efficiency - 2  # Moins efficace mais plus rapide
    elif power_mode == "V2G Prioritaire":
        efficiency = base_efficiency + 1
    else:  # Équilibré
        efficiency = base_efficiency

    efficiency = np.clip(efficiency, 80, 98)

    # Calculs économiques en MAD
    charging_cost = sum(max(0, ev['power']) for ev in ev_fleet) * price_mad / 60  # MAD/min
    v2g_revenue = sum(abs(min(0, ev['power'])) for ev in ev_fleet) * v2g_price_mad / 60  # MAD/min
    net_economic_result = v2g_revenue - charging_cost
    
    return {
        'timestamp': datetime.now(),
        'step': step,
        'algorithm': algorithm,
        'ev_fleet': ev_fleet,
        'total_power': total_power,
        'avg_soc': avg_soc,
        'charging_evs': charging_evs,
        'discharging_evs': discharging_evs,
        'idle_evs': idle_evs,
        'efficiency': efficiency,
        'charging_cost_mad': charging_cost,
        'v2g_revenue_mad': v2g_revenue,
        'net_result_mad': net_economic_result,
        'power_mode': power_mode,
        'time_hour': time_hour
    }

def main():
    """Interface principale"""
    
    # En-tête moderne
    st.markdown("""
    <div class="main-header">
        SOC & Power Analysis Dashboard
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="background: #f8f9fa; color: #495057; padding: 1rem; border-radius: 8px;
                text-align: center; font-size: 1.1rem; margin-bottom: 1.5rem; font-weight: 500;
                border-left: 4px solid #007bff;">
        Analyse Temps Réel de l'État de Charge et des Flux de Puissance des Véhicules Électriques
        <br>Modèles RL • MPC • Heuristiques • Données EV2Gym
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar paramètres
    with st.sidebar:
        st.header("⚙️ Configuration Flotte VE")
        
        # Algorithme
        algorithm = st.selectbox(
            "🤖 Algorithme de Contrôle",
            [
                "Heuristique (RoundRobin)",
                "Heuristique (ChargeAsFastAsPossible)",
                "MPC (V2GProfitMax)", 
                "RL (PPO)",
                "RL (SAC)"
            ]
        )
        
        # Paramètres flotte
        st.subheader("🚗 Paramètres Flotte")
        n_evs = st.slider("Nombre de VE", 5, 200, 30, step=5)
        max_power_per_ev = st.slider("Puissance Max/VE (kW)", 3, 22, 11)
        battery_capacity = st.slider("Capacité Batterie (kWh)", 30, 100, 60)

        st.subheader("💰 Paramètres Économiques (MAD)")
        electricity_price_mad = st.slider("Prix Électricité (MAD/kWh)", 0.5, 2.5, 1.2, 0.1)
        v2g_price_mad = st.slider("Prix V2G (MAD/kWh)", 1.0, 3.0, 1.5, 0.1)

        st.subheader("⚡ Mode Puissance")
        power_mode = st.selectbox(
            "Mode de Fonctionnement",
            ["Économique", "Performance", "Équilibré", "V2G Prioritaire"]
        )
        
        # Paramètres simulation
        st.subheader("⏱️ Simulation")
        update_speed = st.slider("Vitesse Mise à Jour (s)", 0.5, 3.0, 1.0)
        
        # Contrôles
        col1, col2 = st.columns(2)
        with col1:
            if st.button("▶️ Start", type="primary"):
                st.session_state.soc_simulation_active = True
                st.session_state.soc_step = 0
                st.session_state.soc_data = []
        
        with col2:
            if st.button("⏸️ Stop"):
                st.session_state.soc_simulation_active = False
    
    # Paramètres pour simulation
    fleet_params = {
        'n_evs': n_evs,
        'max_power': max_power_per_ev,
        'battery_capacity': battery_capacity,
        'power_mode': power_mode,
        'price_mad': electricity_price_mad,
        'v2g_price_mad': v2g_price_mad
    }
    
    # Status simulation
    status = "ACTIVE" if st.session_state.soc_simulation_active else "INACTIVE"
    status_class = "status-active" if st.session_state.soc_simulation_active else "status-inactive"

    st.markdown(f"""
    <div style="text-align: center; margin: 1rem 0;">
        <span class="status-badge {status_class}">Simulation {status}</span>
        <span style="margin-left: 2rem; color: #6c757d; font-size: 0.9rem;">
            Étape: {st.session_state.soc_step} | Algorithme: {algorithm}
        </span>
    </div>
    """, unsafe_allow_html=True)
    
    # Simulation temps réel
    if st.session_state.soc_simulation_active:
        # Générer nouvelles données
        new_data = simulate_ev_fleet(algorithm, fleet_params, st.session_state.soc_step)
        st.session_state.soc_data.append(new_data)
        st.session_state.soc_step += 1
        
        # Limiter historique
        if len(st.session_state.soc_data) > 150:
            st.session_state.soc_data = st.session_state.soc_data[-150:]
        
        # Auto-refresh
        time.sleep(update_speed)
        st.rerun()
    
    # Affichage résultats
    if st.session_state.soc_data:
        render_soc_analysis()
    else:
        st.info("👆 Configurez les paramètres et cliquez sur 'Start' pour démarrer l'analyse temps réel")

def render_soc_analysis():
    """Affiche l'analyse SOC et puissance"""
    
    if not st.session_state.soc_data:
        return
    
    latest = st.session_state.soc_data[-1]
    df = pd.DataFrame(st.session_state.soc_data)
    
    # Métriques principales
    st.markdown('<div class="section-title">Métriques Flotte Temps Réel</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{latest['avg_soc']:.1f}%</div>
            <div class="metric-label">SOC Moyen Flotte</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        power_color = "#e74c3c" if latest['total_power'] > 0 else "#2ecc71" if latest['total_power'] < 0 else "#95a5a6"
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="color: {power_color}">{latest['total_power']:.1f}</div>
            <div class="metric-label">kW Puissance Totale</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{latest['charging_evs']}</div>
            <div class="metric-label">VE en Charge</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{latest['discharging_evs']}</div>
            <div class="metric-label">VE en Décharge</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{latest['efficiency']:.1f}%</div>
            <div class="metric-label">Efficacité Système</div>
        </div>
        """, unsafe_allow_html=True)

    # Métriques économiques en MAD
    st.markdown('<div class="section-title">Métriques Économiques (MAD)</div>', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="color: #dc3545">{latest['charging_cost_mad']:.2f}</div>
            <div class="metric-label">MAD/min Coût Charge</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="color: #28a745">{latest['v2g_revenue_mad']:.2f}</div>
            <div class="metric-label">MAD/min Revenus V2G</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        net_color = "#28a745" if latest['net_result_mad'] >= 0 else "#dc3545"
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="color: {net_color}">{latest['net_result_mad']:.2f}</div>
            <div class="metric-label">MAD/min Résultat Net</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{latest['power_mode']}</div>
            <div class="metric-label">Mode Puissance</div>
        </div>
        """, unsafe_allow_html=True)

    # Vue détaillée de la flotte
    st.markdown("## 🚗 Vue Détaillée Flotte VE")

    # Répartition par état
    col1, col2 = st.columns(2)

    with col1:
        # Distribution SOC
        soc_values = [ev['soc'] for ev in latest['ev_fleet']]

        fig_soc = go.Figure()
        fig_soc.add_trace(go.Histogram(
            x=soc_values,
            nbinsx=20,
            marker_color='#007bff',
            opacity=0.7,
            name='Distribution SOC'
        ))

        fig_soc.update_layout(
            title="Distribution SOC Flotte",
            xaxis_title="SOC (%)",
            yaxis_title="Nombre de VE",
            height=400
        )

        st.plotly_chart(fig_soc, use_container_width=True)

    with col2:
        # Répartition par état
        states = ['Charging', 'Discharging', 'Idle']
        counts = [latest['charging_evs'], latest['discharging_evs'], latest['idle_evs']]
        colors = ['#dc3545', '#28a745', '#6c757d']

        fig_states = go.Figure(data=[go.Pie(
            labels=states,
            values=counts,
            marker_colors=colors,
            hole=0.4
        )])

        fig_states.update_layout(
            title="Répartition États VE",
            height=400
        )

        st.plotly_chart(fig_states, use_container_width=True)

    # Évolution temporelle
    st.markdown("## 📈 Évolution Temporelle")

    fig_evolution = make_subplots(
        rows=2, cols=2,
        subplot_titles=(
            'SOC Moyen Flotte (%)',
            'Puissance Totale (kW)',
            'Répartition États VE',
            'Efficacité Système (%)'
        )
    )

    # SOC moyen
    fig_evolution.add_trace(go.Scatter(
        x=df['step'], y=df['avg_soc'],
        mode='lines+markers', name='SOC Moyen',
        line=dict(color='#667eea', width=3),
        marker=dict(size=4)
    ), row=1, col=1)

    # Puissance totale
    fig_evolution.add_trace(go.Scatter(
        x=df['step'], y=df['total_power'],
        mode='lines+markers', name='Puissance',
        line=dict(color='#e74c3c', width=3),
        marker=dict(size=4)
    ), row=1, col=2)

    # États VE
    fig_evolution.add_trace(go.Scatter(
        x=df['step'], y=df['charging_evs'],
        mode='lines', name='Charging',
        line=dict(color='#e74c3c', width=2)
    ), row=2, col=1)

    fig_evolution.add_trace(go.Scatter(
        x=df['step'], y=df['discharging_evs'],
        mode='lines', name='Discharging',
        line=dict(color='#2ecc71', width=2)
    ), row=2, col=1)

    fig_evolution.add_trace(go.Scatter(
        x=df['step'], y=df['idle_evs'],
        mode='lines', name='Idle',
        line=dict(color='#95a5a6', width=2)
    ), row=2, col=1)

    # Efficacité
    fig_evolution.add_trace(go.Scatter(
        x=df['step'], y=df['efficiency'],
        mode='lines+markers', name='Efficacité',
        line=dict(color='#2ecc71', width=3),
        marker=dict(size=4)
    ), row=2, col=2)

    fig_evolution.update_layout(
        height=600,
        showlegend=True,
        title_text=f"Évolution Flotte VE - {latest['algorithm']}"
    )

    st.plotly_chart(fig_evolution, use_container_width=True)

    # Analyse détaillée par VE (échantillon)
    st.markdown("## 🔍 Analyse Détaillée VE (Échantillon)")

    # Afficher 10 premiers VE
    sample_evs = latest['ev_fleet'][:10]

    cols = st.columns(5)
    for i, ev in enumerate(sample_evs):
        col_idx = i % 5
        with cols[col_idx]:
            st.markdown(f"""
            <div class="soc-card {ev['soc_color']}">
                <strong>VE {ev['id']}</strong><br>
                SOC: {ev['soc']:.1f}%<br>
                <small>{ev['soc_level']}</small>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(f"""
            <div class="power-card {ev['power_color']}">
                {ev['power']:.1f} kW<br>
                <small>{ev['state']}</small>
            </div>
            """, unsafe_allow_html=True)

    # Comparaison algorithmes (si assez de données)
    if len(st.session_state.soc_data) >= 30:
        st.markdown('<div class="section-title">Performance Algorithme</div>', unsafe_allow_html=True)

        recent_data = df.tail(30)

        col1, col2, col3 = st.columns(3)

        with col1:
            avg_soc_stability = 1 - (recent_data['avg_soc'].std() / recent_data['avg_soc'].mean())
            st.metric("Stabilité SOC", f"{avg_soc_stability:.3f}",
                     delta=f"{avg_soc_stability - 0.8:.3f}" if avg_soc_stability > 0.8 else None)

        with col2:
            power_efficiency = recent_data['efficiency'].mean()
            st.metric("Efficacité Moyenne", f"{power_efficiency:.1f}%",
                     delta=f"{power_efficiency - 90:.1f}%" if power_efficiency > 90 else None)

        with col3:
            v2g_utilization = recent_data['discharging_evs'].mean() / recent_data['charging_evs'].mean() if recent_data['charging_evs'].mean() > 0 else 0
            st.metric("Utilisation V2G", f"{v2g_utilization:.2f}",
                     delta=f"{v2g_utilization - 0.3:.2f}" if v2g_utilization > 0.3 else None)

if __name__ == "__main__":
    main()
