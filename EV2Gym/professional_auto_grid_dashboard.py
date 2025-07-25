#!/usr/bin/env python3
"""
🌐⚡ DASHBOARD PROFESSIONNEL GRID IMPACT - AUTO

Dashboard ultra-professionnel avec simulation automatique
Impact des VE sur le réseau électrique, services auxiliaires
Déploiement professionnel pour jury de thèse
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
    page_title="🌐⚡ Dashboard Grid Impact Auto",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Style CSS ultra-professionnel
st.markdown("""
<style>
    .main-header-grid {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 50%, #3b82f6 100%);
        color: white;
        padding: 2.5rem;
        border-radius: 15px;
        text-align: center;
        font-size: 2.8rem;
        font-weight: 700;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(30,60,114,0.3);
        border: 2px solid rgba(255,255,255,0.1);
    }
    
    .grid-indicator {
        background: linear-gradient(135deg, #3b82f6, #1d4ed8);
        color: white;
        padding: 0.8rem 1.5rem;
        border-radius: 25px;
        font-weight: 600;
        text-align: center;
        margin: 1rem 0;
        animation: pulse-grid 2s infinite;
    }
    
    @keyframes pulse-grid {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.8; transform: scale(1.02); }
    }
    
    .critical-grid-param {
        background: linear-gradient(135deg, #1e40af, #1e3a8a);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        font-weight: 600;
        border-left: 5px solid #60a5fa;
    }
    
    .metric-card-grid {
        background: linear-gradient(135deg, #ffffff, #f8fafc);
        border: 2px solid #e2e8f0;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 0.5rem 0;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card-grid::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #1e3c72, #3b82f6);
    }
    
    .metric-card-grid:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(30,60,114,0.2);
        border-color: #3b82f6;
    }
    
    .metric-value-grid {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #1e3c72, #3b82f6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0;
        line-height: 1;
    }
    
    .metric-label-grid {
        font-size: 0.9rem;
        color: #64748b;
        margin: 0.8rem 0 0 0;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .status-indicator-grid {
        display: inline-block;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 700;
        text-transform: uppercase;
        margin-top: 0.5rem;
        letter-spacing: 0.5px;
    }
    
    .status-stable { 
        background: linear-gradient(135deg, #dcfce7, #bbf7d0); 
        color: #166534; 
        border: 2px solid #bbf7d0;
    }
    .status-normal { 
        background: linear-gradient(135deg, #dbeafe, #bfdbfe); 
        color: #1e40af; 
        border: 2px solid #bfdbfe;
    }
    .status-alert { 
        background: linear-gradient(135deg, #fef3c7, #fde68a); 
        color: #92400e; 
        border: 2px solid #fde68a;
    }
    .status-critical { 
        background: linear-gradient(135deg, #fecaca, #fca5a5); 
        color: #991b1b; 
        border: 2px solid #fca5a5;
    }
    
    .realtime-pulse-grid {
        display: inline-block;
        width: 15px;
        height: 15px;
        background: linear-gradient(135deg, #3b82f6, #1d4ed8);
        border-radius: 50%;
        margin-right: 12px;
        animation: pulse-grid-dot 1.5s infinite;
        box-shadow: 0 0 20px rgba(59,130,246,0.6);
    }
    
    @keyframes pulse-grid-dot {
        0%, 100% { 
            opacity: 1; 
            transform: scale(1);
            box-shadow: 0 0 20px rgba(59,130,246,0.6);
        }
        50% { 
            opacity: 0.7; 
            transform: scale(1.2);
            box-shadow: 0 0 30px rgba(59,130,246,0.9);
        }
    }
    
    .section-title-grid {
        font-size: 1.6rem;
        font-weight: 700;
        color: #1e293b;
        margin: 2.5rem 0 1.5rem 0;
        padding: 1rem;
        background: linear-gradient(135deg, #f8fafc, #ffffff);
        border-radius: 10px;
        border-left: 5px solid #3b82f6;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    }
    
    .grid-controls {
        background: linear-gradient(135deg, #eff6ff, #f0f9ff);
        border: 2px solid #93c5fd;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Variables de session pour simulation automatique
if 'grid_simulation_active' not in st.session_state:
    st.session_state.grid_simulation_active = False
if 'grid_step' not in st.session_state:
    st.session_state.grid_step = 0
if 'grid_data' not in st.session_state:
    st.session_state.grid_data = []
if 'grid_data_loaded' not in st.session_state:
    st.session_state.grid_data_loaded = False

def load_grid_authentic_data():
    """Charge les vraies données pour analyse réseau"""
    
    data = {}
    data_path = Path("ev2gym/data")
    
    if not data_path.exists():
        st.warning("⚠️ Dossier ev2gym/data non trouvé - Utilisation données simulées")
        return generate_grid_simulated_data()
    
    try:
        # Prix électricité pour calculs services auxiliaires
        price_files = ["Netherlands_day-ahead-2015-2024.csv", "Netherlands_prices_clean.csv"]
        for price_file in price_files:
            file_path = data_path / price_file
            if file_path.exists():
                prices_df = pd.read_csv(file_path)
                if len(prices_df) > 0:
                    data['electricity_prices'] = prices_df
                    st.success(f"✅ Prix électricité: {len(prices_df):,} points")
                    break
        
        # Charges résidentielles pour charge de base
        load_files = ["residential_loads.csv", "hourly_load_profiles.csv"]
        for load_file in load_files:
            file_path = data_path / load_file
            if file_path.exists():
                loads_df = pd.read_csv(file_path)
                data['base_loads'] = loads_df
                st.success(f"✅ Charges base: {loads_df.shape}")
                break
        
        # Génération PV pour variabilité réseau
        pv_files = ["pv_netherlands.csv", "pv_hourly_profile.csv"]
        for pv_file in pv_files:
            file_path = data_path / pv_file
            if file_path.exists():
                pv_df = pd.read_csv(file_path)
                data['pv_generation'] = pv_df
                st.success(f"✅ Génération PV: {pv_df.shape}")
                break
        
        return data
        
    except Exception as e:
        st.error(f"❌ Erreur chargement données: {e}")
        return generate_grid_simulated_data()

def generate_grid_simulated_data():
    """Génère des données simulées pour le réseau"""
    
    st.info("📊 Génération de données réseau simulées")
    
    # Charge de base simulée (profil journalier réaliste)
    hours = np.arange(24)
    base_load = 400 + 200 * np.sin((hours - 6) * np.pi / 12) + 50 * np.random.random(24)
    base_load = np.maximum(200, base_load)
    
    # Prix électricité avec variation
    prices = 1.2 + 0.4 * np.sin((hours - 6) * np.pi / 12) + 0.1 * np.random.random(24)
    
    # Génération PV simulée
    pv_gen = np.maximum(0, 100 * np.sin((hours - 6) * np.pi / 12) * (hours >= 6) * (hours <= 18))
    
    return {
        'base_loads': pd.DataFrame({'Hour': hours, 'Load_MW': base_load}),
        'electricity_prices': pd.DataFrame({'Hour': hours, 'Price_MAD_kWh': prices}),
        'pv_generation': pd.DataFrame({'Hour': hours, 'PV_MW': pv_gen})
    }

def main():
    """Interface principale ultra-professionnelle"""
    
    # En-tête ultra-professionnel
    st.markdown("""
    <div class="main-header-grid">
        <span class="realtime-pulse-grid"></span>
        DASHBOARD GRID IMPACT AUTO
        <br><span style="font-size: 1.2rem; font-weight: 400;">
        Impact Réseau • Services Auxiliaires • Simulation Automatique
        </span>
    </div>
    """, unsafe_allow_html=True)
    
    # Chargement des données authentiques
    if not st.session_state.grid_data_loaded:
        with st.spinner("🔄 Chargement des données réseau authentiques..."):
            st.session_state.grid_authentic_data = load_grid_authentic_data()
            st.session_state.grid_data_loaded = True
    
    # Sidebar avec paramètres critiques
    render_grid_critical_controls()
    
    # Interface principale
    render_grid_professional_interface()
    
    # Simulation automatique
    if st.session_state.grid_simulation_active:
        run_grid_automatic_simulation()

def render_grid_critical_controls():
    """Sidebar avec paramètres critiques réseau"""

    with st.sidebar:
        st.markdown("## ⚙️ PARAMÈTRES RÉSEAU CRITIQUES")

        # Indicateur simulation automatique
        if st.session_state.grid_simulation_active:
            st.markdown("""
            <div class="grid-indicator">
                🌐 SIMULATION RÉSEAU ACTIVE
            </div>
            """, unsafe_allow_html=True)

        # Section Réseau Électrique (Critique)
        st.markdown('<div class="critical-grid-param">🌐 RÉSEAU ÉLECTRIQUE CRITIQUE</div>',
                    unsafe_allow_html=True)

        grid_capacity_mw = st.slider("Capacité Réseau (MW)", 200, 2000, 800, 100,
                                    help="Capacité totale du réseau électrique")

        nominal_voltage_kv = st.selectbox("Tension Nominale (kV)", [22, 60, 225, 400],
                                         index=0, help="Niveau de tension du réseau")

        grid_inertia = st.slider("Inertie Réseau (s)", 3, 20, 10, 1,
                                help="Inertie du réseau - Impact sur stabilité fréquence")

        frequency_tolerance = st.slider("Tolérance Fréquence (±Hz)", 0.1, 0.5, 0.2, 0.05,
                                       help="Tolérance autour de 50Hz")

        # Section Flotte VE Impact (Critique)
        st.markdown('<div class="critical-grid-param">🚗 FLOTTE VE IMPACT</div>',
                    unsafe_allow_html=True)

        n_evs_grid = st.slider("Nombre VE Réseau", 100, 5000, 1500, 100,
                              help="Nombre de VE impactant le réseau")

        ev_penetration = st.slider("Pénétration VE (%)", 10, 80, 40, 5,
                                  help="Pourcentage de pénétration des VE")

        max_charging_power = st.slider("Puissance Charge Max (MW)", 5, 100, 25, 5,
                                      help="Puissance de charge maximale totale")

        # Section Services Auxiliaires (Critique)
        st.markdown('<div class="critical-grid-param">⚡ SERVICES AUXILIAIRES</div>',
                    unsafe_allow_html=True)

        reactive_power_mode = st.selectbox(
            "Mode Puissance Réactive",
            ["Automatique", "Capacitif", "Inductif", "Neutre"],
            help="Mode de gestion de la puissance réactive"
        )

        power_factor_target = st.slider("Facteur Puissance Cible", 0.85, 1.0, 0.95, 0.01,
                                       help="Facteur de puissance cible du réseau")

        voltage_regulation = st.checkbox("Régulation Tension Active", value=True,
                                        help="Active la régulation de tension par les VE")

        # Section Algorithme Réseau (Critique)
        st.markdown('<div class="critical-grid-param">🤖 ALGORITHME RÉSEAU</div>',
                    unsafe_allow_html=True)

        grid_algorithm = st.selectbox(
            "Algorithme Contrôle Réseau",
            [
                "RL_GridStabilizer",
                "MPC_GridOptimal",
                "Heuristic_GridBalance",
                "Advanced_GridControl"
            ],
            help="Algorithme de contrôle pour stabilité réseau"
        )

        # Section Économie Services (Critique)
        st.markdown('<div class="critical-grid-param">💰 ÉCONOMIE SERVICES MAD</div>',
                    unsafe_allow_html=True)

        freq_regulation_price = st.slider("Prix Régulation Freq (MAD/MW)", 50, 500, 200, 25,
                                         help="Prix des services de régulation fréquence")

        voltage_support_price = st.slider("Prix Support Tension (MAD/MVAr)", 30, 300, 120, 15,
                                         help="Prix des services de support tension")

        peak_shaving_price = st.slider("Prix Écrêtage Pointes (MAD/MW)", 100, 1000, 400, 50,
                                      help="Prix de l'écrêtage des pointes")

        # Section Simulation Réseau (Critique)
        st.markdown('<div class="critical-grid-param">⏱️ SIMULATION RÉSEAU</div>',
                    unsafe_allow_html=True)

        grid_auto_speed = st.slider("Vitesse Simulation (s)", 0.2, 2.0, 0.5, 0.1,
                                   help="Vitesse de la simulation réseau")

        grid_max_history = st.slider("Historique Réseau", 100, 400, 200, 25,
                                    help="Points d'historique à conserver")

        # Contrôles simulation
        st.markdown("### 🎮 CONTRÔLES RÉSEAU")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("🌐 GRID START", type="primary", use_container_width=True):
                st.session_state.grid_simulation_active = True
                st.session_state.grid_step = 0
                st.session_state.grid_data = []
                st.balloons()
                st.success("🌐 Simulation réseau démarrée!")

        with col2:
            if st.button("⏹️ STOP", use_container_width=True):
                st.session_state.grid_simulation_active = False
                st.info("⏹️ Simulation réseau arrêtée")

        if st.button("🔄 RESET RÉSEAU", use_container_width=True):
            st.session_state.grid_simulation_active = False
            st.session_state.grid_step = 0
            st.session_state.grid_data = []
            st.session_state.grid_data_loaded = False
            st.info("🔄 Reset réseau effectué")

        # Sauvegarde paramètres critiques réseau
        st.session_state.grid_critical_params = {
            'grid_capacity_mw': grid_capacity_mw,
            'nominal_voltage_kv': nominal_voltage_kv,
            'grid_inertia': grid_inertia,
            'frequency_tolerance': frequency_tolerance,
            'n_evs_grid': n_evs_grid,
            'ev_penetration': ev_penetration,
            'max_charging_power': max_charging_power,
            'reactive_power_mode': reactive_power_mode,
            'power_factor_target': power_factor_target,
            'voltage_regulation': voltage_regulation,
            'grid_algorithm': grid_algorithm,
            'freq_regulation_price': freq_regulation_price,
            'voltage_support_price': voltage_support_price,
            'peak_shaving_price': peak_shaving_price,
            'grid_auto_speed': grid_auto_speed,
            'grid_max_history': grid_max_history
        }

def render_grid_professional_interface():
    """Interface principale réseau ultra-professionnelle"""

    # Status simulation réseau
    if st.session_state.grid_simulation_active:
        status_text = "🟢 SIMULATION RÉSEAU ACTIVE"
        status_color = "#3b82f6"
        pulse_class = "realtime-pulse-grid"
    else:
        status_text = "🔴 SIMULATION RÉSEAU INACTIVE"
        status_color = "#ef4444"
        pulse_class = ""

    params = st.session_state.get('grid_critical_params', {})

    st.markdown(f"""
    <div style="text-align: center; margin: 2rem 0; padding: 1.5rem;
                background: linear-gradient(135deg, #f8fafc, #ffffff);
                border-radius: 15px; border: 2px solid #e2e8f0;
                box-shadow: 0 8px 25px rgba(0,0,0,0.08);">
        <span class="{pulse_class}"></span>
        <span style="font-size: 1.4rem; font-weight: 700; color: {status_color};">
            {status_text}
        </span>
        <div style="margin-top: 1rem; color: #64748b; font-size: 1rem;">
            <strong>Étape:</strong> {st.session_state.grid_step:,} |
            <strong>Capacité:</strong> {params.get('grid_capacity_mw', 0):,} MW |
            <strong>VE:</strong> {params.get('n_evs_grid', 0):,} |
            <strong>Tension:</strong> {params.get('nominal_voltage_kv', 22)} kV
        </div>
    </div>
    """, unsafe_allow_html=True)

    if not st.session_state.grid_data:
        st.info("🌐 Démarrez la simulation réseau pour voir l'impact des VE en temps réel")
        return

    latest = st.session_state.grid_data[-1]
    df = pd.DataFrame(st.session_state.grid_data)

    # Métriques réseau ultra-professionnelles
    render_grid_professional_metrics(latest)

    # Graphiques réseau ultra-avancés
    render_grid_advanced_charts(df)

def run_grid_automatic_simulation():
    """Exécute la simulation automatique réseau"""

    if 'grid_critical_params' not in st.session_state:
        st.error("❌ Paramètres réseau critiques non définis")
        return

    params = st.session_state.grid_critical_params
    authentic_data = st.session_state.get('grid_authentic_data', {})

    # Générer nouvelle donnée réseau
    new_data = simulate_grid_with_authentic_models(
        params=params,
        step=st.session_state.grid_step,
        authentic_data=authentic_data
    )

    # Ajouter aux données
    st.session_state.grid_data.append(new_data)
    st.session_state.grid_step += 1

    # Limiter historique
    max_history = params.get('grid_max_history', 200)
    if len(st.session_state.grid_data) > max_history:
        st.session_state.grid_data = st.session_state.grid_data[-max_history:]

    # Auto-refresh
    time.sleep(params.get('grid_auto_speed', 0.5))
    st.rerun()

def simulate_grid_with_authentic_models(params, step, authentic_data):
    """Simulation réseau avec modèles authentiques"""

    # Seed pour reproductibilité
    seed_value = (step * 98765) % (2**31 - 1)
    np.random.seed(seed_value)

    # Paramètres temporels
    time_hour = step % 24
    day_of_week = (step // 24) % 7

    # Charge de base du réseau
    base_load_mw = calculate_authentic_base_load(time_hour, day_of_week, params, authentic_data)

    # Génération PV si disponible
    pv_generation_mw = calculate_authentic_pv_generation(time_hour, authentic_data)

    # Impact des VE sur le réseau
    ev_impact = calculate_ev_grid_impact(params, time_hour, day_of_week, step)

    # Charge nette du réseau
    net_load_mw = base_load_mw + ev_impact['net_ev_load_mw'] - pv_generation_mw

    # Calculs de stabilité réseau
    grid_stability = calculate_grid_stability(net_load_mw, params, ev_impact)

    # Services auxiliaires fournis par les VE
    auxiliary_services = calculate_auxiliary_services(ev_impact, params, time_hour)

    # Calculs économiques services
    economic_services = calculate_services_economics(auxiliary_services, params)

    return {
        'timestamp': datetime.now(),
        'step': step,
        'time_hour': time_hour,
        'day_of_week': day_of_week,
        'algorithm': params['grid_algorithm'],

        # Charge réseau
        'base_load_mw': base_load_mw,
        'pv_generation_mw': pv_generation_mw,
        'ev_load_mw': ev_impact['charging_power_mw'],
        'ev_v2g_mw': ev_impact['v2g_power_mw'],
        'net_ev_load_mw': ev_impact['net_ev_load_mw'],
        'net_load_mw': net_load_mw,
        'load_factor': net_load_mw / params['grid_capacity_mw'],

        # Stabilité réseau
        'grid_frequency_hz': grid_stability['frequency'],
        'grid_voltage_kv': grid_stability['voltage'],
        'voltage_deviation_percent': grid_stability['voltage_deviation'],
        'power_factor': grid_stability['power_factor'],
        'grid_stability_index': grid_stability['stability_index'],

        # VE connectés
        'connected_evs': ev_impact['connected_evs'],
        'charging_evs': ev_impact['charging_evs'],
        'v2g_evs': ev_impact['v2g_evs'],

        # Services auxiliaires
        'frequency_regulation_mw': auxiliary_services['frequency_regulation'],
        'voltage_support_mvar': auxiliary_services['voltage_support'],
        'reactive_power_mvar': auxiliary_services['reactive_power'],
        'peak_shaving_mw': auxiliary_services['peak_shaving'],
        'grid_support_score': auxiliary_services['support_score'],

        # Économie services MAD
        'freq_regulation_revenue_mad': economic_services['freq_regulation_revenue'],
        'voltage_support_revenue_mad': economic_services['voltage_support_revenue'],
        'peak_shaving_revenue_mad': economic_services['peak_shaving_revenue'],
        'total_services_revenue_mad': economic_services['total_revenue'],
        'hourly_services_revenue_mad': economic_services['total_revenue'] * 60
    }

def calculate_authentic_base_load(time_hour, day_of_week, params, authentic_data):
    """Calcule la charge de base authentique"""

    if 'base_loads' in authentic_data:
        try:
            loads_df = authentic_data['base_loads']
            if 'Hour' in loads_df.columns:
                load_row = loads_df[loads_df['Hour'] == time_hour]
                if not load_row.empty:
                    base_load = load_row['Load_MW'].iloc[0]
                    # Échelle selon capacité réseau
                    scale_factor = params['grid_capacity_mw'] / 800  # Référence 800MW
                    return base_load * scale_factor
        except:
            pass

    # Charge simulée réaliste
    capacity = params['grid_capacity_mw']

    if day_of_week < 5:  # Jour de semaine
        if 7 <= time_hour <= 9 or 17 <= time_hour <= 21:  # Pointes
            base_factor = 0.85
        elif 22 <= time_hour <= 6:  # Heures creuses
            base_factor = 0.45
        else:  # Heures normales
            base_factor = 0.65
    else:  # Weekend
        base_factor = 0.55 + 0.2 * np.sin((time_hour - 10) * np.pi / 12)

    return capacity * base_factor * (0.95 + 0.1 * np.random.random())

def calculate_authentic_pv_generation(time_hour, authentic_data):
    """Calcule la génération PV authentique"""

    if 'pv_generation' in authentic_data:
        try:
            pv_df = authentic_data['pv_generation']
            if 'Hour' in pv_df.columns:
                pv_row = pv_df[pv_df['Hour'] == time_hour]
                if not pv_row.empty:
                    return max(0, pv_row['PV_MW'].iloc[0])
        except:
            pass

    # Génération PV simulée
    if 6 <= time_hour <= 18:  # Heures de jour
        solar_factor = np.sin((time_hour - 6) * np.pi / 12)
        return max(0, 50 * solar_factor * (0.8 + 0.4 * np.random.random()))
    else:
        return 0

def calculate_ev_grid_impact(params, time_hour, day_of_week, step):
    """Calcule l'impact des VE sur le réseau"""

    n_evs = params['n_evs_grid']
    penetration = params['ev_penetration'] / 100
    max_power = params['max_charging_power']

    # Taux de connexion réaliste
    if day_of_week < 5:  # Semaine
        if 7 <= time_hour <= 9 or 17 <= time_hour <= 20:
            connection_rate = 0.6 + 0.3 * np.random.random()
        elif 21 <= time_hour <= 7:
            connection_rate = 0.8 + 0.15 * np.random.random()
        else:
            connection_rate = 0.5 + 0.3 * np.random.random()
    else:  # Weekend
        connection_rate = 0.55 + 0.3 * np.random.random()

    connected_evs = int(n_evs * penetration * connection_rate)

    # Simulation selon algorithme
    algorithm = params['grid_algorithm']

    if "RL_GridStabilizer" in algorithm:
        # RL optimisé pour stabilité réseau
        learning_factor = min(1.0, step / 250)
        charging_factor = 0.6 + 0.2 * learning_factor
        v2g_factor = 0.15 + 0.1 * learning_factor
    elif "MPC_GridOptimal" in algorithm:
        # MPC optimisé pour réseau
        charging_factor = 0.7
        v2g_factor = 0.2
    elif "Advanced_GridControl" in algorithm:
        # Contrôle avancé adaptatif
        charging_factor = 0.65
        v2g_factor = 0.18
    else:  # Heuristic_GridBalance
        charging_factor = 0.6
        v2g_factor = 0.12

    charging_power_mw = connected_evs * max_power * charging_factor / connected_evs if connected_evs > 0 else 0
    v2g_power_mw = connected_evs * max_power * v2g_factor / connected_evs if connected_evs > 0 else 0

    charging_evs = int(connected_evs * charging_factor)
    v2g_evs = int(connected_evs * v2g_factor)

    return {
        'connected_evs': connected_evs,
        'charging_evs': charging_evs,
        'v2g_evs': v2g_evs,
        'charging_power_mw': charging_power_mw,
        'v2g_power_mw': v2g_power_mw,
        'net_ev_load_mw': charging_power_mw - v2g_power_mw
    }

if __name__ == "__main__":
    main()
