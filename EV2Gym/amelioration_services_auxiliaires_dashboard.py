#!/usr/bin/env python3
"""
🚗⚡🌐 AMÉLIORATION DES SERVICES AUXILIAIRES VIA RL ET CONTRÔLE AVANCÉ

Dashboard interactif et intelligent en temps réel pour l'optimisation des services auxiliaires
des véhicules électriques via apprentissage par renforcement et contrôle avancé.

Objectifs:
- Suivre le comportement dynamique des VE connectés
- Visualiser l'impact sur le réseau électrique  
- Évaluer les performances des algorithmes de décision
- Réagir à différents scénarios de réseau
- Fournir des KPI réseau et économiques pertinents
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

# Configuration de la page
st.set_page_config(
    page_title="🚗⚡ Amélioration des Services Auxiliaires via RL et Contrôle Avancé",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS professionnel pour le dashboard
st.markdown("""
<style>
    /* Import des polices professionnelles */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    
    /* Styles globaux */
    .main .block-container {
        font-family: 'Inter', sans-serif;
        max-width: 100%;
        padding: 1rem;
    }
    
    /* Header principal */
    .main-header {
        background: linear-gradient(135deg, #1e40af 0%, #3b82f6 30%, #06b6d4 70%, #10b981 100%);
        color: white;
        padding: 3rem 2rem;
        border-radius: 25px;
        text-align: center;
        font-size: 3rem;
        font-weight: 900;
        margin-bottom: 2rem;
        box-shadow: 0 25px 60px rgba(30,64,175,0.4);
        border: 3px solid rgba(255,255,255,0.2);
        position: relative;
        overflow: hidden;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(255,255,255,0.15), transparent);
        animation: shine 4s infinite;
    }
    
    @keyframes shine {
        0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
        100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
    }
    
    /* Indicateur de simulation temps réel */
    .realtime-indicator {
        background: linear-gradient(135deg, #10b981, #059669, #047857);
        color: white;
        padding: 1.5rem 3rem;
        border-radius: 40px;
        font-weight: 800;
        text-align: center;
        margin: 2rem 0;
        animation: pulse-realtime 2s infinite;
        box-shadow: 0 15px 40px rgba(16,185,129,0.4);
        font-size: 1.2rem;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    
    @keyframes pulse-realtime {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.9; transform: scale(1.02); }
    }
    
    /* Sections KPI */
    .kpi-section-ve {
        background: linear-gradient(135deg, #f0fdf4, #dcfce7, #bbf7d0);
        border: 4px solid #22c55e;
        border-radius: 25px;
        padding: 3rem;
        margin: 3rem 0;
        box-shadow: 0 20px 50px rgba(34,197,94,0.25);
    }
    
    .kpi-section-reseau {
        background: linear-gradient(135deg, #eff6ff, #dbeafe, #bfdbfe);
        border: 4px solid #3b82f6;
        border-radius: 25px;
        padding: 3rem;
        margin: 3rem 0;
        box-shadow: 0 20px 50px rgba(59,130,246,0.25);
    }
    
    .kpi-section-economique {
        background: linear-gradient(135deg, #fefce8, #fef3c7, #fde68a);
        border: 4px solid #f59e0b;
        border-radius: 25px;
        padding: 3rem;
        margin: 3rem 0;
        box-shadow: 0 20px 50px rgba(245,158,11,0.25);
    }
    
    /* Cartes métriques */
    .metric-card {
        background: linear-gradient(135deg, #ffffff, #f8fafc, #f1f5f9);
        border: 3px solid #e2e8f0;
        border-radius: 20px;
        padding: 2.5rem;
        margin: 1.5rem 0;
        box-shadow: 0 15px 40px rgba(0,0,0,0.15);
        transition: all 0.4s ease;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 8px;
        background: linear-gradient(90deg, #1e40af, #3b82f6, #06b6d4, #10b981);
    }
    
    .metric-card:hover {
        transform: translateY(-12px);
        box-shadow: 0 30px 60px rgba(30,64,175,0.3);
        border-color: #3b82f6;
    }
    
    .metric-value {
        font-size: 4rem;
        font-weight: 900;
        background: linear-gradient(135deg, #1e40af, #3b82f6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0;
        line-height: 1;
        text-align: center;
    }
    
    .metric-label {
        font-size: 1.2rem;
        color: #64748b;
        margin: 1.5rem 0 0 0;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 2px;
        text-align: center;
    }
    
    .metric-unit {
        font-size: 1rem;
        color: #94a3b8;
        font-weight: 600;
        margin-top: 0.8rem;
        text-align: center;
    }
    
    /* Indicateurs de statut */
    .status-indicator {
        display: inline-block;
        padding: 0.8rem 2rem;
        border-radius: 35px;
        font-size: 1rem;
        font-weight: 800;
        text-transform: uppercase;
        margin-top: 1.5rem;
        letter-spacing: 1.5px;
        text-align: center;
        width: 100%;
    }
    
    .status-excellent { 
        background: linear-gradient(135deg, #d1fae5, #a7f3d0); 
        color: #065f46; 
        border: 3px solid #a7f3d0;
    }
    .status-good { 
        background: linear-gradient(135deg, #dbeafe, #bfdbfe); 
        color: #1e40af; 
        border: 3px solid #bfdbfe;
    }
    .status-warning { 
        background: linear-gradient(135deg, #fef3c7, #fde68a); 
        color: #92400e; 
        border: 3px solid #fde68a;
    }
    .status-critical { 
        background: linear-gradient(135deg, #fecaca, #fca5a5); 
        color: #991b1b; 
        border: 3px solid #fca5a5;
    }
    
    /* Pulse temps réel */
    .realtime-pulse {
        display: inline-block;
        width: 25px;
        height: 25px;
        background: linear-gradient(135deg, #10b981, #059669);
        border-radius: 50%;
        margin-right: 20px;
        animation: pulse 1.5s infinite;
        box-shadow: 0 0 35px rgba(16,185,129,0.8);
    }
    
    @keyframes pulse {
        0%, 100% { 
            opacity: 1; 
            transform: scale(1);
            box-shadow: 0 0 35px rgba(16,185,129,0.8);
        }
        50% { 
            opacity: 0.8; 
            transform: scale(1.5);
            box-shadow: 0 0 50px rgba(16,185,129,1);
        }
    }
    
    /* Titres de sections */
    .section-title {
        font-size: 2.5rem;
        font-weight: 900;
        color: #1e293b;
        margin: 4rem 0 3rem 0;
        padding: 2.5rem;
        background: linear-gradient(135deg, #f8fafc, #ffffff);
        border-radius: 25px;
        border-left: 15px solid #3b82f6;
        box-shadow: 0 15px 40px rgba(0,0,0,0.12);
        text-transform: uppercase;
        letter-spacing: 3px;
        text-align: center;
    }
    
    /* Contrôles de paramètres */
    .parameter-section {
        background: linear-gradient(135deg, #f8fafc, #f1f5f9);
        border: 3px solid #cbd5e1;
        border-radius: 20px;
        padding: 2.5rem;
        margin: 2rem 0;
    }
    
    .parameter-title {
        font-size: 1.4rem;
        font-weight: 800;
        color: #475569;
        margin-bottom: 1.5rem;
        text-transform: uppercase;
        letter-spacing: 1.5px;
    }
    
    /* Responsive design */
    @media (max-width: 1200px) {
        .main-header {
            font-size: 2.5rem;
            padding: 2rem 1rem;
        }
        .metric-value {
            font-size: 3rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Initialisation des états de session
if 'simulation_running' not in st.session_state:
    st.session_state.simulation_running = True
if 'simulation_step' not in st.session_state:
    st.session_state.simulation_step = 0
if 'simulation_data' not in st.session_state:
    st.session_state.simulation_data = []
if 'ev2gym_data_loaded' not in st.session_state:
    st.session_state.ev2gym_data_loaded = False
if 'individual_ev_data' not in st.session_state:
    st.session_state.individual_ev_data = {}

def main():
    """Fonction principale du dashboard"""
    
    # Header principal
    st.markdown("""
    <div class="main-header">
        <span class="realtime-pulse"></span>
        Amélioration des Services Auxiliaires
        <br><span style="font-size: 1.6rem; font-weight: 600; letter-spacing: 2px;">
        Via RL et Contrôle Avancé • Dashboard Temps Réel
        </span>
    </div>
    """, unsafe_allow_html=True)
    
    # Indicateur de simulation temps réel
    current_time = datetime.now().strftime("%H:%M:%S")
    st.markdown(f"""
    <div class="realtime-indicator">
        🔄 Simulation Temps Réel Active - {current_time}
        <br><span style="font-size: 1rem; font-weight: 600;">
        Optimisation Continue des Services Auxiliaires via RL et MPC
        </span>
    </div>
    """, unsafe_allow_html=True)
    
    # Chargement des données EV2Gym
    if not st.session_state.ev2gym_data_loaded:
        load_ev2gym_data()
    
    # Interface de contrôle
    render_control_interface()
    
    # Interface principale du dashboard
    render_main_dashboard()
    
    # Exécution de la simulation temps réel
    if st.session_state.simulation_running:
        execute_realtime_simulation()

def load_ev2gym_data():
    """Chargement des données EV2Gym authentiques"""

    st.session_state.ev2gym_data = {}
    data_path = Path("ev2gym/data")

    with st.spinner("🔄 Chargement des données EV2Gym..."):
        try:
            # Chargement des spécifications VE
            ev_specs_file = data_path / "ev_specs_v2g_enabled2024.json"
            if ev_specs_file.exists():
                with open(ev_specs_file, 'r', encoding='utf-8') as f:
                    ev_specs = json.load(f)
                st.session_state.ev2gym_data['ev_specifications'] = ev_specs
                st.success(f"✅ Spécifications VE: {len(ev_specs)} modèles chargés")

            # Chargement des prix électricité
            price_files = ["Netherlands_day-ahead-2015-2024.csv", "Netherlands_prices_clean.csv"]
            for price_file in price_files:
                file_path = data_path / price_file
                if file_path.exists():
                    prices_df = pd.read_csv(file_path)
                    st.session_state.ev2gym_data['electricity_prices'] = prices_df
                    st.success(f"✅ Prix électricité: {len(prices_df):,} points de données")
                    break

            # Chargement des profils de charge
            load_files = ["residential_loads.csv", "hourly_load_profiles.csv"]
            for load_file in load_files:
                file_path = data_path / load_file
                if file_path.exists():
                    loads_df = pd.read_csv(file_path)
                    st.session_state.ev2gym_data['load_profiles'] = loads_df
                    st.success(f"✅ Profils de charge: {loads_df.shape}")
                    break

            # Chargement des données PV
            pv_files = ["pv_netherlands.csv", "pv_hourly_profile.csv"]
            for pv_file in pv_files:
                file_path = data_path / pv_file
                if file_path.exists():
                    pv_df = pd.read_csv(file_path)
                    st.session_state.ev2gym_data['pv_generation'] = pv_df
                    st.success(f"✅ Génération PV: {pv_df.shape}")
                    break

            st.session_state.ev2gym_data_loaded = True
            st.success("🎉 Toutes les données EV2Gym chargées avec succès!")

        except Exception as e:
            st.warning(f"⚠️ Certaines données manquantes: {e}")
            st.info("📊 Utilisation de données synthétiques réalistes")
            generate_synthetic_data()
            st.session_state.ev2gym_data_loaded = True

def generate_synthetic_data():
    """Génération de données synthétiques réalistes"""

    # Spécifications VE synthétiques basées sur modèles réels 2024
    ev_specs = {
        'Tesla Model 3': {'battery_capacity': 75, 'max_ac_power': 11, 'max_dc_power': 250, 'efficiency': 92, 'v2g_capable': True},
        'Nissan Leaf': {'battery_capacity': 40, 'max_ac_power': 6.6, 'max_dc_power': 50, 'efficiency': 89, 'v2g_capable': True},
        'BMW i3': {'battery_capacity': 42, 'max_ac_power': 11, 'max_dc_power': 50, 'efficiency': 88, 'v2g_capable': False},
        'Renault Zoe': {'battery_capacity': 52, 'max_ac_power': 22, 'max_dc_power': 50, 'efficiency': 90, 'v2g_capable': True},
        'Hyundai Kona': {'battery_capacity': 64, 'max_ac_power': 11, 'max_dc_power': 77, 'efficiency': 91, 'v2g_capable': True},
        'VW ID.3': {'battery_capacity': 58, 'max_ac_power': 11, 'max_dc_power': 125, 'efficiency': 89, 'v2g_capable': False},
        'Audi e-tron': {'battery_capacity': 95, 'max_ac_power': 11, 'max_dc_power': 150, 'efficiency': 87, 'v2g_capable': True},
        'Mercedes EQC': {'battery_capacity': 80, 'max_ac_power': 11, 'max_dc_power': 110, 'efficiency': 88, 'v2g_capable': False}
    }

    # Prix électricité avec variation horaire réaliste
    hours = np.arange(24)
    base_prices = 1.2 + 0.8 * np.sin((hours - 6) * np.pi / 12) + 0.2 * np.random.random(24)
    prices_df = pd.DataFrame({
        'Hour': hours,
        'Price_EUR_MWh': np.maximum(80, base_prices * 100),
        'Price_MAD_kWh': np.maximum(0.8, base_prices)
    })

    # Profils de charge résidentiels
    residential_loads = 400 + 300 * np.sin((hours - 6) * np.pi / 12) + 80 * np.random.random(24)
    loads_df = pd.DataFrame({'Hour': hours, 'Load_MW': residential_loads})

    # Génération PV
    pv_generation = np.maximum(0, 150 * np.sin((hours - 6) * np.pi / 12) * (hours >= 6) * (hours <= 18))
    pv_df = pd.DataFrame({'Hour': hours, 'PV_MW': pv_generation})

    st.session_state.ev2gym_data = {
        'ev_specifications': ev_specs,
        'electricity_prices': prices_df,
        'load_profiles': loads_df,
        'pv_generation': pv_df
    }

def render_control_interface():
    """Interface de contrôle des paramètres d'entrée"""

    with st.sidebar:
        st.markdown("## 🎛️ CONTRÔLES DE SIMULATION")

        # Contrôles de simulation
        st.markdown('<div class="parameter-section">', unsafe_allow_html=True)
        st.markdown('<div class="parameter-title">🔄 Contrôle Simulation</div>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            if st.button("⏸️ PAUSE", use_container_width=True):
                st.session_state.simulation_running = False
                st.info("⏸️ Simulation en pause")

        with col2:
            if st.button("▶️ REPRENDRE", use_container_width=True):
                st.session_state.simulation_running = True
                st.success("▶️ Simulation reprise")

        if st.button("🔄 RESET", use_container_width=True):
            st.session_state.simulation_running = True
            st.session_state.simulation_step = 0
            st.session_state.simulation_data = []
            st.session_state.individual_ev_data = {}
            st.success("🔄 Simulation réinitialisée")

        st.markdown('</div>', unsafe_allow_html=True)

        # Paramètres VE
        st.markdown('<div class="parameter-section">', unsafe_allow_html=True)
        st.markdown('<div class="parameter-title">🚗 Paramètres Véhicules Électriques</div>', unsafe_allow_html=True)

        n_ve_connectes = st.slider("Nombre de VE connectés", 10, 2000, 500, 10,
                                  help="Nombre total de véhicules électriques connectés")

        n_stations = st.slider("Nombre de stations de recharge", 5, 200, 50, 5,
                              help="Nombre de stations de recharge disponibles")

        type_borne = st.selectbox("Type de borne",
                                 ["Standard (AC)", "Rapide (DC)", "Ultra rapide (DC)"],
                                 help="Type de borne de recharge")

        if type_borne == "Standard (AC)":
            limitation_courant = st.slider("Limitation courant AC (A)", 16, 32, 32, 2)
            puissance_max = limitation_courant * 230 * 3 / 1000  # kW
        elif type_borne == "Rapide (DC)":
            puissance_max = st.slider("Puissance DC (kW)", 50, 150, 100, 10)
        else:  # Ultra rapide
            puissance_max = st.slider("Puissance DC (kW)", 150, 350, 250, 25)

        st.markdown('</div>', unsafe_allow_html=True)

        # Paramètres réseau
        st.markdown('<div class="parameter-section">', unsafe_allow_html=True)
        st.markdown('<div class="parameter-title">⚡ Paramètres Réseau</div>', unsafe_allow_html=True)

        puissance_transformateur = st.slider("Puissance transformateur (kVA)", 100, 5000, 1000, 100,
                                            help="Puissance nominale du transformateur")

        tension_limite_min = st.slider("Tension limite min (V)", 200, 240, 220, 5,
                                      help="Tension minimale acceptable")

        tension_limite_max = st.slider("Tension limite max (V)", 240, 280, 250, 5,
                                      help="Tension maximale acceptable")

        courant_limite = st.slider("Courant limite (A)", 100, 2000, 500, 50,
                                  help="Courant maximal admissible")

        scenario_reseau = st.selectbox("Scénario réseau",
                                      ["Fonctionnement normal",
                                       "Réseau en urgence",
                                       "Intégration énergie renouvelable",
                                       "Période de forte demande",
                                       "Période de faible demande"],
                                      help="Scénario de fonctionnement du réseau")

        st.markdown('</div>', unsafe_allow_html=True)

        # Paramètres économiques avec tarification dynamique
        st.markdown('<div class="parameter-section">', unsafe_allow_html=True)
        st.markdown('<div class="parameter-title">💰 Paramètres Économiques (MAD)</div>', unsafe_allow_html=True)

        # Tarification selon le type de borne et l'heure
        current_hour = datetime.now().hour

        # Facteur de demande selon l'heure
        if 17 <= current_hour <= 21:  # Heures de pointe
            facteur_demande = 1.5
            periode = "Pointe"
        elif 22 <= current_hour <= 6:  # Heures creuses
            facteur_demande = 0.7
            periode = "Creuse"
        else:  # Heures normales
            facteur_demande = 1.0
            periode = "Normale"

        st.info(f"🕐 Heure actuelle: {current_hour:02d}h - Période: {periode} (×{facteur_demande})")

        if type_borne == "Standard (AC)":
            prix_base_ac = st.slider("Prix base AC (MAD/kWh)", 1.0, 3.0, 2.0, 0.1)
            prix_actuel = prix_base_ac * facteur_demande
            st.metric("Prix AC actuel", f"{prix_actuel:.2f} MAD/kWh")
        else:  # DC Fast ou Ultra rapide
            prix_base_dc = st.slider("Prix base DC (MAD/kWh)", 5.0, 10.0, 7.5, 0.5)
            prix_actuel = prix_base_dc * facteur_demande
            st.metric("Prix DC actuel", f"{prix_actuel:.2f} MAD/kWh")

        # V2G et services auxiliaires
        activation_v2g = st.checkbox("Activation V2G", value=True,
                                    help="Activer la fonction Vehicle-to-Grid")

        if activation_v2g:
            prix_v2g = st.slider("Prix V2G (MAD/kWh)", 2.0, 8.0, 4.0, 0.5,
                                help="Prix de rachat de l'énergie V2G")

            prix_services_auxiliaires = st.slider("Services auxiliaires (MAD/kW)", 50, 200, 100, 10,
                                                 help="Rémunération des services auxiliaires")

        st.markdown('</div>', unsafe_allow_html=True)

        # Choix de l'algorithme
        st.markdown('<div class="parameter-section">', unsafe_allow_html=True)
        st.markdown('<div class="parameter-title">🤖 Algorithme de Contrôle</div>', unsafe_allow_html=True)

        algorithme = st.selectbox("Algorithme utilisé",
                                 ["RL - Deep Q-Network (DQN)",
                                  "RL - Proximal Policy Optimization (PPO)",
                                  "RL - Soft Actor-Critic (SAC)",
                                  "MPC - Model Predictive Control",
                                  "Heuristique - Round Robin",
                                  "Heuristique - Charge Rapide",
                                  "Heuristique - Équilibrage Intelligent"],
                                 help="Algorithme de prise de décision")

        if "RL" in algorithme:
            apprentissage_actif = st.checkbox("Apprentissage actif", value=True,
                                             help="Activer l'apprentissage en temps réel")

            if apprentissage_actif:
                taux_apprentissage = st.slider("Taux d'apprentissage", 0.001, 0.1, 0.01, 0.001,
                                              format="%.3f")

        st.markdown('</div>', unsafe_allow_html=True)

        # Paramètres de simulation
        st.markdown('<div class="parameter-section">', unsafe_allow_html=True)
        st.markdown('<div class="parameter-title">⏱️ Paramètres Simulation</div>', unsafe_allow_html=True)

        frequence_maj = st.slider("Fréquence mise à jour (s)", 0.5, 5.0, 1.0, 0.1,
                                 help="Intervalle entre les mises à jour")

        historique_max = st.slider("Points d'historique", 100, 1000, 300, 50,
                                  help="Nombre de points à conserver en mémoire")

        st.markdown('</div>', unsafe_allow_html=True)

        # Sauvegarder tous les paramètres
        st.session_state.simulation_params = {
            'n_ve_connectes': n_ve_connectes,
            'n_stations': n_stations,
            'type_borne': type_borne,
            'puissance_max': puissance_max,
            'puissance_transformateur': puissance_transformateur,
            'tension_limite_min': tension_limite_min,
            'tension_limite_max': tension_limite_max,
            'courant_limite': courant_limite,
            'scenario_reseau': scenario_reseau,
            'prix_actuel': prix_actuel,
            'activation_v2g': activation_v2g,
            'prix_v2g': prix_v2g if activation_v2g else 0,
            'prix_services_auxiliaires': prix_services_auxiliaires if activation_v2g else 0,
            'algorithme': algorithme,
            'apprentissage_actif': apprentissage_actif if "RL" in algorithme else False,
            'taux_apprentissage': taux_apprentissage if "RL" in algorithme and apprentissage_actif else 0,
            'frequence_maj': frequence_maj,
            'historique_max': historique_max,
            'facteur_demande': facteur_demande,
            'periode': periode,
            'current_hour': current_hour
        }

def render_main_dashboard():
    """Interface principale du dashboard avec KPI"""

    # Vérifier si on a des données de simulation
    if not st.session_state.simulation_data:
        st.info("🚀 Démarrage de la simulation - Les données apparaîtront sous peu...")
        return

    # Données les plus récentes
    latest_data = st.session_state.simulation_data[-1]
    df = pd.DataFrame(st.session_state.simulation_data)

    # Statut de la simulation
    params = st.session_state.get('simulation_params', {})
    status_color = "#10b981" if st.session_state.simulation_running else "#ef4444"
    status_text = "🟢 SIMULATION ACTIVE" if st.session_state.simulation_running else "🔴 SIMULATION EN PAUSE"

    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #f8fafc, #ffffff); border: 3px solid #e2e8f0;
                border-radius: 20px; padding: 2rem; margin: 2rem 0; text-align: center;">
        <span style="font-size: 1.8rem; font-weight: 800; color: {status_color};">
            {status_text}
        </span>
        <div style="margin-top: 1rem; color: #64748b; font-size: 1.2rem; line-height: 1.8;">
            <strong>Étape:</strong> {st.session_state.simulation_step:,} |
            <strong>VE:</strong> {params.get('n_ve_connectes', 0):,} |
            <strong>Algorithme:</strong> {params.get('algorithme', 'Non défini')} |
            <strong>Scénario:</strong> {params.get('scenario_reseau', 'Normal')}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Rendu des sections KPI
    render_kpi_vehicules_electriques(latest_data, df)
    render_kpi_reseau(latest_data, df)
    render_kpi_economiques(latest_data, df)
    render_visualisations_avancees(df)

def render_kpi_vehicules_electriques(latest_data, df):
    """KPI de performance - Véhicules Électriques"""

    st.markdown('<div class="section-title">🚗⚡ KPI VÉHICULES ÉLECTRIQUES</div>',
                unsafe_allow_html=True)

    st.markdown('<div class="kpi-section-ve">', unsafe_allow_html=True)

    # Métriques principales VE
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        soc_moyen = latest_data.get('soc_moyen_percent', 0)
        soc_status = get_soc_status(soc_moyen)
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{soc_moyen:.1f}</div>
            <div class="metric-label">SOC Moyen</div>
            <div class="metric-unit">Pourcentage (%)</div>
            <div class="status-indicator {soc_status['class']}">
                {soc_status['text']}
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        puissance_v2g = latest_data.get('puissance_v2g_kw', 0)
        puissance_g2v = latest_data.get('puissance_g2v_kw', 0)
        puissance_nette = puissance_g2v - puissance_v2g
        direction = "Charge" if puissance_nette > 0 else "Décharge" if puissance_nette < 0 else "Équilibre"
        color = "#ef4444" if puissance_nette > 0 else "#22c55e" if puissance_nette < 0 else "#6b7280"

        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="color: {color}">{abs(puissance_nette):.1f}</div>
            <div class="metric-label">Puissance Nette</div>
            <div class="metric-unit">Kilowatts (kW)</div>
            <div class="status-indicator" style="background: {color}; color: white;">
                {direction}
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        ve_en_charge = latest_data.get('ve_en_charge', 0)
        ve_en_decharge = latest_data.get('ve_en_decharge', 0)
        ve_inactifs = latest_data.get('ve_inactifs', 0)

        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{ve_en_charge}</div>
            <div class="metric-label">VE en Charge</div>
            <div class="metric-unit">Décharge: {ve_en_decharge} | Inactifs: {ve_inactifs}</div>
            <div class="status-indicator status-good">
                État Flotte
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        decisions_rl = latest_data.get('decisions_rl', 0)
        performance_algo = latest_data.get('performance_algorithme', 0.8) * 100

        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{performance_algo:.1f}</div>
            <div class="metric-label">Performance Algo</div>
            <div class="metric-unit">Décisions: {decisions_rl}</div>
            <div class="status-indicator status-excellent">
                IA/Contrôle
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

def render_kpi_reseau(latest_data, df):
    """KPI Réseau électrique"""

    st.markdown('<div class="section-title">⚡🌐 KPI RÉSEAU ÉLECTRIQUE</div>',
                unsafe_allow_html=True)

    st.markdown('<div class="kpi-section-reseau">', unsafe_allow_html=True)

    # Métriques réseau
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        tension_moyenne = latest_data.get('tension_moyenne_v', 230)
        tension_status = get_tension_status(tension_moyenne)

        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{tension_moyenne:.1f}</div>
            <div class="metric-label">Tension Moyenne</div>
            <div class="metric-unit">Volts (V)</div>
            <div class="status-indicator {tension_status['class']}">
                {tension_status['text']}
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        courant_reseau = latest_data.get('courant_reseau_a', 0)
        courant_limite = st.session_state.simulation_params.get('courant_limite', 500)
        courant_pct = (courant_reseau / courant_limite) * 100
        courant_status = get_courant_status(courant_pct)

        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{courant_reseau:.1f}</div>
            <div class="metric-label">Courant Réseau</div>
            <div class="metric-unit">Ampères (A) - {courant_pct:.1f}%</div>
            <div class="status-indicator {courant_status['class']}">
                {courant_status['text']}
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        frequence_reseau = latest_data.get('frequence_reseau_hz', 50.0)
        frequence_status = get_frequence_status(frequence_reseau)

        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{frequence_reseau:.3f}</div>
            <div class="metric-label">Fréquence Réseau</div>
            <div class="metric-unit">Hertz (Hz)</div>
            <div class="status-indicator {frequence_status['class']}">
                {frequence_status['text']}
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        thd_percent = latest_data.get('thd_percent', 3.0)
        thd_status = get_thd_status(thd_percent)

        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{thd_percent:.2f}</div>
            <div class="metric-label">THD</div>
            <div class="metric-unit">Pourcentage (%)</div>
            <div class="status-indicator {thd_status['class']}">
                {thd_status['text']}
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Deuxième ligne de métriques réseau
    col5, col6, col7, col8 = st.columns(4)

    with col5:
        puissance_active = latest_data.get('puissance_active_kw', 0)
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{puissance_active:.1f}</div>
            <div class="metric-label">Puissance Active</div>
            <div class="metric-unit">Kilowatts (kW)</div>
            <div class="status-indicator status-good">Réseau</div>
        </div>
        """, unsafe_allow_html=True)

    with col6:
        puissance_reactive = latest_data.get('puissance_reactive_kvar', 0)
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{puissance_reactive:.1f}</div>
            <div class="metric-label">Puissance Réactive</div>
            <div class="metric-unit">Kilovars (kVAr)</div>
            <div class="status-indicator status-good">Réseau</div>
        </div>
        """, unsafe_allow_html=True)

    with col7:
        facteur_puissance = latest_data.get('facteur_puissance', 0.95)
        fp_status = get_facteur_puissance_status(facteur_puissance)

        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{facteur_puissance:.3f}</div>
            <div class="metric-label">Facteur Puissance</div>
            <div class="metric-unit">Cosinus φ</div>
            <div class="status-indicator {fp_status['class']}">
                {fp_status['text']}
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col8:
        energie_renouvelable = latest_data.get('energie_renouvelable_kw', 0)
        utilisation_renouvelable = latest_data.get('utilisation_renouvelable_percent', 0)

        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{energie_renouvelable:.1f}</div>
            <div class="metric-label">Énergie Renouvelable</div>
            <div class="metric-unit">kW - {utilisation_renouvelable:.1f}% utilisé</div>
            <div class="status-indicator status-excellent">Disponible</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

def render_kpi_economiques(latest_data, df):
    """KPI Économiques en MAD"""

    st.markdown('<div class="section-title">💰📊 KPI ÉCONOMIQUES (MAD)</div>',
                unsafe_allow_html=True)

    st.markdown('<div class="kpi-section-economique">', unsafe_allow_html=True)

    # Métriques économiques
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        cout_recharge_total = latest_data.get('cout_recharge_total_mad', 0)
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{cout_recharge_total:.2f}</div>
            <div class="metric-label">Coût Recharge Total</div>
            <div class="metric-unit">MAD (cette période)</div>
            <div class="status-indicator status-warning">Dépense</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        revenus_v2g = latest_data.get('revenus_v2g_mad', 0)
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{revenus_v2g:.2f}</div>
            <div class="metric-label">Revenus V2G</div>
            <div class="metric-unit">MAD (cette période)</div>
            <div class="status-indicator status-excellent">Revenu</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        benefice_net = latest_data.get('benefice_net_mad', 0)
        benefice_color = "#22c55e" if benefice_net >= 0 else "#ef4444"
        benefice_status = "Profit" if benefice_net >= 0 else "Perte"

        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="color: {benefice_color}">{benefice_net:.2f}</div>
            <div class="metric-label">Bénéfice Net</div>
            <div class="metric-unit">MAD (cette période)</div>
            <div class="status-indicator" style="background: {benefice_color}; color: white;">
                {benefice_status}
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        services_auxiliaires_mad = latest_data.get('services_auxiliaires_mad', 0)
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{services_auxiliaires_mad:.2f}</div>
            <div class="metric-label">Services Auxiliaires</div>
            <div class="metric-unit">MAD valorisés</div>
            <div class="status-indicator status-good">Optimisé</div>
        </div>
        """, unsafe_allow_html=True)

    # Projections économiques
    col5, col6, col7, col8 = st.columns(4)

    with col5:
        cout_reseau_evite = latest_data.get('cout_reseau_evite_mad', 0)
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{cout_reseau_evite:.2f}</div>
            <div class="metric-label">Coût Réseau Évité</div>
            <div class="metric-unit">MAD économisés</div>
            <div class="status-indicator status-excellent">Optimisation</div>
        </div>
        """, unsafe_allow_html=True)

    with col6:
        projection_horaire = benefice_net * 60  # Projection sur 1 heure
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{projection_horaire:.2f}</div>
            <div class="metric-label">Projection Horaire</div>
            <div class="metric-unit">MAD/heure</div>
            <div class="status-indicator status-good">Prévision</div>
        </div>
        """, unsafe_allow_html=True)

    with col7:
        projection_journaliere = projection_horaire * 24
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{projection_journaliere:.0f}</div>
            <div class="metric-label">Projection Journalière</div>
            <div class="metric-unit">MAD/jour</div>
            <div class="status-indicator status-good">Prévision</div>
        </div>
        """, unsafe_allow_html=True)

    with col8:
        roi_percent = latest_data.get('roi_percent', 0)
        roi_status = get_roi_status(roi_percent)

        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{roi_percent:.1f}</div>
            <div class="metric-label">ROI</div>
            <div class="metric-unit">Pourcentage (%)</div>
            <div class="status-indicator {roi_status['class']}">
                {roi_status['text']}
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# Fonctions de statut pour les indicateurs
def get_soc_status(soc_percent):
    """Statut SOC avec seuils critiques"""
    if soc_percent < 20:
        return {'class': 'status-critical', 'text': 'Critique'}
    elif soc_percent < 40:
        return {'class': 'status-warning', 'text': 'Faible'}
    elif soc_percent < 80:
        return {'class': 'status-good', 'text': 'Normal'}
    else:
        return {'class': 'status-excellent', 'text': 'Optimal'}

def get_tension_status(tension_v):
    """Statut tension selon normes"""
    if 220 <= tension_v <= 240:
        return {'class': 'status-excellent', 'text': 'Excellent'}
    elif 210 <= tension_v <= 250:
        return {'class': 'status-good', 'text': 'Bon'}
    elif 200 <= tension_v <= 260:
        return {'class': 'status-warning', 'text': 'Attention'}
    else:
        return {'class': 'status-critical', 'text': 'Critique'}

def get_courant_status(courant_pct):
    """Statut courant en pourcentage de la limite"""
    if courant_pct <= 70:
        return {'class': 'status-excellent', 'text': 'Sûr'}
    elif courant_pct <= 85:
        return {'class': 'status-good', 'text': 'Normal'}
    elif courant_pct <= 95:
        return {'class': 'status-warning', 'text': 'Élevé'}
    else:
        return {'class': 'status-critical', 'text': 'Limite'}

def get_frequence_status(frequence_hz):
    """Statut fréquence réseau"""
    deviation = abs(frequence_hz - 50.0)
    if deviation <= 0.1:
        return {'class': 'status-excellent', 'text': 'Stable'}
    elif deviation <= 0.2:
        return {'class': 'status-good', 'text': 'Bon'}
    elif deviation <= 0.5:
        return {'class': 'status-warning', 'text': 'Instable'}
    else:
        return {'class': 'status-critical', 'text': 'Critique'}

def get_thd_status(thd_percent):
    """Statut THD selon IEEE 519"""
    if thd_percent <= 3:
        return {'class': 'status-excellent', 'text': 'Excellent'}
    elif thd_percent <= 5:
        return {'class': 'status-good', 'text': 'Conforme'}
    elif thd_percent <= 8:
        return {'class': 'status-warning', 'text': 'Limite'}
    else:
        return {'class': 'status-critical', 'text': 'Non-conforme'}

def get_facteur_puissance_status(fp):
    """Statut facteur de puissance"""
    if fp >= 0.95:
        return {'class': 'status-excellent', 'text': 'Excellent'}
    elif fp >= 0.90:
        return {'class': 'status-good', 'text': 'Bon'}
    elif fp >= 0.85:
        return {'class': 'status-warning', 'text': 'Moyen'}
    else:
        return {'class': 'status-critical', 'text': 'Faible'}

def get_roi_status(roi_percent):
    """Statut ROI"""
    if roi_percent >= 15:
        return {'class': 'status-excellent', 'text': 'Excellent'}
    elif roi_percent >= 10:
        return {'class': 'status-good', 'text': 'Bon'}
    elif roi_percent >= 5:
        return {'class': 'status-warning', 'text': 'Moyen'}
    else:
        return {'class': 'status-critical', 'text': 'Faible'}

def render_visualisations_avancees(df):
    """Visualisations et graphiques avancés"""

    st.markdown('<div class="section-title">📈📊 VISUALISATIONS TEMPS RÉEL</div>',
                unsafe_allow_html=True)

    # Graphiques SOC vs Temps
    st.markdown("#### 🔋 Courbes SOC vs Temps")

    fig_soc = make_subplots(
        rows=2, cols=2,
        subplot_titles=(
            'SOC Moyen avec Variations',
            'Puissance Active vs Réactive',
            'THD en fonction du nombre de VE',
            'Rentabilité V2G/G2V'
        )
    )

    # SOC avec variations
    if len(df) > 0:
        fig_soc.add_trace(go.Scatter(
            x=df['step'], y=df['soc_moyen_percent'],
            mode='lines+markers', name='SOC Moyen',
            line=dict(color='#22c55e', width=3),
            marker=dict(size=6)
        ), row=1, col=1)

        # Puissance active vs réactive
        fig_soc.add_trace(go.Scatter(
            x=df['puissance_active_kw'], y=df['puissance_reactive_kvar'],
            mode='markers', name='Réseau',
            marker=dict(color='#3b82f6', size=8)
        ), row=1, col=2)

        # THD vs nombre VE
        fig_soc.add_trace(go.Scatter(
            x=df['ve_en_charge'], y=df['thd_percent'],
            mode='lines+markers', name='THD',
            line=dict(color='#ef4444', width=2),
            marker=dict(size=6)
        ), row=2, col=1)

        # Rentabilité
        fig_soc.add_trace(go.Scatter(
            x=df['step'], y=df['benefice_net_mad'],
            mode='lines', name='Bénéfice Net',
            line=dict(color='#10b981', width=3)
        ), row=2, col=2)

    fig_soc.update_layout(height=800, showlegend=True)
    st.plotly_chart(fig_soc, use_container_width=True)

    # Histogramme de charge par station
    st.markdown("#### 📊 Distribution de Charge par Station")

    # Générer données de distribution
    n_stations = st.session_state.simulation_params.get('n_stations', 50)
    charges_stations = np.random.gamma(2, 2, n_stations) * 10  # Distribution réaliste

    fig_hist = px.histogram(
        x=charges_stations,
        nbins=20,
        title="Distribution de la Charge par Station",
        labels={'x': 'Charge (kW)', 'y': 'Nombre de Stations'},
        color_discrete_sequence=['#3b82f6']
    )
    fig_hist.update_layout(height=400)
    st.plotly_chart(fig_hist, use_container_width=True)

    # Heatmap des décisions algorithmes
    st.markdown("#### 🤖 Heatmap des Décisions Algorithmes")

    if len(df) >= 10:
        # Créer matrice de décisions
        decisions_matrix = np.random.rand(10, 24)  # 10 VE x 24 heures

        fig_heatmap = px.imshow(
            decisions_matrix,
            labels=dict(x="Heure", y="Véhicule", color="Décision"),
            x=[f"{i:02d}h" for i in range(24)],
            y=[f"VE_{i+1}" for i in range(10)],
            color_continuous_scale="RdYlGn",
            title="Décisions de Charge/Décharge par VE et par Heure"
        )
        fig_heatmap.update_layout(height=500)
        st.plotly_chart(fig_heatmap, use_container_width=True)

    # Comparaison scénarios réseau
    st.markdown("#### 🌐 Comparaison Scénarios Réseau")

    scenarios = ['Normal', 'Urgence', 'Renouvelable', 'Forte Demande', 'Faible Demande']
    performances = [85, 70, 92, 78, 88]  # Performances simulées

    fig_scenarios = px.bar(
        x=scenarios, y=performances,
        title="Performance par Scénario Réseau",
        labels={'x': 'Scénario', 'y': 'Performance (%)'},
        color=performances,
        color_continuous_scale="RdYlGn"
    )
    fig_scenarios.update_layout(height=400)
    st.plotly_chart(fig_scenarios, use_container_width=True)

def execute_realtime_simulation():
    """Moteur de simulation temps réel"""

    if 'simulation_params' not in st.session_state:
        return

    params = st.session_state.simulation_params

    # Générer nouvelles données de simulation
    new_data = simulate_ev_grid_system(
        params=params,
        step=st.session_state.simulation_step
    )

    # Ajouter aux données de simulation
    st.session_state.simulation_data.append(new_data)
    st.session_state.simulation_step += 1

    # Maintenir historique limité
    max_history = params.get('historique_max', 300)
    if len(st.session_state.simulation_data) > max_history:
        st.session_state.simulation_data = st.session_state.simulation_data[-max_history:]

    # Mise à jour automatique
    time.sleep(params.get('frequence_maj', 1.0))
    st.rerun()

def simulate_ev_grid_system(params, step):
    """Simulation complète du système VE-Réseau"""

    # Paramètres de simulation
    n_ve = params['n_ve_connectes']
    algorithme = params['algorithme']
    scenario = params['scenario_reseau']
    current_hour = datetime.now().hour

    # Simulation selon l'algorithme choisi
    if "RL" in algorithme:
        ev_data = simulate_rl_algorithm(n_ve, algorithme, step, params)
    elif "MPC" in algorithme:
        ev_data = simulate_mpc_algorithm(n_ve, step, params)
    else:  # Heuristique
        ev_data = simulate_heuristic_algorithm(n_ve, algorithme, step, params)

    # Simulation réseau selon le scénario
    grid_data = simulate_grid_scenario(ev_data, scenario, params)

    # Calculs économiques
    economic_data = calculate_economic_metrics(ev_data, grid_data, params)

    # Données complètes
    complete_data = {
        'timestamp': datetime.now(),
        'step': step,
        'hour': current_hour,
        'algorithme': algorithme,
        'scenario': scenario,
        **ev_data,
        **grid_data,
        **economic_data
    }

    return complete_data

def simulate_rl_algorithm(n_ve, algorithme, step, params):
    """Simulation des algorithmes RL (DQN, PPO, SAC)"""

    # Progression d'apprentissage
    if params.get('apprentissage_actif', False):
        learning_progress = min(1.0, step / 500)  # Convergence sur 500 étapes
    else:
        learning_progress = 0.85  # Performance stable

    # Performance selon l'algorithme
    if "DQN" in algorithme:
        base_performance = 0.75 + 0.20 * learning_progress
        exploration_factor = max(0.1, 1.0 - step / 300)
    elif "PPO" in algorithme:
        base_performance = 0.80 + 0.18 * learning_progress
        exploration_factor = max(0.05, 1.0 - step / 400)
    else:  # SAC
        base_performance = 0.85 + 0.15 * learning_progress
        exploration_factor = max(0.02, 1.0 - step / 350)

    # SOC moyen avec apprentissage
    hour = datetime.now().hour
    base_soc = 50 + 25 * np.sin((hour - 6) * np.pi / 12)
    soc_moyen = base_soc + 20 * learning_progress + np.random.normal(0, 5)
    soc_moyen = np.clip(soc_moyen, 20, 95)

    # Décisions de charge/décharge intelligentes
    if 22 <= hour <= 6:  # Heures creuses - favoriser charge
        charge_factor = 0.7 + 0.2 * learning_progress
        decharge_factor = 0.1 + 0.1 * learning_progress
    elif 17 <= hour <= 21:  # Heures pointe - favoriser V2G
        charge_factor = 0.3 + 0.1 * learning_progress
        decharge_factor = 0.4 + 0.3 * learning_progress
    else:  # Heures normales
        charge_factor = 0.5 + 0.2 * learning_progress
        decharge_factor = 0.2 + 0.2 * learning_progress

    ve_en_charge = int(n_ve * charge_factor)
    ve_en_decharge = int(n_ve * decharge_factor * params.get('activation_v2g', 0))
    ve_inactifs = n_ve - ve_en_charge - ve_en_decharge

    # Puissances
    puissance_unitaire = params.get('puissance_max', 22)
    puissance_g2v = ve_en_charge * puissance_unitaire
    puissance_v2g = ve_en_decharge * puissance_unitaire

    return {
        'soc_moyen_percent': soc_moyen,
        've_en_charge': ve_en_charge,
        've_en_decharge': ve_en_decharge,
        've_inactifs': ve_inactifs,
        'puissance_g2v_kw': puissance_g2v,
        'puissance_v2g_kw': puissance_v2g,
        'performance_algorithme': base_performance,
        'decisions_rl': ve_en_charge + ve_en_decharge,
        'learning_progress': learning_progress,
        'exploration_factor': exploration_factor
    }

def simulate_mpc_algorithm(n_ve, step, params):
    """Simulation MPC - Model Predictive Control"""

    hour = datetime.now().hour

    # MPC optimise sur horizon de prédiction
    horizon = 6  # 6 heures

    # Prédiction des prix
    prix_actuel = params.get('prix_actuel', 2.0)
    prix_predit = prix_actuel * (1 + 0.3 * np.sin((hour + horizon) * np.pi / 12))

    # Optimisation basée sur prédiction
    if prix_predit > prix_actuel * 1.2:  # Prix élevé prédit - décharger
        charge_factor = 0.3
        decharge_factor = 0.5
    elif prix_predit < prix_actuel * 0.8:  # Prix bas prédit - charger
        charge_factor = 0.8
        decharge_factor = 0.1
    else:  # Prix stable - équilibrer
        charge_factor = 0.6
        decharge_factor = 0.25

    # SOC optimisé
    soc_target = 70 if prix_predit > prix_actuel else 60
    soc_moyen = soc_target + np.random.normal(0, 8)
    soc_moyen = np.clip(soc_moyen, 25, 90)

    ve_en_charge = int(n_ve * charge_factor)
    ve_en_decharge = int(n_ve * decharge_factor * params.get('activation_v2g', 0))
    ve_inactifs = n_ve - ve_en_charge - ve_en_decharge

    puissance_unitaire = params.get('puissance_max', 22)
    puissance_g2v = ve_en_charge * puissance_unitaire
    puissance_v2g = ve_en_decharge * puissance_unitaire

    return {
        'soc_moyen_percent': soc_moyen,
        've_en_charge': ve_en_charge,
        've_en_decharge': ve_en_decharge,
        've_inactifs': ve_inactifs,
        'puissance_g2v_kw': puissance_g2v,
        'puissance_v2g_kw': puissance_v2g,
        'performance_algorithme': 0.88,
        'decisions_rl': 0,
        'learning_progress': 0,
        'exploration_factor': 0,
        'prix_predit': prix_predit,
        'horizon_mpc': horizon
    }

def simulate_heuristic_algorithm(n_ve, algorithme, step, params):
    """Simulation des algorithmes heuristiques"""

    hour = datetime.now().hour

    if "Round Robin" in algorithme:
        # Distribution équitable
        charge_factor = 0.6
        decharge_factor = 0.2
        performance = 0.65

    elif "Charge Rapide" in algorithme:
        # Charge maximale
        charge_factor = 0.9
        decharge_factor = 0.05
        performance = 0.60

    else:  # Équilibrage Intelligent
        # Équilibrage basé sur SOC et heure
        if 22 <= hour <= 6:
            charge_factor = 0.8
            decharge_factor = 0.1
        elif 17 <= hour <= 21:
            charge_factor = 0.4
            decharge_factor = 0.3
        else:
            charge_factor = 0.6
            decharge_factor = 0.2
        performance = 0.72

    # SOC selon stratégie
    base_soc = 55 + 20 * np.sin((hour - 4) * np.pi / 12)
    soc_moyen = np.clip(base_soc + np.random.normal(0, 6), 30, 85)

    ve_en_charge = int(n_ve * charge_factor)
    ve_en_decharge = int(n_ve * decharge_factor * params.get('activation_v2g', 0))
    ve_inactifs = n_ve - ve_en_charge - ve_en_decharge

    puissance_unitaire = params.get('puissance_max', 22)
    puissance_g2v = ve_en_charge * puissance_unitaire
    puissance_v2g = ve_en_decharge * puissance_unitaire

    return {
        'soc_moyen_percent': soc_moyen,
        've_en_charge': ve_en_charge,
        've_en_decharge': ve_en_decharge,
        've_inactifs': ve_inactifs,
        'puissance_g2v_kw': puissance_g2v,
        'puissance_v2g_kw': puissance_v2g,
        'performance_algorithme': performance,
        'decisions_rl': 0,
        'learning_progress': 0,
        'exploration_factor': 0
    }

def simulate_grid_scenario(ev_data, scenario, params):
    """Simulation du réseau selon le scénario"""

    # Charge de base selon l'heure
    hour = datetime.now().hour
    if 17 <= hour <= 21:  # Pointe
        base_load_factor = 0.9
    elif 22 <= hour <= 6:  # Creuse
        base_load_factor = 0.4
    else:  # Normale
        base_load_factor = 0.7

    # Modifications selon le scénario
    if scenario == "Réseau en urgence":
        tension_moyenne = 215 + np.random.normal(0, 8)  # Tension dégradée
        frequence_reseau = 49.8 + np.random.normal(0, 0.15)
        thd_percent = 6.5 + np.random.normal(0, 1.5)
        load_factor = base_load_factor * 1.3

    elif scenario == "Intégration énergie renouvelable":
        tension_moyenne = 235 + np.random.normal(0, 5)
        frequence_reseau = 50.1 + np.random.normal(0, 0.08)
        thd_percent = 2.8 + np.random.normal(0, 0.8)
        load_factor = base_load_factor * 0.8
        # Énergie renouvelable disponible
        if 8 <= hour <= 17:  # Heures solaires
            energie_renouvelable = 200 + 150 * np.sin((hour - 8) * np.pi / 9)
        else:
            energie_renouvelable = 50  # Éolien résiduel

    elif scenario == "Période de forte demande":
        tension_moyenne = 220 + np.random.normal(0, 6)
        frequence_reseau = 49.9 + np.random.normal(0, 0.12)
        thd_percent = 4.8 + np.random.normal(0, 1.2)
        load_factor = base_load_factor * 1.5

    elif scenario == "Période de faible demande":
        tension_moyenne = 240 + np.random.normal(0, 4)
        frequence_reseau = 50.05 + np.random.normal(0, 0.05)
        thd_percent = 2.2 + np.random.normal(0, 0.6)
        load_factor = base_load_factor * 0.6

    else:  # Fonctionnement normal
        tension_moyenne = 230 + np.random.normal(0, 5)
        frequence_reseau = 50.0 + np.random.normal(0, 0.1)
        thd_percent = 3.5 + np.random.normal(0, 1.0)
        load_factor = base_load_factor

    # Calculs réseau
    puissance_transformateur = params.get('puissance_transformateur', 1000)
    puissance_active = puissance_transformateur * load_factor

    # Impact des VE
    puissance_ve_nette = ev_data['puissance_g2v_kw'] - ev_data['puissance_v2g_kw']
    puissance_active += puissance_ve_nette

    # Courant réseau (approximation triphasée)
    courant_reseau = puissance_active * 1000 / (tension_moyenne * 1.732)

    # Puissance réactive (estimation)
    facteur_puissance = 0.92 + 0.06 * np.random.random()
    puissance_reactive = puissance_active * np.tan(np.arccos(facteur_puissance))

    # Énergie renouvelable (si pas définie)
    if 'energie_renouvelable' not in locals():
        if 8 <= hour <= 17:
            energie_renouvelable = 100 + 80 * np.sin((hour - 8) * np.pi / 9)
        else:
            energie_renouvelable = 20

    utilisation_renouvelable = min(100, (puissance_ve_nette / max(1, energie_renouvelable)) * 100)

    return {
        'tension_moyenne_v': np.clip(tension_moyenne, 200, 260),
        'courant_reseau_a': courant_reseau,
        'frequence_reseau_hz': np.clip(frequence_reseau, 49.0, 51.0),
        'thd_percent': np.clip(thd_percent, 1.0, 10.0),
        'puissance_active_kw': puissance_active,
        'puissance_reactive_kvar': puissance_reactive,
        'facteur_puissance': facteur_puissance,
        'energie_renouvelable_kw': energie_renouvelable,
        'utilisation_renouvelable_percent': utilisation_renouvelable,
        'load_factor': load_factor
    }

def calculate_economic_metrics(ev_data, grid_data, params):
    """Calculs économiques en MAD"""

    # Coûts de recharge
    puissance_charge = ev_data['puissance_g2v_kw']
    prix_actuel = params.get('prix_actuel', 2.0)
    duree_periode = params.get('frequence_maj', 1.0) / 60  # en heures

    cout_recharge_total = puissance_charge * prix_actuel * duree_periode

    # Revenus V2G
    puissance_decharge = ev_data['puissance_v2g_kw']
    prix_v2g = params.get('prix_v2g', 4.0)
    revenus_v2g = puissance_decharge * prix_v2g * duree_periode

    # Services auxiliaires
    prix_services = params.get('prix_services_auxiliaires', 100)

    # Régulation de fréquence
    freq_deviation = abs(grid_data['frequence_reseau_hz'] - 50.0)
    if freq_deviation > 0.1:
        regulation_freq = puissance_decharge * 0.5  # 50% pour régulation
        revenus_regulation = regulation_freq * prix_services / 1000 * duree_periode
    else:
        revenus_regulation = 0

    # Support de tension
    tension_deviation = abs(grid_data['tension_moyenne_v'] - 230) / 230
    if tension_deviation > 0.05:
        support_tension = puissance_decharge * 0.3  # 30% pour support tension
        revenus_tension = support_tension * prix_services / 1000 * duree_periode
    else:
        revenus_tension = 0

    services_auxiliaires_total = revenus_regulation + revenus_tension

    # Coût réseau évité (réduction de pointe)
    if grid_data['load_factor'] > 0.8:
        cout_evite = puissance_decharge * 0.5 * duree_periode  # Évitement pointe
    else:
        cout_evite = 0

    # Bénéfice net
    benefice_net = revenus_v2g + services_auxiliaires_total + cout_evite - cout_recharge_total

    # ROI (approximation)
    investissement_estime = params.get('n_ve_connectes', 500) * 50  # 50 MAD par VE
    if investissement_estime > 0:
        roi_percent = (benefice_net * 24 * 365 / investissement_estime) * 100  # ROI annuel
    else:
        roi_percent = 0

    return {
        'cout_recharge_total_mad': cout_recharge_total,
        'revenus_v2g_mad': revenus_v2g,
        'services_auxiliaires_mad': services_auxiliaires_total,
        'cout_reseau_evite_mad': cout_evite,
        'benefice_net_mad': benefice_net,
        'roi_percent': np.clip(roi_percent, -50, 100),
        'revenus_regulation_mad': revenus_regulation,
        'revenus_tension_mad': revenus_tension
    }

if __name__ == "__main__":
    main()
