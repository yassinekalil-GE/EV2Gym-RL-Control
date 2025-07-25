#!/usr/bin/env python3
"""
⚡🚗 EXPERT EV ENERGY MANAGEMENT DASHBOARD
Advanced Electric Vehicle Fleet Energy Management System

Développé par un expert en véhicules électriques et gestion énergétique
Basé sur les standards industriels et les meilleures pratiques du secteur
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import datetime as dt
from datetime import datetime, timedelta
import json
import sys
import time
from pathlib import Path

# Configuration experte
st.set_page_config(
    page_title="⚡ Expert EV Energy Management Dashboard",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS professionnel pour experts
st.markdown("""
<style>
    .main .block-container { padding: 1rem; font-family: 'Segoe UI', sans-serif; }
    
    .expert-header {
        background: linear-gradient(135deg, #1a365d 0%, #2d3748 50%, #1a202c 100%);
        color: white; padding: 2rem; border-radius: 15px; text-align: center;
        margin-bottom: 2rem; box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }
    
    .kpi-card {
        background: white; border: 2px solid #e2e8f0; border-radius: 12px;
        padding: 1.5rem; margin: 1rem 0; box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    
    .kpi-card:hover { transform: translateY(-5px); box-shadow: 0 8px 25px rgba(0,0,0,0.15); }
    
    .kpi-value { font-size: 2.5rem; font-weight: bold; color: #2d3748; margin: 0; }
    .kpi-label { font-size: 0.9rem; color: #718096; text-transform: uppercase; letter-spacing: 1px; }
    .kpi-unit { font-size: 0.8rem; color: #a0aec0; margin-top: 0.5rem; }
    
    .status-optimal { background: #c6f6d5; color: #22543d; padding: 0.5rem 1rem; border-radius: 20px; }
    .status-good { background: #bee3f8; color: #2a4365; padding: 0.5rem 1rem; border-radius: 20px; }
    .status-warning { background: #fef5e7; color: #c05621; padding: 0.5rem 1rem; border-radius: 20px; }
    .status-critical { background: #fed7d7; color: #c53030; padding: 0.5rem 1rem; border-radius: 20px; }
    
    .section-title {
        font-size: 1.5rem; font-weight: bold; color: #2d3748; margin: 2rem 0 1rem 0;
        border-left: 4px solid #4299e1; padding-left: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# États de session pour simulation experte
if 'expert_simulation_running' not in st.session_state:
    st.session_state.expert_simulation_running = True
if 'expert_data' not in st.session_state:
    st.session_state.expert_data = []
if 'fleet_state' not in st.session_state:
    st.session_state.fleet_state = {}
if 'grid_state' not in st.session_state:
    st.session_state.grid_state = {}

def main():
    """Interface principale du dashboard expert"""
    
    # Header professionnel
    st.markdown("""
    <div class="expert-header">
        <h1>⚡ Expert EV Energy Management Dashboard</h1>
        <p>Système Avancé de Gestion Énergétique pour Flottes de Véhicules Électriques</p>
        <p><strong>Temps Réel</strong> • <strong>Standards Industriels</strong> • <strong>Optimisation IA</strong></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Interface de contrôle experte
    render_expert_controls()
    
    # Chargement et initialisation des données
    if not st.session_state.expert_data:
        initialize_expert_simulation()
    
    # Dashboard principal
    render_expert_dashboard()
    
    # Simulation temps réel
    if st.session_state.expert_simulation_running:
        execute_expert_simulation()

def render_expert_controls():
    """Contrôles experts basés sur l'expérience industrielle"""
    
    with st.sidebar:
        st.markdown("## ⚙️ CONTRÔLES EXPERTS")
        
        # Contrôle simulation
        st.markdown("### 🔄 Simulation")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("⏸️ Pause", use_container_width=True):
                st.session_state.expert_simulation_running = False
        with col2:
            if st.button("▶️ Start", use_container_width=True):
                st.session_state.expert_simulation_running = True
        
        # Configuration de la flotte (paramètres réalistes)
        st.markdown("### 🚗 Configuration Flotte")
        
        fleet_size = st.slider("Taille de la flotte", 50, 1000, 200, 25,
                              help="Nombre total de véhicules dans la flotte")
        
        # Types de véhicules réalistes
        vehicle_mix = st.selectbox("Mix véhicules", [
            "Urbain (Citadines + Compactes)",
            "Mixte (Berlines + SUV)",
            "Commercial (Utilitaires + Bus)",
            "Premium (Tesla + Luxe)"
        ])
        
        # Profils de charge réalistes
        charging_profile = st.selectbox("Profil de charge", [
            "Résidentiel (Nuit 22h-6h)",
            "Bureau (Jour 8h-17h)", 
            "Commercial (Mixte)",
            "Rapide (Autoroute)"
        ])
        
        # Infrastructure de charge
        st.markdown("### 🔌 Infrastructure")
        
        ac_stations = st.number_input("Bornes AC (7-22 kW)", 10, 200, 50, 5)
        dc_fast = st.number_input("Bornes DC Fast (50-150 kW)", 5, 50, 15, 2)
        dc_ultra = st.number_input("Bornes DC Ultra (150-350 kW)", 0, 20, 5, 1)
        
        # Paramètres réseau critiques
        st.markdown("### ⚡ Réseau Électrique")
        
        grid_capacity = st.slider("Capacité réseau (MVA)", 5, 50, 15, 1,
                                 help="Capacité totale du transformateur")
        
        voltage_level = st.selectbox("Niveau de tension", [
            "BT - 400V (Résidentiel)",
            "MT - 20kV (Commercial)", 
            "HT - 63kV (Industriel)"
        ])
        
        power_factor_target = st.slider("Facteur de puissance cible", 0.85, 1.0, 0.95, 0.01)
        
        # Tarification réaliste Maroc
        st.markdown("### 💰 Tarification (MAD)")
        
        tariff_structure = st.selectbox("Structure tarifaire", [
            "Résidentiel ONEE",
            "Professionnel ONEE",
            "Industriel ONEE",
            "Tarif Vert (Renouvelable)"
        ])
        
        # Heures de pointe Maroc (réalistes)
        peak_hours = st.multiselect("Heures de pointe", 
                                   list(range(24)), 
                                   default=[18, 19, 20, 21],
                                   help="Heures de forte demande réseau")
        
        # Algorithmes de gestion
        st.markdown("### 🤖 Algorithme de Gestion")
        
        algorithm = st.selectbox("Stratégie d'optimisation", [
            "Load Balancing (Équilibrage)",
            "Peak Shaving (Écrêtage)",
            "Valley Filling (Remplissage)",
            "Price Optimization (Prix)",
            "Grid Support (Support réseau)",
            "Renewable Integration (Renouvelable)"
        ])
        
        # V2G si applicable
        v2g_enabled = st.checkbox("V2G activé", value=False,
                                 help="Vehicle-to-Grid (nécessite véhicules compatibles)")
        
        if v2g_enabled:
            v2g_capacity = st.slider("Capacité V2G (%)", 10, 50, 25, 5,
                                   help="% de la flotte capable de V2G")
        
        # Sauvegarder configuration
        st.session_state.expert_config = {
            'fleet_size': fleet_size,
            'vehicle_mix': vehicle_mix,
            'charging_profile': charging_profile,
            'ac_stations': ac_stations,
            'dc_fast': dc_fast,
            'dc_ultra': dc_ultra,
            'grid_capacity': grid_capacity,
            'voltage_level': voltage_level,
            'power_factor_target': power_factor_target,
            'tariff_structure': tariff_structure,
            'peak_hours': peak_hours,
            'algorithm': algorithm,
            'v2g_enabled': v2g_enabled,
            'v2g_capacity': v2g_capacity if v2g_enabled else 0
        }

def load_ev2gym_vehicle_data():
    """Chargement des données réelles de véhicules EV2Gym"""

    try:
        # Chargement des spécifications V2G 2024
        with open('ev2gym/data/ev_specs_v2g_enabled2024.json', 'r', encoding='utf-8') as f:
            v2g_specs = json.load(f)

        # Chargement des spécifications générales
        try:
            with open('ev2gym/data/ev_specs.json', 'r', encoding='utf-8') as f:
                general_specs = json.load(f)
        except:
            general_specs = {}

        # Fusion et enrichissement des données
        enriched_vehicles = {}

        for model, specs in v2g_specs.items():
            enriched_vehicles[model] = {
                'model': model,
                'registrations': specs.get('number_of_registrations', 0),
                'battery_capacity': specs.get('battery_capacity', 50),
                'max_ac_power': specs.get('max_ac_charge_power', 11),
                'max_dc_power': specs.get('max_dc_charge_power', 50),
                'avg_dc_power': specs.get('avg_dc_charge_power', 40),
                'max_ac_discharge': specs.get('max_ac_discharge_power', 0),
                'max_dc_discharge': specs.get('max_dc_discharge_power', 0),
                'v2g_capable': specs.get('max_ac_discharge_power', 0) > 0,
                'efficiency_1ph': specs.get('1ph_ch_efficiency', [85] * 14),
                'efficiency_3ph': specs.get('3ph_ch_efficiency', [90] * 14),
                'ch_current': specs.get('ch_current', [6,8,10,12,14,16,18,20,22,24,26,28,30,32])
            }

        st.session_state.ev2gym_vehicles = enriched_vehicles
        return enriched_vehicles

    except Exception as e:
        st.error(f"Erreur chargement données véhicules: {e}")
        return {}

def initialize_expert_simulation():
    """Initialisation de la simulation avec données réalistes"""

    config = st.session_state.get('expert_config', {})
    fleet_size = config.get('fleet_size', 200)

    # Chargement des données EV2Gym
    if 'ev2gym_vehicles' not in st.session_state:
        load_ev2gym_vehicle_data()

    # Génération de la flotte avec caractéristiques réalistes
    fleet_data = generate_realistic_fleet_from_ev2gym(fleet_size, config.get('vehicle_mix', 'Mixte'))

    # État initial de la flotte
    st.session_state.fleet_state = {
        'vehicles': fleet_data,
        'total_capacity': sum(v['battery_capacity'] for v in fleet_data),
        'connected_count': 0,
        'charging_count': 0,
        'avg_soc': 65.0,
        'total_power': 0.0
    }

    # État initial du réseau
    st.session_state.grid_state = {
        'frequency': 50.0,
        'voltage': get_nominal_voltage(config.get('voltage_level', 'BT - 400V')),
        'power_factor': 0.95,
        'thd': 2.5,
        'load_factor': 0.6
    }

def generate_realistic_fleet(fleet_size, vehicle_mix):
    """Génération d'une flotte réaliste basée sur le marché marocain"""
    
    # Définition des véhicules disponibles au Maroc avec données réelles
    vehicle_database = {
        'Urbain': [
            {'model': 'Dacia Spring', 'battery': 27.4, 'efficiency': 13.5, 'max_ac': 7, 'max_dc': 30, 'v2g': False},
            {'model': 'Renault Twingo E-Tech', 'battery': 22, 'efficiency': 12.8, 'max_ac': 7, 'max_dc': 22, 'v2g': False},
            {'model': 'Peugeot e-208', 'battery': 50, 'efficiency': 15.8, 'max_ac': 11, 'max_dc': 100, 'v2g': False},
            {'model': 'Fiat 500e', 'battery': 42, 'efficiency': 14.9, 'max_ac': 11, 'max_dc': 85, 'v2g': False}
        ],
        'Mixte': [
            {'model': 'Tesla Model 3', 'battery': 75, 'efficiency': 15.0, 'max_ac': 11, 'max_dc': 250, 'v2g': True},
            {'model': 'BMW i3', 'battery': 42.2, 'efficiency': 13.1, 'max_ac': 11, 'max_dc': 50, 'v2g': False},
            {'model': 'Nissan Leaf', 'battery': 40, 'efficiency': 15.6, 'max_ac': 6.6, 'max_dc': 46, 'v2g': True},
            {'model': 'Hyundai Kona Electric', 'battery': 64, 'efficiency': 14.7, 'max_ac': 11, 'max_dc': 77, 'v2g': False}
        ],
        'Commercial': [
            {'model': 'Renault Kangoo E-Tech', 'battery': 45, 'efficiency': 19.5, 'max_ac': 22, 'max_dc': 80, 'v2g': False},
            {'model': 'Mercedes eVito', 'battery': 90, 'efficiency': 26.4, 'max_ac': 11, 'max_dc': 110, 'v2g': False},
            {'model': 'Iveco Daily Electric', 'battery': 105, 'efficiency': 35.2, 'max_ac': 22, 'max_dc': 80, 'v2g': False}
        ],
        'Premium': [
            {'model': 'Tesla Model S', 'battery': 100, 'efficiency': 18.1, 'max_ac': 11, 'max_dc': 250, 'v2g': True},
            {'model': 'Audi e-tron GT', 'battery': 93.4, 'efficiency': 19.6, 'max_ac': 11, 'max_dc': 270, 'v2g': False},
            {'model': 'Mercedes EQS', 'battery': 107.8, 'efficiency': 15.7, 'max_ac': 11, 'max_dc': 200, 'v2g': False}
        ]
    }
    
    # Sélection des véhicules selon le mix
    available_vehicles = vehicle_database.get(vehicle_mix.split(' ')[0], vehicle_database['Mixte'])
    
    fleet = []
    for i in range(fleet_size):
        # Sélection aléatoire d'un modèle
        vehicle_spec = np.random.choice(available_vehicles)
        
        # Génération des caractéristiques individuelles
        vehicle = {
            'id': f"EV_{i+1:03d}",
            'model': vehicle_spec['model'],
            'battery_capacity': vehicle_spec['battery'],  # kWh
            'efficiency': vehicle_spec['efficiency'],     # kWh/100km
            'max_ac_power': vehicle_spec['max_ac'],       # kW
            'max_dc_power': vehicle_spec['max_dc'],       # kW
            'v2g_capable': vehicle_spec['v2g'],
            'current_soc': np.random.uniform(20, 90),     # %
            'is_connected': np.random.choice([True, False], p=[0.3, 0.7]),
            'is_charging': False,
            'charging_power': 0.0,
            'arrival_time': None,
            'departure_time': None
        }
        
        fleet.append(vehicle)
    
    return fleet

def generate_realistic_fleet_from_ev2gym(fleet_size, vehicle_mix):
    """Génération d'une flotte réaliste basée sur les données EV2Gym"""

    ev2gym_vehicles = st.session_state.get('ev2gym_vehicles', {})

    if not ev2gym_vehicles:
        # Fallback vers l'ancienne méthode si pas de données
        return generate_realistic_fleet(fleet_size, vehicle_mix)

    # Sélection des véhicules selon le mix et les enregistrements
    available_models = list(ev2gym_vehicles.keys())

    # Pondération selon les enregistrements réels
    weights = [ev2gym_vehicles[model]['registrations'] for model in available_models]
    total_weight = sum(weights)
    probabilities = [w/total_weight for w in weights]

    fleet = []
    for i in range(fleet_size):
        # Sélection pondérée d'un modèle selon popularité réelle
        model_name = np.random.choice(available_models, p=probabilities)
        vehicle_spec = ev2gym_vehicles[model_name]

        # Génération des caractéristiques individuelles
        vehicle = {
            'id': f"EV_{i+1:03d}",
            'model': model_name,
            'battery_capacity': vehicle_spec['battery_capacity'],
            'max_ac_power': vehicle_spec['max_ac_power'],
            'max_dc_power': vehicle_spec['max_dc_power'],
            'avg_dc_power': vehicle_spec['avg_dc_power'],
            'max_ac_discharge': vehicle_spec['max_ac_discharge'],
            'max_dc_discharge': vehicle_spec['max_dc_discharge'],
            'v2g_capable': vehicle_spec['v2g_capable'],
            'efficiency_1ph': vehicle_spec['efficiency_1ph'],
            'efficiency_3ph': vehicle_spec['efficiency_3ph'],
            'registrations': vehicle_spec['registrations'],
            'current_soc': np.random.uniform(20, 90),
            'is_connected': np.random.choice([True, False], p=[0.3, 0.7]),
            'is_charging': False,
            'charging_power': 0.0,
            'discharge_power': 0.0,
            'mode': 'idle',  # idle, charging, discharging
            'arrival_time': None,
            'departure_time': None
        }

        fleet.append(vehicle)

    return fleet

def get_nominal_voltage(voltage_level):
    """Retourne la tension nominale selon le niveau"""
    voltage_map = {
        'BT - 400V (Résidentiel)': 400,
        'MT - 20kV (Commercial)': 20000,
        'HT - 63kV (Industriel)': 63000
    }
    return voltage_map.get(voltage_level, 400)

def render_expert_dashboard():
    """Dashboard principal avec expertise industrielle"""

    if not st.session_state.expert_data:
        st.info("🚀 Initialisation de la simulation experte...")
        return

    latest_data = st.session_state.expert_data[-1]
    config = st.session_state.get('expert_config', {})

    # Statut global du système
    render_system_status(latest_data, config)

    # KPI critiques pour experts
    render_critical_kpis(latest_data)

    # Section véhicules EV2Gym avec tableau V2G/G2V
    render_ev2gym_vehicles_section()

    # Analyse de la flotte
    render_fleet_analysis(latest_data)

    # Analyse réseau
    render_grid_analysis(latest_data)

    # Performance économique
    render_economic_performance(latest_data)

    # Visualisations expertes
    render_expert_visualizations()

def render_system_status(latest_data, config):
    """Statut global du système avec indicateurs critiques"""

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        # Statut de charge de la flotte
        avg_soc = latest_data.get('fleet_avg_soc', 65)
        soc_status = "Optimal" if avg_soc > 70 else "Bon" if avg_soc > 50 else "Critique"
        soc_color = "status-optimal" if avg_soc > 70 else "status-good" if avg_soc > 50 else "status-critical"

        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value">{avg_soc:.1f}%</div>
            <div class="kpi-label">SOC Moyen Flotte</div>
            <div class="kpi-unit">État de charge global</div>
            <div class="{soc_color}">{soc_status}</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        # Puissance active totale
        total_power = latest_data.get('total_charging_power', 0)
        grid_capacity = config.get('grid_capacity', 15) * 1000  # MVA to kW
        load_percent = (total_power / grid_capacity) * 100

        load_status = "Critique" if load_percent > 90 else "Élevé" if load_percent > 75 else "Normal"
        load_color = "status-critical" if load_percent > 90 else "status-warning" if load_percent > 75 else "status-good"

        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value">{total_power:.0f} kW</div>
            <div class="kpi-label">Puissance Active</div>
            <div class="kpi-unit">{load_percent:.1f}% de la capacité</div>
            <div class="{load_color}">{load_status}</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        # Efficacité énergétique
        efficiency = latest_data.get('energy_efficiency', 92)
        eff_status = "Excellent" if efficiency > 95 else "Bon" if efficiency > 90 else "Moyen"
        eff_color = "status-optimal" if efficiency > 95 else "status-good" if efficiency > 90 else "status-warning"

        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value">{efficiency:.1f}%</div>
            <div class="kpi-label">Efficacité Énergétique</div>
            <div class="kpi-unit">Rendement global système</div>
            <div class="{eff_color}">{eff_status}</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        # Coût énergétique
        energy_cost = latest_data.get('energy_cost_mad_kwh', 1.5)
        cost_trend = latest_data.get('cost_trend', 'stable')

        cost_color = "status-good" if cost_trend == 'decreasing' else "status-warning" if cost_trend == 'increasing' else "status-optimal"

        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value">{energy_cost:.2f}</div>
            <div class="kpi-label">Coût Énergétique</div>
            <div class="kpi-unit">MAD/kWh moyen</div>
            <div class="{cost_color}">Tendance {cost_trend}</div>
        </div>
        """, unsafe_allow_html=True)

def render_critical_kpis(latest_data):
    """KPI critiques pour la gestion énergétique"""

    st.markdown('<div class="section-title">⚡ Indicateurs Critiques Réseau</div>', unsafe_allow_html=True)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        # Fréquence réseau (critique pour stabilité)
        frequency = latest_data.get('grid_frequency', 50.0)
        freq_deviation = abs(frequency - 50.0)
        freq_status = "Stable" if freq_deviation < 0.1 else "Attention" if freq_deviation < 0.2 else "Critique"
        freq_color = "status-optimal" if freq_deviation < 0.1 else "status-warning" if freq_deviation < 0.2 else "status-critical"

        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value">{frequency:.3f}</div>
            <div class="kpi-label">Fréquence</div>
            <div class="kpi-unit">Hz (±{freq_deviation:.3f})</div>
            <div class="{freq_color}">{freq_status}</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        # Tension réseau
        voltage = latest_data.get('grid_voltage', 400)
        voltage_deviation = abs(voltage - 400) / 400 * 100
        volt_status = "Normal" if voltage_deviation < 5 else "Attention" if voltage_deviation < 10 else "Critique"
        volt_color = "status-optimal" if voltage_deviation < 5 else "status-warning" if voltage_deviation < 10 else "status-critical"

        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value">{voltage:.0f}</div>
            <div class="kpi-label">Tension</div>
            <div class="kpi-unit">V (±{voltage_deviation:.1f}%)</div>
            <div class="{volt_color}">{volt_status}</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        # Facteur de puissance
        power_factor = latest_data.get('power_factor', 0.95)
        pf_status = "Excellent" if power_factor > 0.95 else "Bon" if power_factor > 0.90 else "Faible"
        pf_color = "status-optimal" if power_factor > 0.95 else "status-good" if power_factor > 0.90 else "status-warning"

        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value">{power_factor:.3f}</div>
            <div class="kpi-label">Facteur Puissance</div>
            <div class="kpi-unit">cos φ</div>
            <div class="{pf_color}">{pf_status}</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        # THD (Total Harmonic Distortion)
        thd = latest_data.get('thd_percent', 3.5)
        thd_status = "Conforme" if thd < 5 else "Limite" if thd < 8 else "Non-conforme"
        thd_color = "status-optimal" if thd < 5 else "status-warning" if thd < 8 else "status-critical"

        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value">{thd:.1f}%</div>
            <div class="kpi-label">THD</div>
            <div class="kpi-unit">IEEE 519 < 5%</div>
            <div class="{thd_color}">{thd_status}</div>
        </div>
        """, unsafe_allow_html=True)

    with col5:
        # Déséquilibre de phases
        phase_imbalance = latest_data.get('phase_imbalance', 2.1)
        imb_status = "Bon" if phase_imbalance < 3 else "Attention" if phase_imbalance < 5 else "Critique"
        imb_color = "status-optimal" if phase_imbalance < 3 else "status-warning" if phase_imbalance < 5 else "status-critical"

        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value">{phase_imbalance:.1f}%</div>
            <div class="kpi-label">Déséquilibre</div>
            <div class="kpi-unit">Phases (< 3%)</div>
            <div class="{imb_color}">{imb_status}</div>
        </div>
        """, unsafe_allow_html=True)

def render_fleet_analysis(latest_data):
    """Analyse détaillée de la flotte"""

    st.markdown('<div class="section-title">🚗 Analyse Flotte Véhicules</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        # Distribution SOC de la flotte
        soc_distribution = latest_data.get('soc_distribution', {
            'critical': 5, 'low': 15, 'normal': 60, 'high': 20
        })

        fig_soc = go.Figure(data=[
            go.Bar(
                x=['Critique<20%', 'Bas 20-40%', 'Normal 40-80%', 'Élevé>80%'],
                y=[soc_distribution['critical'], soc_distribution['low'],
                   soc_distribution['normal'], soc_distribution['high']],
                marker_color=['#e53e3e', '#dd6b20', '#38a169', '#3182ce']
            )
        ])
        fig_soc.update_layout(
            title="Distribution SOC Flotte",
            xaxis_title="Niveau SOC",
            yaxis_title="Nombre de véhicules",
            height=300
        )
        st.plotly_chart(fig_soc, use_container_width=True)

    with col2:
        # Utilisation des bornes
        charging_utilization = latest_data.get('charging_utilization', {
            'AC': 75, 'DC_Fast': 45, 'DC_Ultra': 25
        })

        fig_util = go.Figure(data=[
            go.Bar(
                x=['AC 7-22kW', 'DC Fast 50-150kW', 'DC Ultra 150-350kW'],
                y=[charging_utilization['AC'], charging_utilization['DC_Fast'],
                   charging_utilization['DC_Ultra']],
                marker_color=['#4299e1', '#ed8936', '#9f7aea']
            )
        ])
        fig_util.update_layout(
            title="Utilisation Infrastructure",
            xaxis_title="Type de borne",
            yaxis_title="Taux utilisation (%)",
            height=300
        )
        st.plotly_chart(fig_util, use_container_width=True)

def render_ev2gym_vehicles_section():
    """Section dédiée aux véhicules EV2Gym avec tableau V2G/G2V"""

    st.markdown('<div class="section-title">🚗📊 Véhicules EV2Gym - États V2G/G2V</div>', unsafe_allow_html=True)

    ev2gym_vehicles = st.session_state.get('ev2gym_vehicles', {})
    fleet_state = st.session_state.get('fleet_state', {})

    if not ev2gym_vehicles:
        st.warning("⚠️ Données véhicules EV2Gym non chargées")
        return

    # Statistiques globales de la flotte
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        total_vehicles = len(ev2gym_vehicles)
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value">{total_vehicles}</div>
            <div class="kpi-label">Modèles EV2Gym</div>
            <div class="kpi-unit">Base de données</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        v2g_capable = sum(1 for v in ev2gym_vehicles.values() if v['v2g_capable'])
        v2g_percent = (v2g_capable / total_vehicles) * 100
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value">{v2g_capable}</div>
            <div class="kpi-label">Véhicules V2G</div>
            <div class="kpi-unit">{v2g_percent:.1f}% de la base</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        total_registrations = sum(v['registrations'] for v in ev2gym_vehicles.values())
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value">{total_registrations:,}</div>
            <div class="kpi-label">Enregistrements</div>
            <div class="kpi-unit">Total marché</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        avg_battery = sum(v['battery_capacity'] for v in ev2gym_vehicles.values()) / total_vehicles
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value">{avg_battery:.1f}</div>
            <div class="kpi-label">Capacité Moyenne</div>
            <div class="kpi-unit">kWh par véhicule</div>
        </div>
        """, unsafe_allow_html=True)

    # Tableau détaillé des véhicules
    st.markdown("#### 📋 Tableau Détaillé des Véhicules EV2Gym")

    # Préparation des données pour le tableau
    vehicle_data = []
    for model, specs in ev2gym_vehicles.items():
        # Calcul de l'état actuel dans la flotte
        fleet_vehicles = fleet_state.get('vehicles', [])
        model_vehicles = [v for v in fleet_vehicles if v['model'] == model]

        if model_vehicles:
            connected = sum(1 for v in model_vehicles if v['is_connected'])
            charging = sum(1 for v in model_vehicles if v['mode'] == 'charging')
            discharging = sum(1 for v in model_vehicles if v['mode'] == 'discharging')
            avg_soc = sum(v['current_soc'] for v in model_vehicles) / len(model_vehicles)
            total_power = sum(v['charging_power'] - v.get('discharge_power', 0) for v in model_vehicles)
        else:
            connected = charging = discharging = avg_soc = total_power = 0

        vehicle_data.append({
            'Modèle': model,
            'Enregistrements': f"{specs['registrations']:,}",
            'Batterie (kWh)': specs['battery_capacity'],
            'AC Max (kW)': specs['max_ac_power'],
            'DC Max (kW)': specs['max_dc_power'],
            'V2G AC (kW)': specs['max_ac_discharge'] if specs['v2g_capable'] else 0,
            'V2G DC (kW)': specs['max_dc_discharge'] if specs['v2g_capable'] else 0,
            'Capacité V2G': '✅ Oui' if specs['v2g_capable'] else '❌ Non',
            'Dans Flotte': len(model_vehicles),
            'Connectés': connected,
            'En Charge': charging,
            'En Décharge': discharging,
            'SOC Moyen (%)': f"{avg_soc:.1f}" if model_vehicles else "N/A",
            'Puissance (kW)': f"{total_power:.1f}" if model_vehicles else "0.0"
        })

    # Affichage du tableau avec style
    df_vehicles = pd.DataFrame(vehicle_data)

    # Tri par nombre d'enregistrements (popularité)
    df_vehicles['Enregistrements_num'] = [specs['registrations'] for specs in ev2gym_vehicles.values()]
    df_vehicles = df_vehicles.sort_values('Enregistrements_num', ascending=False)
    df_vehicles = df_vehicles.drop('Enregistrements_num', axis=1)

    # Affichage avec style conditionnel
    st.dataframe(
        df_vehicles,
        use_container_width=True,
        height=400,
        column_config={
            "Modèle": st.column_config.TextColumn("🚗 Modèle", width="medium"),
            "Enregistrements": st.column_config.TextColumn("📊 Enregistrements", width="small"),
            "Batterie (kWh)": st.column_config.NumberColumn("🔋 Batterie", format="%.1f kWh"),
            "AC Max (kW)": st.column_config.NumberColumn("🔌 AC Max", format="%.1f kW"),
            "DC Max (kW)": st.column_config.NumberColumn("⚡ DC Max", format="%.0f kW"),
            "V2G AC (kW)": st.column_config.NumberColumn("🔄 V2G AC", format="%.1f kW"),
            "V2G DC (kW)": st.column_config.NumberColumn("🔄 V2G DC", format="%.1f kW"),
            "Capacité V2G": st.column_config.TextColumn("🔄 V2G", width="small"),
            "Dans Flotte": st.column_config.NumberColumn("👥 Flotte", format="%d"),
            "Connectés": st.column_config.NumberColumn("🔌 Connectés", format="%d"),
            "En Charge": st.column_config.NumberColumn("⬆️ Charge", format="%d"),
            "En Décharge": st.column_config.NumberColumn("⬇️ Décharge", format="%d"),
            "SOC Moyen (%)": st.column_config.TextColumn("🔋 SOC", width="small"),
            "Puissance (kW)": st.column_config.TextColumn("⚡ Puissance", width="small")
        }
    )

    # Graphiques de répartition
    col1, col2 = st.columns(2)

    with col1:
        # Répartition V2G vs Non-V2G
        v2g_counts = {'V2G Capable': v2g_capable, 'Non V2G': total_vehicles - v2g_capable}

        fig_v2g = go.Figure(data=[
            go.Pie(
                labels=list(v2g_counts.keys()),
                values=list(v2g_counts.values()),
                marker_colors=['#22c55e', '#ef4444'],
                hole=0.4
            )
        ])
        fig_v2g.update_layout(
            title="Répartition Capacité V2G",
            height=300,
            showlegend=True
        )
        st.plotly_chart(fig_v2g, use_container_width=True)

    with col2:
        # Top 5 modèles par enregistrements
        top_models = sorted(ev2gym_vehicles.items(),
                           key=lambda x: x[1]['registrations'],
                           reverse=True)[:5]

        models = [item[0] for item in top_models]
        registrations = [item[1]['registrations'] for item in top_models]

        fig_top = go.Figure(data=[
            go.Bar(
                x=registrations,
                y=models,
                orientation='h',
                marker_color='#3b82f6'
            )
        ])
        fig_top.update_layout(
            title="Top 5 Modèles (Enregistrements)",
            xaxis_title="Nombre d'enregistrements",
            height=300
        )
        st.plotly_chart(fig_top, use_container_width=True)

def render_grid_analysis(latest_data):
    """Analyse experte du réseau électrique"""

    st.markdown('<div class="section-title">⚡ Analyse Réseau Électrique</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        # Courbe de charge journalière
        hours = list(range(24))
        base_load = [300 + 200 * np.sin((h - 6) * np.pi / 12) + 50 * np.random.random() for h in hours]
        ev_load = latest_data.get('hourly_ev_load', [50 * np.random.random() for _ in hours])

        fig_load = go.Figure()
        fig_load.add_trace(go.Scatter(
            x=hours, y=base_load, name='Charge de base',
            line=dict(color='#4299e1', width=2)
        ))
        fig_load.add_trace(go.Scatter(
            x=hours, y=[b + e for b, e in zip(base_load, ev_load)],
            name='Charge totale (avec VE)',
            line=dict(color='#e53e3e', width=2)
        ))

        fig_load.update_layout(
            title="Profil de Charge 24h",
            xaxis_title="Heure",
            yaxis_title="Puissance (kW)",
            height=350
        )
        st.plotly_chart(fig_load, use_container_width=True)

    with col2:
        # Qualité de l'énergie
        quality_metrics = latest_data.get('power_quality', {
            'voltage_stability': 98.5,
            'frequency_stability': 99.2,
            'harmonic_compliance': 96.8,
            'power_factor': 94.5
        })

        fig_quality = go.Figure(data=go.Scatterpolar(
            r=list(quality_metrics.values()),
            theta=list(quality_metrics.keys()),
            fill='toself',
            marker_color='rgba(66, 153, 225, 0.6)'
        ))

        fig_quality.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[80, 100])
            ),
            title="Qualité de l'Énergie (%)",
            height=350
        )
        st.plotly_chart(fig_quality, use_container_width=True)

def render_economic_performance(latest_data):
    """Performance économique avec tarification marocaine réaliste"""

    st.markdown('<div class="section-title">💰 Performance Économique (MAD)</div>', unsafe_allow_html=True)

    # Tarification ONEE réaliste
    current_hour = datetime.now().hour

    # Tarifs ONEE 2024 (approximatifs)
    if current_hour in [18, 19, 20, 21]:  # Heures de pointe
        tariff_mad_kwh = 1.85  # Tarif pointe
        period = "Pointe"
        color = "#e53e3e"
    elif current_hour in [22, 23, 0, 1, 2, 3, 4, 5]:  # Heures creuses
        tariff_mad_kwh = 0.95  # Tarif creux
        period = "Creuse"
        color = "#38a169"
    else:  # Heures normales
        tariff_mad_kwh = 1.35  # Tarif normal
        period = "Normale"
        color = "#3182ce"

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value" style="color: {color}">{tariff_mad_kwh:.2f}</div>
            <div class="kpi-label">Tarif Actuel</div>
            <div class="kpi-unit">MAD/kWh - Période {period}</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        # Coût énergétique journalier
        daily_consumption = latest_data.get('daily_consumption_kwh', 2500)
        daily_cost = daily_consumption * 1.35  # Tarif moyen

        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value">{daily_cost:.0f}</div>
            <div class="kpi-label">Coût Journalier</div>
            <div class="kpi-unit">MAD ({daily_consumption:.0f} kWh)</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        # Économies par optimisation
        savings_percent = latest_data.get('optimization_savings', 15.5)
        savings_mad = daily_cost * (savings_percent / 100)

        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value" style="color: #38a169">{savings_mad:.0f}</div>
            <div class="kpi-label">Économies</div>
            <div class="kpi-unit">MAD/jour ({savings_percent:.1f}%)</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        # ROI mensuel
        monthly_savings = savings_mad * 30
        infrastructure_cost = 50000  # Estimation infrastructure
        roi_months = infrastructure_cost / monthly_savings if monthly_savings > 0 else 999

        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value">{roi_months:.1f}</div>
            <div class="kpi-label">ROI</div>
            <div class="kpi-unit">Mois pour amortissement</div>
        </div>
        """, unsafe_allow_html=True)

def render_expert_visualizations():
    """Visualisations avancées pour experts"""

    st.markdown('<div class="section-title">📊 Analyses Avancées</div>', unsafe_allow_html=True)

    # Simulation de données historiques
    if len(st.session_state.expert_data) > 1:
        df = pd.DataFrame(st.session_state.expert_data)

        col1, col2 = st.columns(2)

        with col1:
            # Évolution SOC moyen
            fig_soc_trend = go.Figure()
            fig_soc_trend.add_trace(go.Scatter(
                x=df.index, y=df['fleet_avg_soc'],
                mode='lines+markers',
                name='SOC Moyen',
                line=dict(color='#4299e1', width=3)
            ))

            fig_soc_trend.update_layout(
                title="Évolution SOC Moyen Flotte",
                xaxis_title="Temps (minutes)",
                yaxis_title="SOC (%)",
                height=300
            )
            st.plotly_chart(fig_soc_trend, use_container_width=True)

        with col2:
            # Puissance vs Efficacité
            fig_power_eff = go.Figure()
            fig_power_eff.add_trace(go.Scatter(
                x=df['total_charging_power'], y=df['energy_efficiency'],
                mode='markers',
                marker=dict(
                    size=10,
                    color=df['fleet_avg_soc'],
                    colorscale='Viridis',
                    showscale=True,
                    colorbar=dict(title="SOC (%)")
                ),
                name='Efficacité vs Puissance'
            ))

            fig_power_eff.update_layout(
                title="Efficacité vs Puissance de Charge",
                xaxis_title="Puissance Totale (kW)",
                yaxis_title="Efficacité (%)",
                height=300
            )
            st.plotly_chart(fig_power_eff, use_container_width=True)

def execute_expert_simulation():
    """Moteur de simulation expert avec logique industrielle"""

    config = st.session_state.get('expert_config', {})
    fleet_state = st.session_state.fleet_state

    # Simulation basée sur l'heure actuelle et les profils réalistes
    current_time = datetime.now()
    hour = current_time.hour
    minute = current_time.minute

    # Calcul de la demande de charge selon le profil
    charging_demand = calculate_charging_demand(hour, config.get('charging_profile', 'Résidentiel'))

    # Mise à jour de l'état de la flotte
    update_fleet_state(fleet_state, charging_demand, config)

    # Calcul des métriques réseau
    grid_metrics = calculate_grid_metrics(fleet_state, config)

    # Calcul des métriques économiques
    economic_metrics = calculate_economic_metrics(fleet_state, config, hour)

    # Données complètes pour cette itération
    simulation_data = {
        'timestamp': current_time,
        'hour': hour,
        'minute': minute,
        'fleet_avg_soc': fleet_state.get('avg_soc', 65),
        'total_charging_power': fleet_state.get('total_power', 0),
        'energy_efficiency': calculate_efficiency(fleet_state),
        'connected_vehicles': fleet_state.get('connected_count', 0),
        'charging_vehicles': fleet_state.get('charging_count', 0),
        **grid_metrics,
        **economic_metrics
    }

    # Ajouter aux données historiques
    st.session_state.expert_data.append(simulation_data)

    # Limiter l'historique
    if len(st.session_state.expert_data) > 100:
        st.session_state.expert_data = st.session_state.expert_data[-100:]

    # Mise à jour automatique
    time.sleep(2)  # 2 secondes entre les mises à jour
    st.rerun()

def calculate_charging_demand(hour, charging_profile):
    """Calcul de la demande de charge selon le profil et l'heure"""

    # Profils de charge réalistes basés sur les études de mobilité
    profiles = {
        'Résidentiel (Nuit 22h-6h)': {
            'peak_hours': [22, 23, 0, 1, 2, 3, 4, 5],
            'peak_demand': 0.8,
            'base_demand': 0.2
        },
        'Bureau (Jour 8h-17h)': {
            'peak_hours': [8, 9, 10, 11, 12, 13, 14, 15, 16, 17],
            'peak_demand': 0.7,
            'base_demand': 0.1
        },
        'Commercial (Mixte)': {
            'peak_hours': [7, 8, 12, 13, 18, 19, 20],
            'peak_demand': 0.6,
            'base_demand': 0.3
        },
        'Rapide (Autoroute)': {
            'peak_hours': [10, 11, 14, 15, 16, 17, 18, 19],
            'peak_demand': 0.9,
            'base_demand': 0.4
        }
    }

    profile_data = profiles.get(charging_profile, profiles['Résidentiel (Nuit 22h-6h)'])

    if hour in profile_data['peak_hours']:
        return profile_data['peak_demand']
    else:
        return profile_data['base_demand']

def update_fleet_state(fleet_state, charging_demand, config):
    """Mise à jour de l'état de la flotte avec logique experte"""

    vehicles = fleet_state['vehicles']
    algorithm = config.get('algorithm', 'Load Balancing')

    # Réinitialiser les compteurs
    connected_count = 0
    charging_count = 0
    total_power = 0
    total_soc = 0

    # Mise à jour de chaque véhicule
    for vehicle in vehicles:
        # Probabilité de connexion selon la demande
        if not vehicle['is_connected']:
            if np.random.random() < charging_demand * 0.3:  # 30% max de connexion
                vehicle['is_connected'] = True
                vehicle['arrival_time'] = datetime.now()

        if vehicle['is_connected']:
            connected_count += 1

            # Logique de charge selon l'algorithme
            should_charge = determine_charging_decision(vehicle, algorithm, config)

            # Décision de charge ou décharge
            charge_decision = should_charge and vehicle['current_soc'] < 90
            discharge_decision = (should_discharge_v2g(vehicle, algorithm, config) and
                                vehicle['v2g_capable'] and vehicle['current_soc'] > 30)

            if charge_decision and not discharge_decision:
                # Mode charge (G2V)
                vehicle['is_charging'] = True
                vehicle['mode'] = 'charging'
                charging_count += 1

                # Puissance de charge selon le type de borne
                charging_power = get_charging_power(vehicle, config)
                vehicle['charging_power'] = charging_power
                vehicle['discharge_power'] = 0
                total_power += charging_power

                # Mise à jour SOC (simulation simplifiée)
                soc_increase = (charging_power / vehicle['battery_capacity']) * (2/60)  # 2 min
                vehicle['current_soc'] = min(90, vehicle['current_soc'] + soc_increase)

            elif discharge_decision and not charge_decision:
                # Mode décharge (V2G)
                vehicle['is_charging'] = False
                vehicle['mode'] = 'discharging'

                # Puissance de décharge V2G
                discharge_power = get_discharge_power(vehicle, config)
                vehicle['discharge_power'] = discharge_power
                vehicle['charging_power'] = 0
                total_power -= discharge_power  # Négatif car injection réseau

                # Mise à jour SOC (décharge)
                soc_decrease = (discharge_power / vehicle['battery_capacity']) * (2/60)  # 2 min
                vehicle['current_soc'] = max(20, vehicle['current_soc'] - soc_decrease)

            else:
                # Mode idle
                vehicle['is_charging'] = False
                vehicle['mode'] = 'idle'
                vehicle['charging_power'] = 0
                vehicle['discharge_power'] = 0

            # Déconnexion aléatoire
            if np.random.random() < 0.02:  # 2% chance de déconnexion
                vehicle['is_connected'] = False
                vehicle['is_charging'] = False
                vehicle['charging_power'] = 0

        total_soc += vehicle['current_soc']

    # Mise à jour des métriques globales
    fleet_state['connected_count'] = connected_count
    fleet_state['charging_count'] = charging_count
    fleet_state['total_power'] = total_power
    fleet_state['avg_soc'] = total_soc / len(vehicles)

def determine_charging_decision(vehicle, algorithm, config):
    """Décision de charge selon l'algorithme expert"""

    current_hour = datetime.now().hour
    soc = vehicle['current_soc']

    if algorithm == 'Load Balancing (Équilibrage)':
        # Équilibrage de charge - éviter les pics
        peak_hours = config.get('peak_hours', [18, 19, 20, 21])
        if current_hour in peak_hours:
            return soc < 30  # Charge seulement si critique
        else:
            return soc < 80  # Charge normale

    elif algorithm == 'Peak Shaving (Écrêtage)':
        # Écrêtage des pics - charge en heures creuses
        off_peak = [22, 23, 0, 1, 2, 3, 4, 5, 6]
        if current_hour in off_peak:
            return soc < 85  # Charge agressive en heures creuses
        else:
            return soc < 25  # Charge minimale en heures pleines

    elif algorithm == 'Valley Filling (Remplissage)':
        # Remplissage des vallées - optimise la courbe de charge
        low_demand_hours = [1, 2, 3, 4, 5, 13, 14, 15]
        if current_hour in low_demand_hours:
            return soc < 90  # Charge maximale
        else:
            return soc < 40  # Charge modérée

    elif algorithm == 'Price Optimization (Prix)':
        # Optimisation tarifaire
        cheap_hours = [22, 23, 0, 1, 2, 3, 4, 5]  # Heures creuses ONEE
        if current_hour in cheap_hours:
            return soc < 85  # Charge en tarif réduit
        else:
            return soc < 30  # Évite les tarifs élevés

    elif algorithm == 'Grid Support (Support réseau)':
        # Support réseau - V2G si disponible
        if vehicle['v2g_capable'] and config.get('v2g_enabled', False):
            peak_hours = [18, 19, 20, 21]
            if current_hour in peak_hours and soc > 60:
                return False  # Peut décharger vers le réseau
            else:
                return soc < 70  # Maintient niveau pour support
        else:
            return soc < 75

    elif algorithm == 'Renewable Integration (Renouvelable)':
        # Intégration renouvelable - charge quand production solaire
        solar_hours = [9, 10, 11, 12, 13, 14, 15, 16]
        if current_hour in solar_hours:
            return soc < 85  # Charge avec énergie verte
        else:
            return soc < 40  # Charge minimale

    else:
        # Algorithme par défaut
        return soc < 70

def should_discharge_v2g(vehicle, algorithm, config):
    """Décision de décharge V2G selon l'algorithme expert"""

    if not vehicle['v2g_capable'] or not config.get('v2g_enabled', False):
        return False

    current_hour = datetime.now().hour
    soc = vehicle['current_soc']

    if algorithm == 'Grid Support (Support réseau)':
        # Support réseau - décharge en heures de pointe
        peak_hours = config.get('peak_hours', [18, 19, 20, 21])
        if current_hour in peak_hours and soc > 60:
            return True
        return False

    elif algorithm == 'Peak Shaving (Écrêtage)':
        # Écrêtage des pics - décharge en heures pointe
        peak_hours = [18, 19, 20, 21]
        if current_hour in peak_hours and soc > 70:
            return True
        return False

    elif algorithm == 'Price Optimization (Prix)':
        # Optimisation tarifaire - décharge en tarif élevé
        expensive_hours = [18, 19, 20, 21]  # Heures pointe ONEE
        if current_hour in expensive_hours and soc > 65:
            return True
        return False

    elif algorithm == 'Renewable Integration (Renouvelable)':
        # Décharge quand pas de production solaire mais demande élevée
        evening_hours = [18, 19, 20, 21, 22]
        if current_hour in evening_hours and soc > 60:
            return True
        return False

    else:
        # Autres algorithmes - pas de V2G par défaut
        return False

def get_charging_power(vehicle, config):
    """Calcul de la puissance de charge selon l'infrastructure"""

    # Répartition des bornes selon configuration
    ac_stations = config.get('ac_stations', 50)
    dc_fast = config.get('dc_fast', 15)
    dc_ultra = config.get('dc_ultra', 5)

    total_stations = ac_stations + dc_fast + dc_ultra

    # Probabilité d'utilisation selon disponibilité
    station_prob = np.random.random()

    if station_prob < (ac_stations / total_stations):
        # Borne AC - limitée par véhicule et infrastructure
        return min(vehicle['max_ac_power'], 22)  # Max 22kW AC
    elif station_prob < ((ac_stations + dc_fast) / total_stations):
        # Borne DC Fast
        return min(vehicle['max_dc_power'], 150)  # Max 150kW DC Fast
    else:
        # Borne DC Ultra
        return min(vehicle['max_dc_power'], 350)  # Max 350kW DC Ultra

def get_discharge_power(vehicle, config):
    """Calcul de la puissance de décharge V2G selon les capacités du véhicule"""

    if not vehicle['v2g_capable']:
        return 0

    # Utilisation des données réelles EV2Gym pour V2G
    max_ac_discharge = vehicle.get('max_ac_discharge', 0)
    max_dc_discharge = vehicle.get('max_dc_discharge', 0)

    # Répartition AC/DC pour décharge (principalement AC pour V2G résidentiel)
    if max_ac_discharge > 0:
        # Décharge AC (plus courante pour V2G)
        return min(max_ac_discharge, 11)  # Limité par infrastructure résidentielle
    elif max_dc_discharge > 0:
        # Décharge DC (pour applications spéciales)
        return min(max_dc_discharge, 50)  # Limité par infrastructure
    else:
        # Pas de capacité V2G
        return 0

def calculate_grid_metrics(fleet_state, config):
    """Calcul des métriques réseau avec expertise technique"""

    total_power = fleet_state['total_power']
    grid_capacity = config.get('grid_capacity', 15) * 1000  # MVA to kW

    # Calculs réseau réalistes
    load_factor = total_power / grid_capacity

    # Fréquence - impact de la charge sur la stabilité
    frequency_deviation = -load_factor * 0.1  # Simplification
    grid_frequency = 50.0 + frequency_deviation + np.random.normal(0, 0.02)

    # Tension - chute selon la charge
    voltage_drop = load_factor * 5  # 5% max
    nominal_voltage = get_nominal_voltage(config.get('voltage_level', 'BT - 400V'))
    grid_voltage = nominal_voltage * (1 - voltage_drop / 100)

    # Facteur de puissance - dégradation avec charge VE
    base_pf = config.get('power_factor_target', 0.95)
    pf_degradation = load_factor * 0.05  # Dégradation max 5%
    power_factor = max(0.85, base_pf - pf_degradation)

    # THD - augmente avec la charge non-linéaire des VE
    base_thd = 2.0
    thd_increase = load_factor * 3.0  # Augmentation avec charge VE
    thd_percent = base_thd + thd_increase + np.random.normal(0, 0.5)

    # Déséquilibre de phases (simulation)
    phase_imbalance = 1.0 + load_factor * 2.0 + np.random.normal(0, 0.5)

    return {
        'grid_frequency': np.clip(grid_frequency, 49.5, 50.5),
        'grid_voltage': max(nominal_voltage * 0.9, grid_voltage),
        'power_factor': power_factor,
        'thd_percent': np.clip(thd_percent, 1.0, 10.0),
        'phase_imbalance': np.clip(phase_imbalance, 0.5, 8.0),
        'load_factor': load_factor
    }

def calculate_economic_metrics(fleet_state, config, hour):
    """Calculs économiques avec tarification ONEE réaliste"""

    # Tarification ONEE 2024 (approximative)
    if hour in [18, 19, 20, 21]:  # Pointe
        tariff = 1.85
        trend = 'increasing'
    elif hour in [22, 23, 0, 1, 2, 3, 4, 5]:  # Creuse
        tariff = 0.95
        trend = 'decreasing'
    else:  # Normal
        tariff = 1.35
        trend = 'stable'

    # Consommation énergétique
    power_kw = fleet_state['total_power']
    energy_2min = power_kw * (2/60)  # Énergie en 2 minutes
    cost_2min = energy_2min * tariff

    # Projection journalière
    daily_consumption = power_kw * 24  # Approximation
    daily_cost = daily_consumption * 1.35  # Tarif moyen

    # Calcul des économies par optimisation
    algorithm = config.get('algorithm', 'Load Balancing')
    optimization_savings = {
        'Load Balancing (Équilibrage)': 12.0,
        'Peak Shaving (Écrêtage)': 18.5,
        'Valley Filling (Remplissage)': 15.2,
        'Price Optimization (Prix)': 22.8,
        'Grid Support (Support réseau)': 16.7,
        'Renewable Integration (Renouvelable)': 25.3
    }.get(algorithm, 10.0)

    return {
        'energy_cost_mad_kwh': tariff,
        'cost_trend': trend,
        'daily_consumption_kwh': daily_consumption,
        'daily_cost_mad': daily_cost,
        'optimization_savings': optimization_savings,
        'current_cost_mad': cost_2min
    }

def calculate_efficiency(fleet_state):
    """Calcul de l'efficacité énergétique globale"""

    total_power = fleet_state['total_power']
    charging_count = fleet_state['charging_count']

    if charging_count == 0:
        return 95.0  # Efficacité par défaut

    # Efficacité selon la répartition de puissance
    avg_power_per_vehicle = total_power / charging_count

    # Les bornes AC sont plus efficaces que DC à haute puissance
    if avg_power_per_vehicle < 25:  # Principalement AC
        base_efficiency = 94.5
    elif avg_power_per_vehicle < 100:  # Mixte AC/DC
        base_efficiency = 92.8
    else:  # Principalement DC haute puissance
        base_efficiency = 90.5

    # Variation aléatoire réaliste
    efficiency = base_efficiency + np.random.normal(0, 1.5)
    return np.clip(efficiency, 85.0, 97.0)

if __name__ == "__main__":
    main()
