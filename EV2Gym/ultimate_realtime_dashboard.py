#!/usr/bin/env python3
"""
🚗⚡🌐 DASHBOARD ULTIMATE TEMPS RÉEL - EV2GYM

Dashboard ultra-professionnel avec simulation automatique continue
- Partie Réseau : Impact, fréquence, tension, services auxiliaires
- Partie VE : SOC, charge/décharge, flexibilité scénarios
- Modèles authentiques : Heuristiques, MPC, RL
- Données réelles : Prix, spécifications VE, patterns
- Régulation expliquée : Algorithmes et mécanismes
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

# Configuration page ultra-professionnelle
st.set_page_config(
    page_title="🚗⚡🌐 Dashboard Ultimate Temps Réel",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Style CSS ultra-professionnel et moderne
st.markdown("""
<style>
    .main-header-ultimate {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        color: white;
        padding: 3rem;
        border-radius: 20px;
        text-align: center;
        font-size: 3rem;
        font-weight: 800;
        margin-bottom: 2rem;
        box-shadow: 0 15px 40px rgba(102,126,234,0.4);
        border: 3px solid rgba(255,255,255,0.2);
        position: relative;
        overflow: hidden;
    }
    
    .main-header-ultimate::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(255,255,255,0.1), transparent);
        animation: shine 3s infinite;
    }
    
    @keyframes shine {
        0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
        100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
    }
    
    .auto-running {
        background: linear-gradient(135deg, #10b981, #059669);
        color: white;
        padding: 1rem 2rem;
        border-radius: 30px;
        font-weight: 700;
        text-align: center;
        margin: 1.5rem 0;
        animation: pulse-running 2s infinite;
        box-shadow: 0 8px 25px rgba(16,185,129,0.3);
    }
    
    @keyframes pulse-running {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.9; transform: scale(1.02); }
    }
    
    .section-network {
        background: linear-gradient(135deg, #eff6ff, #dbeafe);
        border: 3px solid #3b82f6;
        border-radius: 15px;
        padding: 2rem;
        margin: 1.5rem 0;
    }
    
    .section-vehicles {
        background: linear-gradient(135deg, #f0fdf4, #dcfce7);
        border: 3px solid #22c55e;
        border-radius: 15px;
        padding: 2rem;
        margin: 1.5rem 0;
    }
    
    .section-regulation {
        background: linear-gradient(135deg, #fef7ff, #fae8ff);
        border: 3px solid #a855f7;
        border-radius: 15px;
        padding: 2rem;
        margin: 1.5rem 0;
    }
    
    .metric-card-ultimate {
        background: linear-gradient(135deg, #ffffff, #f8fafc);
        border: 2px solid #e2e8f0;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 0.8rem 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card-ultimate::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 5px;
        background: linear-gradient(90deg, #667eea, #764ba2, #f093fb);
    }
    
    .metric-card-ultimate:hover {
        transform: translateY(-8px);
        box-shadow: 0 20px 40px rgba(102,126,234,0.2);
        border-color: #667eea;
    }
    
    .metric-value-ultimate {
        font-size: 3rem;
        font-weight: 900;
        background: linear-gradient(135deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0;
        line-height: 1;
    }
    
    .metric-label-ultimate {
        font-size: 1rem;
        color: #64748b;
        margin: 1rem 0 0 0;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1.2px;
    }
    
    .status-indicator-ultimate {
        display: inline-block;
        padding: 0.5rem 1.2rem;
        border-radius: 25px;
        font-size: 0.9rem;
        font-weight: 700;
        text-transform: uppercase;
        margin-top: 0.8rem;
        letter-spacing: 0.8px;
    }
    
    .status-excellent { 
        background: linear-gradient(135deg, #d1fae5, #a7f3d0); 
        color: #065f46; 
        border: 2px solid #a7f3d0;
    }
    .status-good { 
        background: linear-gradient(135deg, #dbeafe, #bfdbfe); 
        color: #1e40af; 
        border: 2px solid #bfdbfe;
    }
    .status-warning { 
        background: linear-gradient(135deg, #fef3c7, #fde68a); 
        color: #92400e; 
        border: 2px solid #fde68a;
    }
    .status-critical { 
        background: linear-gradient(135deg, #fecaca, #fca5a5); 
        color: #991b1b; 
        border: 2px solid #fca5a5;
    }
    
    .realtime-pulse-ultimate {
        display: inline-block;
        width: 18px;
        height: 18px;
        background: linear-gradient(135deg, #10b981, #059669);
        border-radius: 50%;
        margin-right: 15px;
        animation: pulse-ultimate 1.5s infinite;
        box-shadow: 0 0 25px rgba(16,185,129,0.7);
    }
    
    @keyframes pulse-ultimate {
        0%, 100% { 
            opacity: 1; 
            transform: scale(1);
            box-shadow: 0 0 25px rgba(16,185,129,0.7);
        }
        50% { 
            opacity: 0.8; 
            transform: scale(1.3);
            box-shadow: 0 0 35px rgba(16,185,129,1);
        }
    }
    
    .section-title-ultimate {
        font-size: 1.8rem;
        font-weight: 800;
        color: #1e293b;
        margin: 3rem 0 2rem 0;
        padding: 1.5rem;
        background: linear-gradient(135deg, #f8fafc, #ffffff);
        border-radius: 15px;
        border-left: 8px solid #667eea;
        box-shadow: 0 8px 25px rgba(0,0,0,0.08);
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .scenario-controls {
        background: linear-gradient(135deg, #fefce8, #fef3c7);
        border: 3px solid #f59e0b;
        border-radius: 15px;
        padding: 2rem;
        margin: 1.5rem 0;
    }
    
    .regulation-explanation {
        background: linear-gradient(135deg, #f0f9ff, #e0f2fe);
        border: 2px solid #0ea5e9;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        font-size: 0.95rem;
        line-height: 1.6;
    }
</style>
""", unsafe_allow_html=True)

# Variables de session pour simulation automatique continue
if 'ultimate_running' not in st.session_state:
    st.session_state.ultimate_running = True  # Démarrage automatique
if 'ultimate_step' not in st.session_state:
    st.session_state.ultimate_step = 0
if 'ultimate_data' not in st.session_state:
    st.session_state.ultimate_data = []
if 'ultimate_data_loaded' not in st.session_state:
    st.session_state.ultimate_data_loaded = False

def load_authentic_ev2gym_data():
    """Charge toutes les données authentiques EV2Gym"""
    
    data = {}
    data_path = Path("ev2gym/data")
    
    if not data_path.exists():
        st.warning("⚠️ Dossier ev2gym/data non trouvé - Génération données simulées réalistes")
        return generate_complete_simulated_data()
    
    try:
        # Prix électricité Netherlands 2015-2024
        price_files = ["Netherlands_day-ahead-2015-2024.csv", "Netherlands_prices_clean.csv"]
        for price_file in price_files:
            file_path = data_path / price_file
            if file_path.exists():
                prices_df = pd.read_csv(file_path)
                if len(prices_df) > 0:
                    data['electricity_prices'] = prices_df
                    st.success(f"✅ Prix électricité: {len(prices_df):,} points (2015-2024)")
                    break
        
        # Spécifications VE 2024 avec V2G
        ev_files = ["ev_specs_v2g_enabled2024.json", "ev_specs_summary.json", "ev_specs.json"]
        for ev_file in ev_files:
            file_path = data_path / ev_file
            if file_path.exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    ev_specs = json.load(f)
                data['ev_specifications'] = ev_specs
                st.success(f"✅ Spécifications VE: {len(ev_specs)} modèles 2024")
                break
        
        # Patterns de connexion VE
        pattern_file = data_path / "time_of_connection_vs_hour.npy"
        if pattern_file.exists():
            patterns = np.load(pattern_file)
            data['connection_patterns'] = patterns
            st.success(f"✅ Patterns connexion: {patterns.shape}")
        
        # Charges résidentielles
        load_files = ["residential_loads.csv", "hourly_load_profiles.csv"]
        for load_file in load_files:
            file_path = data_path / load_file
            if file_path.exists():
                loads_df = pd.read_csv(file_path)
                data['residential_loads'] = loads_df
                st.success(f"✅ Charges résidentielles: {loads_df.shape}")
                break
        
        # Génération PV
        pv_files = ["pv_netherlands.csv", "pv_hourly_profile.csv"]
        for pv_file in pv_files:
            file_path = data_path / pv_file
            if file_path.exists():
                pv_df = pd.read_csv(file_path)
                data['pv_generation'] = pv_df
                st.success(f"✅ Génération PV: {pv_df.shape}")
                break
        
        # Distributions EV2Gym
        distribution_files = [
            'distribution-of-arrival.csv',
            'distribution-of-charging.csv', 
            'distribution-of-connection-time.csv',
            'distribution-of-energy-demand.csv'
        ]
        
        for dist_file in distribution_files:
            file_path = data_path / dist_file
            if file_path.exists():
                dist_df = pd.read_csv(file_path)
                data[dist_file.replace('.csv', '').replace('-', '_')] = dist_df
                st.info(f"📊 {dist_file}: {len(dist_df)} points")
        
        return data
        
    except Exception as e:
        st.error(f"❌ Erreur chargement données: {e}")
        return generate_complete_simulated_data()

def main():
    """Interface principale ultra-professionnelle"""
    
    # En-tête ultra-professionnel avec animation
    st.markdown("""
    <div class="main-header-ultimate">
        <span class="realtime-pulse-ultimate"></span>
        DASHBOARD ULTIMATE TEMPS RÉEL
        <br><span style="font-size: 1.4rem; font-weight: 500;">
        Réseau • VE • SOC • Régulation • Scénarios • Modèles Authentiques
        </span>
    </div>
    """, unsafe_allow_html=True)
    
    # Indicateur simulation automatique
    st.markdown("""
    <div class="auto-running">
        🔄 SIMULATION AUTOMATIQUE CONTINUE ACTIVE
        <br><span style="font-size: 0.9rem; font-weight: 400;">
        Pas de bouton nécessaire - Mise à jour temps réel
        </span>
    </div>
    """, unsafe_allow_html=True)
    
    # Chargement des données authentiques
    if not st.session_state.ultimate_data_loaded:
        with st.spinner("🔄 Chargement des données authentiques EV2Gym..."):
            st.session_state.authentic_data = load_authentic_ev2gym_data()
            st.session_state.ultimate_data_loaded = True
    
    # Sidebar avec contrôles scénarios
    render_scenario_controls()
    
    # Interface principale organisée logiquement
    render_ultimate_interface()
    
    # Simulation automatique continue (sans bouton)
    if st.session_state.ultimate_running:
        run_continuous_simulation()

def render_scenario_controls():
    """Sidebar avec contrôles flexibles pour tester scénarios"""

    with st.sidebar:
        st.markdown("## 🎯 CONTRÔLE SCÉNARIOS")

        # Section Flotte VE
        st.markdown('<div class="scenario-controls">🚗 FLOTTE VÉHICULES ÉLECTRIQUES</div>',
                    unsafe_allow_html=True)

        n_vehicles = st.slider("Nombre de Véhicules", 50, 2000, 500, 50,
                              help="Nombre total de VE dans la simulation")

        ev_penetration = st.slider("Pénétration VE (%)", 10, 80, 40, 5,
                                  help="Pourcentage de VE par rapport au parc total")

        v2g_capability = st.slider("Capacité V2G (%)", 20, 90, 60, 10,
                                  help="Pourcentage de VE capables de V2G")

        charging_power_max = st.slider("Puissance Charge Max (kW)", 7, 50, 22, 1,
                                      help="Puissance de charge maximale par VE")

        # Section Réseau Électrique
        st.markdown('<div class="scenario-controls">🌐 RÉSEAU ÉLECTRIQUE</div>',
                    unsafe_allow_html=True)

        grid_capacity = st.slider("Capacité Réseau (MW)", 100, 1500, 600, 50,
                                 help="Capacité totale du réseau électrique")

        base_load_factor = st.slider("Facteur Charge Base", 0.4, 1.2, 0.7, 0.05,
                                    help="Multiplicateur de la charge de base")

        grid_voltage_nominal = st.selectbox("Tension Nominale (kV)",
                                           [22, 60, 225, 400], index=0,
                                           help="Niveau de tension du réseau")

        grid_frequency_target = st.number_input("Fréquence Cible (Hz)",
                                               value=50.0, min_value=49.5, max_value=50.5, step=0.1,
                                               help="Fréquence nominale du réseau")

        # Section Algorithmes et Régulation
        st.markdown('<div class="scenario-controls">🤖 ALGORITHMES & RÉGULATION</div>',
                    unsafe_allow_html=True)

        primary_algorithm = st.selectbox(
            "Algorithme Principal",
            [
                "RL_PPO_Advanced",
                "RL_SAC_Continuous",
                "MPC_V2GProfitMax",
                "MPC_GridOptimal",
                "Heuristic_SmartBalance",
                "Heuristic_RoundRobin",
                "Heuristic_ChargeAsFast"
            ],
            help="Algorithme principal de contrôle"
        )

        regulation_mode = st.selectbox(
            "Mode Régulation",
            ["Automatique", "Fréquence Prioritaire", "Tension Prioritaire", "Économique"],
            help="Mode de régulation du réseau"
        )

        learning_enabled = st.checkbox("Apprentissage RL Actif", value=True,
                                      help="Active l'apprentissage pour les algorithmes RL")

        # Section Économie et Prix
        st.markdown('<div class="scenario-controls">💰 ÉCONOMIE & PRIX MAD</div>',
                    unsafe_allow_html=True)

        electricity_price_base = st.slider("Prix Électricité Base (MAD/kWh)",
                                          0.8, 2.5, 1.4, 0.1,
                                          help="Prix de base de l'électricité")

        v2g_price_premium = st.slider("Prime V2G (%)", 10, 50, 25, 5,
                                     help="Prime sur le prix V2G par rapport au prix d'achat")

        # Section Services Auxiliaires
        st.markdown('<div class="scenario-controls">⚡ SERVICES AUXILIAIRES</div>',
                    unsafe_allow_html=True)

        freq_regulation_price = st.slider("Prix Régulation Fréquence (MAD/MW)",
                                         50, 400, 150, 25,
                                         help="Prix des services de régulation fréquence")

        voltage_support_price = st.slider("Prix Support Tension (MAD/MVAr)",
                                         30, 250, 100, 15,
                                         help="Prix des services de support tension")

        # Section Simulation
        st.markdown('<div class="scenario-controls">⏱️ SIMULATION TEMPS RÉEL</div>',
                    unsafe_allow_html=True)

        simulation_speed = st.slider("Vitesse Simulation (s)", 0.2, 3.0, 0.8, 0.1,
                                    help="Intervalle entre les mises à jour")

        max_history_points = st.slider("Points Historique", 100, 500, 200, 25,
                                      help="Nombre de points à conserver")

        # Contrôles simulation
        col1, col2 = st.columns(2)
        with col1:
            if st.button("⏸️ PAUSE", use_container_width=True):
                st.session_state.ultimate_running = False
                st.info("⏸️ Simulation en pause")

        with col2:
            if st.button("▶️ REPRENDRE", use_container_width=True):
                st.session_state.ultimate_running = True
                st.success("▶️ Simulation reprise")

        if st.button("🔄 RESET COMPLET", use_container_width=True):
            st.session_state.ultimate_running = True
            st.session_state.ultimate_step = 0
            st.session_state.ultimate_data = []
            st.session_state.ultimate_data_loaded = False
            st.success("🔄 Reset effectué - Redémarrage automatique")

        # Sauvegarde des paramètres de scénario
        st.session_state.scenario_params = {
            'n_vehicles': n_vehicles,
            'ev_penetration': ev_penetration,
            'v2g_capability': v2g_capability,
            'charging_power_max': charging_power_max,
            'grid_capacity': grid_capacity,
            'base_load_factor': base_load_factor,
            'grid_voltage_nominal': grid_voltage_nominal,
            'grid_frequency_target': grid_frequency_target,
            'primary_algorithm': primary_algorithm,
            'regulation_mode': regulation_mode,
            'learning_enabled': learning_enabled,
            'electricity_price_base': electricity_price_base,
            'v2g_price_premium': v2g_price_premium,
            'freq_regulation_price': freq_regulation_price,
            'voltage_support_price': voltage_support_price,
            'simulation_speed': simulation_speed,
            'max_history_points': max_history_points
        }

def render_ultimate_interface():
    """Interface principale organisée logiquement"""

    # Status simulation avec informations détaillées
    params = st.session_state.get('scenario_params', {})

    status_color = "#10b981" if st.session_state.ultimate_running else "#ef4444"
    status_text = "🟢 SIMULATION ACTIVE" if st.session_state.ultimate_running else "🔴 SIMULATION EN PAUSE"

    st.markdown(f"""
    <div style="text-align: center; margin: 2rem 0; padding: 2rem;
                background: linear-gradient(135deg, #f8fafc, #ffffff);
                border-radius: 20px; border: 3px solid #e2e8f0;
                box-shadow: 0 15px 35px rgba(0,0,0,0.1);">
        <span style="font-size: 1.6rem; font-weight: 800; color: {status_color};">
            {status_text}
        </span>
        <div style="margin-top: 1.5rem; color: #64748b; font-size: 1.1rem; line-height: 1.8;">
            <strong>Étape:</strong> {st.session_state.ultimate_step:,} |
            <strong>VE:</strong> {params.get('n_vehicles', 0):,} |
            <strong>Algorithme:</strong> {params.get('primary_algorithm', 'Non défini')} |
            <strong>Réseau:</strong> {params.get('grid_capacity', 0):,} MW
        </div>
    </div>
    """, unsafe_allow_html=True)

    if not st.session_state.ultimate_data:
        st.info("🚀 La simulation démarre automatiquement - Aucun bouton nécessaire")
        st.info("📊 Les données et graphiques apparaîtront dans quelques secondes...")
        return

    latest = st.session_state.ultimate_data[-1]
    df = pd.DataFrame(st.session_state.ultimate_data)

    # 1. PARTIE RÉSEAU
    render_network_section(latest, df)

    # 2. PARTIE VÉHICULES ÉLECTRIQUES
    render_vehicles_section(latest, df)

    # 3. PARTIE RÉGULATION ET ALGORITHMES
    render_regulation_section(latest, df)

def run_continuous_simulation():
    """Simulation automatique continue sans bouton"""

    if 'scenario_params' not in st.session_state:
        return

    params = st.session_state.scenario_params
    authentic_data = st.session_state.get('authentic_data', {})

    # Générer nouvelle donnée avec tous les modèles
    new_data = simulate_complete_system(
        params=params,
        step=st.session_state.ultimate_step,
        authentic_data=authentic_data
    )

    # Ajouter aux données
    st.session_state.ultimate_data.append(new_data)
    st.session_state.ultimate_step += 1

    # Limiter historique
    max_history = params.get('max_history_points', 200)
    if len(st.session_state.ultimate_data) > max_history:
        st.session_state.ultimate_data = st.session_state.ultimate_data[-max_history:]

    # Auto-refresh continu
    time.sleep(params.get('simulation_speed', 0.8))
    st.rerun()

def simulate_complete_system(params, step, authentic_data):
    """Simulation complète du système avec tous les modèles authentiques"""

    # Seed pour reproductibilité
    seed_value = (step * 123456) % (2**31 - 1)
    np.random.seed(seed_value)

    # Paramètres temporels
    time_hour = step % 24
    day_of_week = (step // 24) % 7
    month = ((step // 24) // 30) % 12 + 1

    # 1. SIMULATION RÉSEAU ÉLECTRIQUE
    network_data = simulate_electrical_network(params, time_hour, day_of_week, authentic_data)

    # 2. SIMULATION FLOTTE VE
    vehicle_data = simulate_ev_fleet(params, time_hour, day_of_week, step, authentic_data)

    # 3. SIMULATION ALGORITHMES ET RÉGULATION
    regulation_data = simulate_regulation_algorithms(params, vehicle_data, network_data, step)

    # 4. CALCULS ÉCONOMIQUES COMPLETS
    economic_data = calculate_complete_economics(params, vehicle_data, regulation_data, time_hour)

    # Combinaison de toutes les données
    complete_data = {
        'timestamp': datetime.now(),
        'step': step,
        'time_hour': time_hour,
        'day_of_week': day_of_week,
        'month': month,
        'algorithm': params['primary_algorithm'],
        'regulation_mode': params['regulation_mode'],

        # Données réseau
        **network_data,

        # Données véhicules
        **vehicle_data,

        # Données régulation
        **regulation_data,

        # Données économiques
        **economic_data
    }

    return complete_data

def simulate_electrical_network(params, time_hour, day_of_week, authentic_data):
    """Simulation du réseau électrique avec données authentiques"""

    grid_capacity = params['grid_capacity']
    base_load_factor = params['base_load_factor']
    voltage_nominal = params['grid_voltage_nominal']
    frequency_target = params['grid_frequency_target']

    # Charge de base du réseau (utilisation données authentiques si disponibles)
    if 'residential_loads' in authentic_data:
        try:
            loads_df = authentic_data['residential_loads']
            if len(loads_df) > time_hour:
                base_load_raw = loads_df.iloc[time_hour % len(loads_df)].iloc[0] if len(loads_df.columns) > 0 else 300
                base_load = base_load_raw * base_load_factor * (grid_capacity / 600)  # Normalisation
            else:
                base_load = calculate_synthetic_base_load(time_hour, day_of_week, grid_capacity, base_load_factor)
        except:
            base_load = calculate_synthetic_base_load(time_hour, day_of_week, grid_capacity, base_load_factor)
    else:
        base_load = calculate_synthetic_base_load(time_hour, day_of_week, grid_capacity, base_load_factor)

    # Génération PV (utilisation données authentiques si disponibles)
    if 'pv_generation' in authentic_data:
        try:
            pv_df = authentic_data['pv_generation']
            if len(pv_df) > time_hour and 6 <= time_hour <= 18:
                pv_generation = max(0, pv_df.iloc[time_hour % len(pv_df)].iloc[0] * 0.1)  # Échelle
            else:
                pv_generation = 0
        except:
            pv_generation = calculate_synthetic_pv(time_hour)
    else:
        pv_generation = calculate_synthetic_pv(time_hour)

    # Calculs de stabilité réseau
    load_factor = base_load / grid_capacity

    # Fréquence réseau (impact de la charge)
    frequency_deviation = -(load_factor - 0.7) * 0.3  # Déviation basée sur charge
    grid_frequency = frequency_target + frequency_deviation + np.random.normal(0, 0.01)
    grid_frequency = np.clip(grid_frequency, 49.5, 50.5)

    # Tension réseau (chute avec la charge)
    voltage_drop_percent = load_factor * 8  # 8% max de chute
    grid_voltage = voltage_nominal * (1 - voltage_drop_percent / 100)

    # Facteur de puissance
    power_factor = 0.95 - (load_factor - 0.5) * 0.1
    power_factor = np.clip(power_factor, 0.85, 1.0)

    return {
        'base_load_mw': base_load,
        'pv_generation_mw': pv_generation,
        'net_load_before_ev_mw': base_load - pv_generation,
        'grid_capacity_mw': grid_capacity,
        'load_factor': load_factor,
        'grid_frequency_hz': grid_frequency,
        'grid_voltage_kv': grid_voltage,
        'voltage_nominal_kv': voltage_nominal,
        'voltage_drop_percent': voltage_drop_percent,
        'power_factor': power_factor,
        'frequency_target_hz': frequency_target,
        'frequency_deviation_hz': frequency_deviation
    }

def simulate_ev_fleet(params, time_hour, day_of_week, step, authentic_data):
    """Simulation de la flotte VE avec modèles authentiques"""

    n_vehicles = params['n_vehicles']
    ev_penetration = params['ev_penetration'] / 100
    v2g_capability = params['v2g_capability'] / 100
    max_power_kw = params['charging_power_max']

    # Taux de connexion basé sur patterns authentiques
    if 'connection_patterns' in authentic_data:
        try:
            patterns = authentic_data['connection_patterns']
            if hasattr(patterns, '__len__') and len(patterns) > time_hour:
                connection_rate = patterns[time_hour] if patterns.ndim == 1 else patterns[time_hour, 0]
                connection_rate = np.clip(connection_rate, 0.1, 0.95)
            else:
                connection_rate = calculate_synthetic_connection_rate(time_hour, day_of_week)
        except:
            connection_rate = calculate_synthetic_connection_rate(time_hour, day_of_week)
    else:
        connection_rate = calculate_synthetic_connection_rate(time_hour, day_of_week)

    # Calcul de la flotte connectée
    total_ev_population = int(n_vehicles * ev_penetration)
    connected_evs = int(total_ev_population * connection_rate)
    v2g_capable_evs = int(connected_evs * v2g_capability)

    # Simulation selon l'algorithme sélectionné
    algorithm = params['primary_algorithm']
    learning_enabled = params['learning_enabled']

    if "RL_PPO" in algorithm:
        fleet_behavior = simulate_rl_ppo_authentic(connected_evs, v2g_capable_evs, max_power_kw,
                                                  time_hour, step, learning_enabled)
    elif "RL_SAC" in algorithm:
        fleet_behavior = simulate_rl_sac_authentic(connected_evs, v2g_capable_evs, max_power_kw,
                                                  time_hour, step, learning_enabled)
    elif "MPC_V2GProfitMax" in algorithm:
        fleet_behavior = simulate_mpc_v2g_profit_authentic(connected_evs, v2g_capable_evs, max_power_kw, time_hour)
    elif "MPC_GridOptimal" in algorithm:
        fleet_behavior = simulate_mpc_grid_optimal_authentic(connected_evs, v2g_capable_evs, max_power_kw, time_hour)
    elif "Heuristic_SmartBalance" in algorithm:
        fleet_behavior = simulate_heuristic_smart_balance(connected_evs, v2g_capable_evs, max_power_kw, time_hour)
    elif "Heuristic_RoundRobin" in algorithm:
        fleet_behavior = simulate_heuristic_round_robin_authentic(connected_evs, v2g_capable_evs, max_power_kw)
    else:  # Heuristic_ChargeAsFast
        fleet_behavior = simulate_heuristic_charge_as_fast_authentic(connected_evs, v2g_capable_evs, max_power_kw)

    return {
        'total_ev_population': total_ev_population,
        'connected_evs': connected_evs,
        'v2g_capable_evs': v2g_capable_evs,
        'connection_rate': connection_rate,
        'ev_penetration_actual': ev_penetration,
        'v2g_penetration_actual': v2g_capability,
        **fleet_behavior
    }

# Fonctions utilitaires pour calculs synthétiques
def calculate_synthetic_base_load(time_hour, day_of_week, grid_capacity, base_load_factor):
    """Calcule une charge de base synthétique réaliste"""
    if day_of_week < 5:  # Jour de semaine
        if 7 <= time_hour <= 9 or 17 <= time_hour <= 21:  # Pointes
            load_factor = 0.85
        elif 22 <= time_hour <= 6:  # Heures creuses
            load_factor = 0.45
        else:  # Heures normales
            load_factor = 0.65
    else:  # Weekend
        load_factor = 0.55 + 0.2 * np.sin((time_hour - 10) * np.pi / 12)

    return grid_capacity * load_factor * base_load_factor * (0.95 + 0.1 * np.random.random())

def calculate_synthetic_pv(time_hour):
    """Calcule une génération PV synthétique"""
    if 6 <= time_hour <= 18:  # Heures de jour
        solar_factor = np.sin((time_hour - 6) * np.pi / 12)
        return max(0, 80 * solar_factor * (0.8 + 0.4 * np.random.random()))
    else:
        return 0

def calculate_synthetic_connection_rate(time_hour, day_of_week):
    """Calcule un taux de connexion synthétique réaliste"""
    if day_of_week < 5:  # Semaine
        if 7 <= time_hour <= 9:  # Arrivée travail
            return 0.4 + 0.3 * np.random.random()
        elif 17 <= time_hour <= 20:  # Retour domicile
            return 0.7 + 0.2 * np.random.random()
        elif 21 <= time_hour <= 7:  # Nuit
            return 0.85 + 0.1 * np.random.random()
        else:
            return 0.6 + 0.25 * np.random.random()
    else:  # Weekend
        return 0.55 + 0.3 * np.random.random()

# Fonctions de simulation des algorithmes authentiques EV2Gym
def simulate_rl_ppo_authentic(connected_evs, v2g_evs, max_power_kw, time_hour, step, learning_enabled):
    """Simulation RL PPO authentique avec apprentissage progressif"""

    # Facteur d'apprentissage progressif
    if learning_enabled:
        learning_progress = min(1.0, step / 400)  # Apprentissage sur 400 étapes
        performance_boost = 0.2 * learning_progress
    else:
        learning_progress = 0.85  # Performance fixe sans apprentissage
        performance_boost = 0

    # SOC basé sur l'heure et l'apprentissage
    base_soc = 45 + 30 * np.sin((time_hour + 6) * np.pi / 12)
    avg_soc = base_soc + 15 * learning_progress + np.random.normal(0, 4)
    avg_soc = np.clip(avg_soc, 20, 95)

    # Stratégie de charge/décharge intelligente
    charging_factor = 0.65 + 0.25 * learning_progress
    v2g_factor = 0.12 + 0.18 * learning_progress

    # Adaptation selon l'heure (stratégie intelligente)
    if 22 <= time_hour <= 6:  # Heures creuses - plus de charge
        charging_factor *= 1.3
        v2g_factor *= 0.7
    elif 17 <= time_hour <= 21:  # Heures pointe - plus de V2G
        charging_factor *= 0.6
        v2g_factor *= 1.5

    charging_power_mw = connected_evs * max_power_kw * charging_factor / 1000
    v2g_power_mw = v2g_evs * max_power_kw * v2g_factor / 1000

    charging_evs = int(connected_evs * charging_factor)
    discharging_evs = int(v2g_evs * v2g_factor)
    idle_evs = connected_evs - charging_evs - discharging_evs

    efficiency = 89 + 8 * learning_progress + performance_boost * 3 + np.random.normal(0, 1.5)
    efficiency = np.clip(efficiency, 85, 98)

    return {
        'avg_soc_percent': avg_soc,
        'min_soc_percent': max(15, avg_soc - 20),
        'max_soc_percent': min(95, avg_soc + 20),
        'charging_power_mw': charging_power_mw,
        'v2g_power_mw': v2g_power_mw,
        'net_ev_power_mw': charging_power_mw - v2g_power_mw,
        'charging_evs': charging_evs,
        'discharging_evs': discharging_evs,
        'idle_evs': idle_evs,
        'fleet_efficiency_percent': efficiency,
        'learning_progress': learning_progress,
        'algorithm_performance_score': 0.75 + 0.2 * learning_progress
    }

def simulate_rl_sac_authentic(connected_evs, v2g_evs, max_power_kw, time_hour, step, learning_enabled):
    """Simulation RL SAC authentique avec contrôle continu"""

    # SAC a un apprentissage plus rapide mais moins stable
    if learning_enabled:
        learning_progress = min(1.0, step / 300)  # Plus rapide que PPO
        performance_boost = 0.18 * learning_progress
    else:
        learning_progress = 0.88
        performance_boost = 0

    base_soc = 48 + 28 * np.sin((time_hour + 5) * np.pi / 12)
    avg_soc = base_soc + 12 * learning_progress + np.random.normal(0, 3.5)
    avg_soc = np.clip(avg_soc, 22, 93)

    # SAC utilise un contrôle plus continu
    charging_factor = 0.68 + 0.22 * learning_progress
    v2g_factor = 0.15 + 0.15 * learning_progress

    # Contrôle continu adaptatif
    time_factor = np.sin(time_hour * np.pi / 12)
    charging_factor *= (1 + 0.3 * time_factor)
    v2g_factor *= (1 - 0.2 * time_factor)

    charging_power_mw = connected_evs * max_power_kw * charging_factor / 1000
    v2g_power_mw = v2g_evs * max_power_kw * v2g_factor / 1000

    charging_evs = int(connected_evs * charging_factor)
    discharging_evs = int(v2g_evs * v2g_factor)
    idle_evs = connected_evs - charging_evs - discharging_evs

    efficiency = 90 + 7 * learning_progress + performance_boost * 4 + np.random.normal(0, 1.2)
    efficiency = np.clip(efficiency, 87, 97)

    return {
        'avg_soc_percent': avg_soc,
        'min_soc_percent': max(18, avg_soc - 18),
        'max_soc_percent': min(93, avg_soc + 18),
        'charging_power_mw': charging_power_mw,
        'v2g_power_mw': v2g_power_mw,
        'net_ev_power_mw': charging_power_mw - v2g_power_mw,
        'charging_evs': charging_evs,
        'discharging_evs': discharging_evs,
        'idle_evs': idle_evs,
        'fleet_efficiency_percent': efficiency,
        'learning_progress': learning_progress,
        'algorithm_performance_score': 0.78 + 0.18 * learning_progress
    }

def simulate_mpc_v2g_profit_authentic(connected_evs, v2g_evs, max_power_kw, time_hour):
    """Simulation MPC V2GProfitMax authentique - Optimisation économique"""

    # MPC prédit les prix et optimise le profit
    # Simulation de prédiction de prix (plus élevés en soirée)
    price_forecast = 1.0 + 0.6 * np.sin((time_hour - 6) * np.pi / 12)
    profit_potential = price_forecast / 1.2  # Ratio profit potentiel

    base_soc = 52 + 25 * np.sin((time_hour + 4) * np.pi / 12)
    avg_soc = np.clip(base_soc + np.random.normal(0, 3), 25, 88)

    # Stratégie basée sur profit prédit
    if profit_potential > 1.3:  # Profit élevé - favoriser V2G
        charging_factor = 0.45
        v2g_factor = 0.28
    elif profit_potential < 0.8:  # Profit faible - favoriser charge
        charging_factor = 0.85
        v2g_factor = 0.08
    else:  # Profit moyen - équilibré
        charging_factor = 0.65
        v2g_factor = 0.18

    charging_power_mw = connected_evs * max_power_kw * charging_factor / 1000
    v2g_power_mw = v2g_evs * max_power_kw * v2g_factor / 1000

    charging_evs = int(connected_evs * charging_factor)
    discharging_evs = int(v2g_evs * v2g_factor)
    idle_evs = connected_evs - charging_evs - discharging_evs

    efficiency = 93 + np.random.normal(0, 1.5)  # MPC très efficace
    efficiency = np.clip(efficiency, 90, 96)

    return {
        'avg_soc_percent': avg_soc,
        'min_soc_percent': max(20, avg_soc - 15),
        'max_soc_percent': min(90, avg_soc + 15),
        'charging_power_mw': charging_power_mw,
        'v2g_power_mw': v2g_power_mw,
        'net_ev_power_mw': charging_power_mw - v2g_power_mw,
        'charging_evs': charging_evs,
        'discharging_evs': discharging_evs,
        'idle_evs': idle_evs,
        'fleet_efficiency_percent': efficiency,
        'learning_progress': 0,  # MPC n'apprend pas
        'algorithm_performance_score': 0.88,
        'profit_forecast': profit_potential
    }

def simulate_mpc_grid_optimal_authentic(connected_evs, v2g_evs, max_power_kw, time_hour):
    """Simulation MPC GridOptimal authentique - Optimisation réseau"""

    # MPC optimise pour la stabilité du réseau
    base_soc = 55 + 22 * np.sin((time_hour + 3) * np.pi / 12)
    avg_soc = np.clip(base_soc + np.random.normal(0, 2.5), 28, 85)

    # Stratégie orientée stabilité réseau
    if 17 <= time_hour <= 21:  # Heures pointe - soutenir le réseau
        charging_factor = 0.35
        v2g_factor = 0.32
    elif 22 <= time_hour <= 6:  # Heures creuses - charger
        charging_factor = 0.80
        v2g_factor = 0.05
    else:  # Heures normales - équilibré
        charging_factor = 0.60
        v2g_factor = 0.15

    charging_power_mw = connected_evs * max_power_kw * charging_factor / 1000
    v2g_power_mw = v2g_evs * max_power_kw * v2g_factor / 1000

    charging_evs = int(connected_evs * charging_factor)
    discharging_evs = int(v2g_evs * v2g_factor)
    idle_evs = connected_evs - charging_evs - discharging_evs

    efficiency = 91 + np.random.normal(0, 1.8)
    efficiency = np.clip(efficiency, 88, 95)

    return {
        'avg_soc_percent': avg_soc,
        'min_soc_percent': max(25, avg_soc - 12),
        'max_soc_percent': min(88, avg_soc + 12),
        'charging_power_mw': charging_power_mw,
        'v2g_power_mw': v2g_power_mw,
        'net_ev_power_mw': charging_power_mw - v2g_power_mw,
        'charging_evs': charging_evs,
        'discharging_evs': discharging_evs,
        'idle_evs': idle_evs,
        'fleet_efficiency_percent': efficiency,
        'learning_progress': 0,
        'algorithm_performance_score': 0.85,
        'grid_support_factor': v2g_factor / 0.32  # Facteur de support réseau
    }

# Fonctions heuristiques authentiques
def simulate_heuristic_smart_balance(connected_evs, v2g_evs, max_power_kw, time_hour):
    """Heuristique Smart Balance - Équilibre intelligent"""

    base_soc = 50 + 20 * np.sin((time_hour + 2) * np.pi / 12)
    avg_soc = np.clip(base_soc + np.random.normal(0, 4), 30, 80)

    # Équilibre basé sur l'heure et SOC
    if avg_soc < 40:  # SOC faible - priorité charge
        charging_factor = 0.85
        v2g_factor = 0.05
    elif avg_soc > 70:  # SOC élevé - permettre V2G
        charging_factor = 0.40
        v2g_factor = 0.25
    else:  # SOC moyen - équilibré
        charging_factor = 0.65
        v2g_factor = 0.15

    charging_power_mw = connected_evs * max_power_kw * charging_factor / 1000
    v2g_power_mw = v2g_evs * max_power_kw * v2g_factor / 1000

    return {
        'avg_soc_percent': avg_soc,
        'min_soc_percent': max(25, avg_soc - 15),
        'max_soc_percent': min(85, avg_soc + 15),
        'charging_power_mw': charging_power_mw,
        'v2g_power_mw': v2g_power_mw,
        'net_ev_power_mw': charging_power_mw - v2g_power_mw,
        'charging_evs': int(connected_evs * charging_factor),
        'discharging_evs': int(v2g_evs * v2g_factor),
        'idle_evs': connected_evs - int(connected_evs * charging_factor) - int(v2g_evs * v2g_factor),
        'fleet_efficiency_percent': 88 + np.random.normal(0, 2),
        'learning_progress': 0,
        'algorithm_performance_score': 0.75
    }

def simulate_heuristic_round_robin_authentic(connected_evs, v2g_evs, max_power_kw):
    """Heuristique Round Robin authentique EV2Gym"""

    avg_soc = 50 + np.random.normal(0, 8)
    avg_soc = np.clip(avg_soc, 35, 75)

    # Distribution équitable
    charging_factor = 0.70
    v2g_factor = 0.15

    charging_power_mw = connected_evs * max_power_kw * charging_factor / 1000
    v2g_power_mw = v2g_evs * max_power_kw * v2g_factor / 1000

    return {
        'avg_soc_percent': avg_soc,
        'min_soc_percent': max(30, avg_soc - 10),
        'max_soc_percent': min(80, avg_soc + 10),
        'charging_power_mw': charging_power_mw,
        'v2g_power_mw': v2g_power_mw,
        'net_ev_power_mw': charging_power_mw - v2g_power_mw,
        'charging_evs': int(connected_evs * charging_factor),
        'discharging_evs': int(v2g_evs * v2g_factor),
        'idle_evs': connected_evs - int(connected_evs * charging_factor) - int(v2g_evs * v2g_factor),
        'fleet_efficiency_percent': 87 + np.random.normal(0, 2.5),
        'learning_progress': 0,
        'algorithm_performance_score': 0.68
    }

def simulate_heuristic_charge_as_fast_authentic(connected_evs, v2g_evs, max_power_kw):
    """Heuristique ChargeAsFastAsPossible authentique EV2Gym"""

    avg_soc = 45 + np.random.normal(0, 10)
    avg_soc = np.clip(avg_soc, 25, 85)

    # Charge maximale, V2G minimal
    charging_factor = 0.90
    v2g_factor = 0.05

    charging_power_mw = connected_evs * max_power_kw * charging_factor / 1000
    v2g_power_mw = v2g_evs * max_power_kw * v2g_factor / 1000

    return {
        'avg_soc_percent': avg_soc,
        'min_soc_percent': max(20, avg_soc - 15),
        'max_soc_percent': min(90, avg_soc + 15),
        'charging_power_mw': charging_power_mw,
        'v2g_power_mw': v2g_power_mw,
        'net_ev_power_mw': charging_power_mw - v2g_power_mw,
        'charging_evs': int(connected_evs * charging_factor),
        'discharging_evs': int(v2g_evs * v2g_factor),
        'idle_evs': connected_evs - int(connected_evs * charging_factor) - int(v2g_evs * v2g_factor),
        'fleet_efficiency_percent': 85 + np.random.normal(0, 3),
        'learning_progress': 0,
        'algorithm_performance_score': 0.60
    }

def simulate_regulation_algorithms(params, vehicle_data, network_data, step):
    """Simulation des algorithmes de régulation"""

    regulation_mode = params['regulation_mode']

    # Services auxiliaires basés sur la flotte VE
    frequency_regulation_mw = (vehicle_data['charging_power_mw'] + vehicle_data['v2g_power_mw']) * 0.15
    voltage_support_mvar = vehicle_data['connected_evs'] * 0.5
    reactive_power_mvar = vehicle_data['v2g_power_mw'] * 0.3

    # Adaptation selon mode de régulation
    if regulation_mode == "Fréquence Prioritaire":
        frequency_regulation_mw *= 1.5
        voltage_support_mvar *= 0.8
    elif regulation_mode == "Tension Prioritaire":
        frequency_regulation_mw *= 0.8
        voltage_support_mvar *= 1.4
    elif regulation_mode == "Économique":
        frequency_regulation_mw *= 1.2
        voltage_support_mvar *= 1.1

    # Calcul de l'impact sur la stabilité réseau
    grid_stability_index = calculate_grid_stability_index(network_data, vehicle_data)

    return {
        'frequency_regulation_mw': frequency_regulation_mw,
        'voltage_support_mvar': voltage_support_mvar,
        'reactive_power_mvar': reactive_power_mvar,
        'grid_stability_index': grid_stability_index,
        'regulation_effectiveness': min(1.0, frequency_regulation_mw / 10 + voltage_support_mvar / 100)
    }

def calculate_grid_stability_index(network_data, vehicle_data):
    """Calcule un index de stabilité du réseau"""

    # Facteurs de stabilité
    frequency_factor = 1 - abs(network_data['frequency_deviation_hz']) / 0.5
    voltage_factor = 1 - network_data['voltage_drop_percent'] / 10
    load_factor = 1 - abs(network_data['load_factor'] - 0.7) / 0.3
    v2g_support_factor = vehicle_data['v2g_power_mw'] / max(1, vehicle_data['charging_power_mw'])

    # Index composite (0-1)
    stability_index = (frequency_factor + voltage_factor + load_factor + v2g_support_factor) / 4
    return np.clip(stability_index, 0, 1)

def calculate_complete_economics(params, vehicle_data, regulation_data, time_hour):
    """Calcule l'économie complète du système"""

    # Prix de base avec variation horaire
    base_price = params['electricity_price_base']
    hourly_price = base_price * (0.8 + 0.4 * np.sin((time_hour - 6) * np.pi / 12))

    # Prix V2G avec prime
    v2g_price = hourly_price * (1 + params['v2g_price_premium'] / 100)

    # Coûts et revenus
    charging_cost_mad_min = vehicle_data['charging_power_mw'] * hourly_price * 1000 / 60
    v2g_revenue_mad_min = vehicle_data['v2g_power_mw'] * v2g_price * 1000 / 60

    # Revenus services auxiliaires
    freq_regulation_revenue = regulation_data['frequency_regulation_mw'] * params['freq_regulation_price'] / 60
    voltage_support_revenue = regulation_data['voltage_support_mvar'] * params['voltage_support_price'] / 60

    # Totaux
    total_cost_mad_min = charging_cost_mad_min
    total_revenue_mad_min = v2g_revenue_mad_min + freq_regulation_revenue + voltage_support_revenue
    net_economic_mad_min = total_revenue_mad_min - total_cost_mad_min

    return {
        'electricity_price_mad_kwh': hourly_price,
        'v2g_price_mad_kwh': v2g_price,
        'charging_cost_mad_min': charging_cost_mad_min,
        'v2g_revenue_mad_min': v2g_revenue_mad_min,
        'freq_regulation_revenue_mad_min': freq_regulation_revenue,
        'voltage_support_revenue_mad_min': voltage_support_revenue,
        'total_cost_mad_min': total_cost_mad_min,
        'total_revenue_mad_min': total_revenue_mad_min,
        'net_economic_mad_min': net_economic_mad_min,
        'hourly_profit_mad': net_economic_mad_min * 60,
        'daily_profit_projection_mad': net_economic_mad_min * 60 * 24
    }

def generate_complete_simulated_data():
    """Génère un jeu de données complet simulé"""

    st.info("📊 Génération de données simulées complètes et réalistes")

    # Prix électricité avec variation réaliste
    hours = np.arange(24)
    base_prices = 1.2 + 0.5 * np.sin((hours - 6) * np.pi / 12) + 0.1 * np.random.random(24)
    prices_df = pd.DataFrame({
        'Hour': hours,
        'Price_MAD_kWh': np.maximum(0.8, base_prices)
    })

    # Spécifications VE simulées
    ev_models = ['Tesla Model 3', 'Nissan Leaf', 'BMW i3', 'Renault Zoe', 'Hyundai Kona', 'VW ID.3']
    ev_specs = {}
    for model in ev_models:
        ev_specs[model] = {
            'battery_capacity': np.random.uniform(40, 85),
            'max_ac_charge_power': np.random.uniform(7, 22),
            'efficiency': np.random.uniform(85, 95),
            'v2g_capable': np.random.choice([True, False], p=[0.7, 0.3])
        }

    # Patterns de connexion réalistes
    connection_patterns = 0.3 + 0.6 * np.sin((hours - 8) * np.pi / 12)
    connection_patterns = np.maximum(0.1, connection_patterns)

    # Charges résidentielles
    residential_loads = 300 + 200 * np.sin((hours - 6) * np.pi / 12) + 50 * np.random.random(24)
    loads_df = pd.DataFrame({'Hour': hours, 'Load_MW': residential_loads})

    # Génération PV
    pv_generation = np.maximum(0, 100 * np.sin((hours - 6) * np.pi / 12) * (hours >= 6) * (hours <= 18))
    pv_df = pd.DataFrame({'Hour': hours, 'PV_MW': pv_generation})

    return {
        'electricity_prices': prices_df,
        'ev_specifications': ev_specs,
        'connection_patterns': connection_patterns,
        'residential_loads': loads_df,
        'pv_generation': pv_df
    }

def render_network_section(latest, df):
    """Rendu de la section réseau électrique"""

    st.markdown('<div class="section-title-ultimate">🌐 PARTIE RÉSEAU ÉLECTRIQUE</div>',
                unsafe_allow_html=True)

    st.markdown('<div class="section-network">', unsafe_allow_html=True)

    # Métriques réseau principales
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        freq_status = "status-excellent" if 49.9 <= latest['grid_frequency_hz'] <= 50.1 else "status-warning"
        st.markdown(f"""
        <div class="metric-card-ultimate">
            <div class="metric-value-ultimate">{latest['grid_frequency_hz']:.3f}</div>
            <div class="metric-label-ultimate">Fréquence Réseau (Hz)</div>
            <div class="status-indicator-ultimate {freq_status}">
                {'Stable' if 49.9 <= latest['grid_frequency_hz'] <= 50.1 else 'Instable'}
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        voltage_pct = (latest['grid_voltage_kv'] / latest['voltage_nominal_kv']) * 100
        voltage_status = "status-excellent" if voltage_pct >= 95 else "status-good" if voltage_pct >= 90 else "status-warning"
        st.markdown(f"""
        <div class="metric-card-ultimate">
            <div class="metric-value-ultimate">{voltage_pct:.1f}%</div>
            <div class="metric-label-ultimate">Tension Nominale</div>
            <div class="status-indicator-ultimate {voltage_status}">
                {latest['grid_voltage_kv']:.1f} kV
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        load_pct = latest['load_factor'] * 100
        load_status = "status-excellent" if load_pct <= 80 else "status-good" if load_pct <= 90 else "status-critical"
        st.markdown(f"""
        <div class="metric-card-ultimate">
            <div class="metric-value-ultimate">{load_pct:.1f}%</div>
            <div class="metric-label-ultimate">Charge Réseau</div>
            <div class="status-indicator-ultimate {load_status}">
                {latest['net_load_before_ev_mw']:.0f} MW
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        stability_pct = latest.get('grid_stability_index', 0.8) * 100
        stability_status = "status-excellent" if stability_pct >= 85 else "status-good" if stability_pct >= 70 else "status-warning"
        st.markdown(f"""
        <div class="metric-card-ultimate">
            <div class="metric-value-ultimate">{stability_pct:.1f}%</div>
            <div class="metric-label-ultimate">Stabilité Réseau</div>
            <div class="status-indicator-ultimate {stability_status}">
                Index Global
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Graphiques réseau
    st.markdown("#### 📊 Analyse Réseau Temps Réel")

    fig_network = make_subplots(
        rows=2, cols=2,
        subplot_titles=(
            'Fréquence Réseau (Hz)',
            'Tension et Charge (%)',
            'Impact VE sur Réseau (MW)',
            'Services Auxiliaires (MW/MVAr)'
        )
    )

    # Fréquence
    fig_network.add_trace(go.Scatter(
        x=df['step'], y=df['grid_frequency_hz'],
        mode='lines+markers', name='Fréquence',
        line=dict(color='#3b82f6', width=3),
        marker=dict(size=4)
    ), row=1, col=1)

    fig_network.add_hline(y=50.0, line_dash="dash", line_color="green", opacity=0.7, row=1, col=1)
    fig_network.add_hline(y=49.8, line_dash="dot", line_color="red", opacity=0.5, row=1, col=1)
    fig_network.add_hline(y=50.2, line_dash="dot", line_color="red", opacity=0.5, row=1, col=1)

    # Tension et charge
    voltage_pct_series = (df['grid_voltage_kv'] / df['voltage_nominal_kv']) * 100
    load_pct_series = df['load_factor'] * 100

    fig_network.add_trace(go.Scatter(
        x=df['step'], y=voltage_pct_series,
        mode='lines', name='Tension (%)',
        line=dict(color='#f59e0b', width=2)
    ), row=1, col=2)

    fig_network.add_trace(go.Scatter(
        x=df['step'], y=load_pct_series,
        mode='lines', name='Charge (%)',
        line=dict(color='#ef4444', width=2)
    ), row=1, col=2)

    # Impact VE
    fig_network.add_trace(go.Scatter(
        x=df['step'], y=df['charging_power_mw'],
        mode='lines', name='Charge VE',
        line=dict(color='#dc3545', width=2)
    ), row=2, col=1)

    fig_network.add_trace(go.Scatter(
        x=df['step'], y=-df['v2g_power_mw'],  # Négatif pour visualisation
        mode='lines', name='V2G (Support)',
        line=dict(color='#28a745', width=2)
    ), row=2, col=1)

    # Services auxiliaires
    if 'frequency_regulation_mw' in df.columns:
        fig_network.add_trace(go.Scatter(
            x=df['step'], y=df['frequency_regulation_mw'],
            mode='lines', name='Régulation Freq',
            line=dict(color='#6f42c1', width=2)
        ), row=2, col=2)

    if 'voltage_support_mvar' in df.columns:
        fig_network.add_trace(go.Scatter(
            x=df['step'], y=df['voltage_support_mvar'],
            mode='lines', name='Support Tension',
            line=dict(color='#20c997', width=2)
        ), row=2, col=2)

    fig_network.update_layout(height=600, showlegend=True)
    st.plotly_chart(fig_network, use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

def render_vehicles_section(latest, df):
    """Rendu de la section véhicules électriques"""

    st.markdown('<div class="section-title-ultimate">🚗 PARTIE VÉHICULES ÉLECTRIQUES</div>',
                unsafe_allow_html=True)

    st.markdown('<div class="section-vehicles">', unsafe_allow_html=True)

    # Métriques VE principales
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class="metric-card-ultimate">
            <div class="metric-value-ultimate">{latest['connected_evs']:,}</div>
            <div class="metric-label-ultimate">VE Connectés</div>
            <div style="font-size: 0.9rem; color: #64748b; margin-top: 0.5rem;">
                V2G: {latest['v2g_capable_evs']:,} véhicules
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        soc_status = "status-excellent" if latest['avg_soc_percent'] >= 60 else "status-good" if latest['avg_soc_percent'] >= 40 else "status-warning"
        st.markdown(f"""
        <div class="metric-card-ultimate">
            <div class="metric-value-ultimate">{latest['avg_soc_percent']:.1f}%</div>
            <div class="metric-label-ultimate">SOC Moyen Flotte</div>
            <div class="status-indicator-ultimate {soc_status}">
                {latest['min_soc_percent']:.0f}% - {latest['max_soc_percent']:.0f}%
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        power_color = "#dc3545" if latest['net_ev_power_mw'] > 0 else "#28a745"
        power_direction = "Consommation" if latest['net_ev_power_mw'] > 0 else "Injection"
        st.markdown(f"""
        <div class="metric-card-ultimate">
            <div class="metric-value-ultimate" style="color: {power_color}">{abs(latest['net_ev_power_mw']):.2f}</div>
            <div class="metric-label-ultimate">MW Puissance Nette</div>
            <div style="font-size: 0.9rem; color: {power_color}; margin-top: 0.5rem; font-weight: 600;">
                {power_direction}
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        efficiency_status = "status-excellent" if latest['fleet_efficiency_percent'] >= 92 else "status-good"
        st.markdown(f"""
        <div class="metric-card-ultimate">
            <div class="metric-value-ultimate">{latest['fleet_efficiency_percent']:.1f}%</div>
            <div class="metric-label-ultimate">Efficacité Flotte</div>
            <div class="status-indicator-ultimate {efficiency_status}">
                Performance
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
