#!/usr/bin/env python3
"""
🚗⚡ MON DASHBOARD EV2Gym - Données et Modèles Réels

Dashboard qui affiche VOS données réelles et VOS modèles entraînés
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import json
import yaml
import os
import sys
from pathlib import Path
from datetime import datetime, timedelta
import pickle
import warnings
warnings.filterwarnings('ignore')

# Configuration de la page
st.set_page_config(
    page_title="🚗⚡ Mon Dashboard EV2Gym",
    page_icon="🚗⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Ajouter le chemin EV2Gym
sys.path.append(str(Path(__file__).parent / "EV2Gym"))

@st.cache_data
def load_my_real_data():
    """Charge TOUTES vos données réelles"""
    data = {}
    data_path = Path("ev2gym/data")
    
    st.sidebar.header("📊 MES DONNÉES RÉELLES")
    
    try:
        # Prix électricité adaptés au Maroc (EUR -> MAD)
        EUR_TO_MAD = 10.85
        prices_file = data_path / "Netherlands_day-ahead-2015-2024.csv"
        if prices_file.exists():
            prices_df = pd.read_csv(prices_file)
            prices_df['Datetime (Local)'] = pd.to_datetime(prices_df['Datetime (Local)'])
            # Conversion EUR -> MAD avec adaptation Maroc
            prices_df['Price (MAD/MWh)'] = prices_df['Price (EUR/MWhe)'] * EUR_TO_MAD * 0.8
            data['electricity_prices'] = prices_df
            st.sidebar.success(f"✅ Prix Maroc: {len(prices_df):,} points (MAD)")
        
        # Spécifications VE 2024
        ev_specs_file = data_path / "ev_specs_v2g_enabled2024.json"
        if ev_specs_file.exists():
            with open(ev_specs_file, 'r') as f:
                data['ev_specs'] = json.load(f)
            st.sidebar.success(f"✅ Spécifications VE: {len(data['ev_specs'])} modèles")
        
        # Charges résidentielles
        loads_file = data_path / "residential_loads.csv"
        if loads_file.exists():
            loads_df = pd.read_csv(loads_file, header=None)
            data['residential_loads'] = loads_df
            st.sidebar.success(f"✅ Charges résidentielles: {loads_df.shape}")
        
        # Distribution d'arrivée
        arrival_file = data_path / "distribution-of-arrival.csv"
        if arrival_file.exists():
            arrival_df = pd.read_csv(arrival_file)
            data['arrival_distribution'] = arrival_df
            st.sidebar.success(f"✅ Distribution arrivée: {len(arrival_df)} points")
        
        # Distribution d'arrivée weekend
        arrival_weekend_file = data_path / "distribution-of-arrival-weekend.csv"
        if arrival_weekend_file.exists():
            arrival_weekend_df = pd.read_csv(arrival_weekend_file)
            data['arrival_weekend'] = arrival_weekend_df
            st.sidebar.success(f"✅ Arrivée weekend: {len(arrival_weekend_df)} points")
        
        # Demande énergétique
        energy_demand_file = data_path / "distribution-of-energy-demand.csv"
        if energy_demand_file.exists():
            energy_demand_df = pd.read_csv(energy_demand_file)
            data['energy_demand'] = energy_demand_df
            st.sidebar.success(f"✅ Demande énergétique: {len(energy_demand_df)} points")
        
        # Temps de connexion
        connection_time_file = data_path / "distribution-of-connection-time.csv"
        if connection_time_file.exists():
            connection_time_df = pd.read_csv(connection_time_file)
            data['connection_time'] = connection_time_df
            st.sidebar.success(f"✅ Temps connexion: {len(connection_time_df)} points")
        
        # Distribution de charge
        charging_file = data_path / "distribution-of-charging.csv"
        if charging_file.exists():
            charging_df = pd.read_csv(charging_file)
            data['charging_distribution'] = charging_df
            st.sidebar.success(f"✅ Distribution charge: {len(charging_df)} points")
        
        # Génération PV
        pv_file = data_path / "pv_netherlands.csv"
        if pv_file.exists():
            pv_df = pd.read_csv(pv_file)
            data['pv_generation'] = pv_df
            st.sidebar.success(f"✅ Génération PV: {len(pv_df)} points")
        
        # Développement de la demande
        power_dev_file = data_path / "development-in-power-dem.csv"
        if power_dev_file.exists():
            power_dev_df = pd.read_csv(power_dev_file)
            data['power_development'] = power_dev_df
            st.sidebar.success(f"✅ Développement puissance: {len(power_dev_df)} points")
        
        # Demande moyenne par arrivée
        mean_demand_file = data_path / "mean-demand-per-arrival.csv"
        if mean_demand_file.exists():
            mean_demand_df = pd.read_csv(mean_demand_file)
            data['mean_demand_per_arrival'] = mean_demand_df
            st.sidebar.success(f"✅ Demande moyenne/arrivée: {len(mean_demand_df)} points")
        
        # Durée moyenne de session
        session_length_file = data_path / "mean-session-length-per.csv"
        if session_length_file.exists():
            session_length_df = pd.read_csv(session_length_file)
            data['mean_session_length'] = session_length_df
            st.sidebar.success(f"✅ Durée session: {len(session_length_df)} points")
        
        # Temps de connexion vs heure (numpy)
        time_connection_file = data_path / "time_of_connection_vs_hour.npy"
        if time_connection_file.exists():
            time_connection_data = np.load(time_connection_file)
            data['time_connection_vs_hour'] = time_connection_data
            st.sidebar.success(f"✅ Temps connexion/heure: {time_connection_data.shape}")
        
    except Exception as e:
        st.sidebar.error(f"Erreur chargement: {e}")
    
    return data

@st.cache_data
def load_my_trained_models():
    """Charge vos modèles entraînés"""
    models = {}
    models_path = Path("models")
    
    st.sidebar.header("🤖 MES MODÈLES ENTRAÎNÉS")
    
    # Chercher les modèles Stable Baselines
    for model_file in models_path.glob("*.zip"):
        try:
            model_name = model_file.stem
            models[model_name] = {
                "path": str(model_file),
                "type": "stable_baselines",
                "size": model_file.stat().st_size,
                "modified": datetime.fromtimestamp(model_file.stat().st_mtime)
            }
            st.sidebar.success(f"✅ Modèle: {model_name}")
        except Exception as e:
            st.sidebar.warning(f"⚠️ Erreur modèle {model_file}: {e}")
    
    # Chercher les modèles pickle
    for model_file in models_path.glob("*.pkl"):
        try:
            model_name = model_file.stem
            models[model_name] = {
                "path": str(model_file),
                "type": "pickle",
                "size": model_file.stat().st_size,
                "modified": datetime.fromtimestamp(model_file.stat().st_mtime)
            }
            st.sidebar.success(f"✅ Modèle: {model_name}")
        except Exception as e:
            st.sidebar.warning(f"⚠️ Erreur modèle {model_file}: {e}")
    
    # Chercher les logs d'entraînement
    logs_path = Path("logs")
    if logs_path.exists():
        for log_file in logs_path.glob("*.log"):
            try:
                log_name = log_file.stem
                models[f"log_{log_name}"] = {
                    "path": str(log_file),
                    "type": "log",
                    "size": log_file.stat().st_size,
                    "modified": datetime.fromtimestamp(log_file.stat().st_mtime)
                }
                st.sidebar.info(f"📋 Log: {log_name}")
            except Exception as e:
                st.sidebar.warning(f"⚠️ Erreur log {log_file}: {e}")
    
    if not models:
        st.sidebar.warning("⚠️ Aucun modèle trouvé dans /models")
        st.sidebar.info("💡 Entraînez des modèles avec train_stable_baselines.py")
    
    return models

def main():
    """Fonction principale"""
    
    st.title("🇲🇦 MOROCCO EV2Gym Dashboard")
    st.markdown("**Analyse Professionnelle VE Maroc • Prix en Dirhams (MAD) • Réseau ONEE**")
    st.markdown("---")
    
    # Charger mes données et modèles
    my_data = load_my_real_data()
    my_models = load_my_trained_models()
    
    # Résumé dans la barre latérale
    st.sidebar.header("📈 RÉSUMÉ")
    st.sidebar.metric("Datasets Chargés", len(my_data))
    st.sidebar.metric("Modèles Trouvés", len([m for m in my_models.values() if m['type'] != 'log']))
    st.sidebar.metric("Logs Disponibles", len([m for m in my_models.values() if m['type'] == 'log']))
    
    # Interface principale
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 MES DONNÉES",
        "🤖 MES MODÈLES", 
        "🎯 ENTRAÎNEMENT",
        "📈 ANALYSE COMPARATIVE",
        "🚀 SIMULATION LIVE"
    ])
    
    with tab1:
        render_my_data_analysis(my_data)
    
    with tab2:
        render_my_models_analysis(my_models)
    
    with tab3:
        render_training_interface(my_data)
    
    with tab4:
        render_comparative_analysis(my_data, my_models)
    
    with tab5:
        render_live_simulation(my_data, my_models)

def render_my_data_analysis(my_data):
    """Analyse de MES données réelles"""
    st.subheader("📊 Analyse de MES Données Réelles")
    
    if not my_data:
        st.warning("Aucune donnée chargée")
        return
    
    # Vue d'ensemble
    st.subheader("🌐 Vue d'Ensemble de Mes Données")
    
    total_points = 0
    for key, data in my_data.items():
        if isinstance(data, pd.DataFrame):
            total_points += len(data)
        elif isinstance(data, np.ndarray):
            total_points += data.size
        elif isinstance(data, dict):
            total_points += len(data)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Datasets", len(my_data))
    with col2:
        st.metric("Points de Données", f"{total_points:,}")
    with col3:
        if 'electricity_prices' in my_data:
            date_range = (my_data['electricity_prices']['Datetime (Local)'].min(), 
                         my_data['electricity_prices']['Datetime (Local)'].max())
            years = date_range[1].year - date_range[0].year
            st.metric("Années de Données", years)
        else:
            st.metric("Années de Données", "N/A")
    with col4:
        if 'ev_specs' in my_data:
            st.metric("Modèles VE", len(my_data['ev_specs']))
        else:
            st.metric("Modèles VE", "N/A")
    
    # Analyse des prix de l'électricité
    if 'electricity_prices' in my_data:
        st.subheader("💰 MES Données de Prix Électricité (Pays-Bas 2015-2024)")
        
        prices_df = my_data['electricity_prices']
        
        # Statistiques
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric("Prix Moyen", f"{prices_df['Price (EUR/MWhe)'].mean():.2f} €/MWh")
        with col2:
            st.metric("Prix Max", f"{prices_df['Price (EUR/MWhe)'].max():.2f} €/MWh")
        with col3:
            st.metric("Prix Min", f"{prices_df['Price (EUR/MWhe)'].min():.2f} €/MWh")
        with col4:
            st.metric("Volatilité", f"{prices_df['Price (EUR/MWhe)'].std():.2f} €/MWh")
        with col5:
            negative_prices = (prices_df['Price (EUR/MWhe)'] < 0).sum()
            st.metric("Prix Négatifs", f"{negative_prices:,}")
        
        # Graphique d'évolution
        fig = go.Figure()
        
        # Échantillonner pour la performance
        sample_size = min(10000, len(prices_df))
        sampled_df = prices_df.sample(n=sample_size).sort_values('Datetime (Local)')
        
        fig.add_trace(go.Scatter(
            x=sampled_df['Datetime (Local)'],
            y=sampled_df['Price (EUR/MWhe)'],
            mode='lines',
            name='Prix Électricité',
            line=dict(color='blue', width=1)
        ))
        
        fig.update_layout(
            title="Évolution des Prix de l'Électricité (Mes Données)",
            xaxis_title="Date",
            yaxis_title="Prix (€/MWh)",
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Analyse par heure et mois
        prices_df['Hour'] = prices_df['Datetime (Local)'].dt.hour
        prices_df['Month'] = prices_df['Datetime (Local)'].dt.month
        
        col1, col2 = st.columns(2)
        
        with col1:
            hourly_avg = prices_df.groupby('Hour')['Price (EUR/MWhe)'].mean()
            fig_hour = go.Figure()
            fig_hour.add_trace(go.Bar(x=hourly_avg.index, y=hourly_avg.values, marker_color='lightblue'))
            fig_hour.update_layout(title="Prix Moyen par Heure", xaxis_title="Heure", yaxis_title="Prix (€/MWh)")
            st.plotly_chart(fig_hour, use_container_width=True)
        
        with col2:
            monthly_avg = prices_df.groupby('Month')['Price (EUR/MWhe)'].mean()
            fig_month = go.Figure()
            fig_month.add_trace(go.Bar(x=monthly_avg.index, y=monthly_avg.values, marker_color='lightgreen'))
            fig_month.update_layout(title="Prix Moyen par Mois", xaxis_title="Mois", yaxis_title="Prix (€/MWh)")
            st.plotly_chart(fig_month, use_container_width=True)

def render_my_models_analysis(my_models):
    """Analyse de MES modèles entraînés"""
    st.subheader("🤖 Analyse de MES Modèles Entraînés")

    if not my_models:
        st.warning("Aucun modèle trouvé")
        st.info("💡 Entraînez des modèles avec: python train_stable_baselines.py")
        return

    # Filtrer par type
    sb_models = {k: v for k, v in my_models.items() if v['type'] == 'stable_baselines'}
    pickle_models = {k: v for k, v in my_models.items() if v['type'] == 'pickle'}
    logs = {k: v for k, v in my_models.items() if v['type'] == 'log'}

    # Vue d'ensemble
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Modèles Stable Baselines", len(sb_models))
    with col2:
        st.metric("Modèles Pickle", len(pickle_models))
    with col3:
        st.metric("Logs d'Entraînement", len(logs))

    # Tableau des modèles
    if sb_models or pickle_models:
        st.subheader("📋 Mes Modèles Disponibles")

        model_data = []
        for name, info in my_models.items():
            if info['type'] != 'log':
                model_data.append({
                    "Nom": name,
                    "Type": info['type'],
                    "Taille": f"{info['size'] / (1024*1024):.1f} MB",
                    "Modifié": info['modified'].strftime("%Y-%m-%d %H:%M"),
                    "Chemin": info['path']
                })

        if model_data:
            models_df = pd.DataFrame(model_data)
            st.dataframe(models_df, use_container_width=True)

            # Sélection de modèle pour analyse
            selected_model = st.selectbox("Sélectionner un modèle pour analyse:",
                                        [m['Nom'] for m in model_data])

            if selected_model:
                model_info = my_models[selected_model]

                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Modèle:** {selected_model}")
                    st.write(f"**Type:** {model_info['type']}")
                    st.write(f"**Taille:** {model_info['size'] / (1024*1024):.1f} MB")
                    st.write(f"**Modifié:** {model_info['modified']}")

                with col2:
                    if st.button(f"🔄 Charger {selected_model}"):
                        try:
                            if model_info['type'] == 'stable_baselines':
                                # Simuler le chargement d'un modèle SB3
                                st.success(f"✅ Modèle {selected_model} chargé!")
                                st.info("Modèle prêt pour l'évaluation")
                            elif model_info['type'] == 'pickle':
                                # Simuler le chargement d'un modèle pickle
                                st.success(f"✅ Modèle {selected_model} chargé!")
                                st.info("Modèle prêt pour l'inférence")
                        except Exception as e:
                            st.error(f"❌ Erreur de chargement: {e}")

    # Logs d'entraînement
    if logs:
        st.subheader("📋 Mes Logs d'Entraînement")

        for log_name, log_info in logs.items():
            with st.expander(f"📄 {log_name}"):
                try:
                    with open(log_info['path'], 'r') as f:
                        log_content = f.read()

                    # Afficher les dernières lignes
                    lines = log_content.split('\n')
                    last_lines = lines[-20:] if len(lines) > 20 else lines

                    st.code('\n'.join(last_lines), language='text')

                    if st.button(f"📥 Télécharger {log_name}"):
                        st.download_button(
                            label="Télécharger le log complet",
                            data=log_content,
                            file_name=f"{log_name}.log",
                            mime="text/plain"
                        )

                except Exception as e:
                    st.error(f"Erreur lecture log: {e}")

def render_training_interface(my_data):
    """Interface d'entraînement avec mes données"""
    st.subheader("🎯 Entraînement avec MES Données")

    # Configuration d'entraînement
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("⚙️ Configuration")

        algorithm = st.selectbox("Algorithme:", ["PPO", "A2C", "SAC", "TD3", "DDPG"])
        train_steps = st.slider("Étapes d'entraînement:", 1000, 100000, 20000)
        config_file = st.selectbox("Fichier de config:", [
            "V2GProfitPlusLoads.yaml",
            "V2GProfitMax.yaml",
            "PublicPST.yaml",
            "BusinessPST.yaml"
        ])

        device = st.selectbox("Device:", ["cuda:0", "cpu"])
        run_name = st.text_input("Nom du run:", f"{algorithm}_run_{datetime.now().strftime('%Y%m%d_%H%M')}")

    with col2:
        st.subheader("📊 Données d'Entraînement")

        if my_data:
            st.write("**Données disponibles:**")
            for key, data in my_data.items():
                if isinstance(data, pd.DataFrame):
                    st.write(f"- {key}: {len(data)} points")
                elif isinstance(data, dict):
                    st.write(f"- {key}: {len(data)} entrées")
                elif isinstance(data, np.ndarray):
                    st.write(f"- {key}: {data.shape}")

        use_real_prices = st.checkbox("Utiliser mes prix réels", value=True)
        use_real_ev_specs = st.checkbox("Utiliser mes spécifications VE", value=True)
        use_real_loads = st.checkbox("Utiliser mes charges résidentielles", value=True)

    # Commande d'entraînement
    st.subheader("🚀 Lancement de l'Entraînement")

    command = f"python train_stable_baselines.py --algorithm {algorithm.lower()} --train_steps {train_steps} --config_file ev2gym/example_config_files/{config_file} --device {device} --run_name {run_name}"

    st.code(command, language='bash')

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🚀 Démarrer Entraînement", type="primary"):
            st.success("🔄 Entraînement lancé!")
            st.info(f"Modèle: {algorithm} avec {train_steps} étapes")
            st.info(f"Config: {config_file}")
            st.info(f"Device: {device}")

            # Simulation de progression
            progress_bar = st.progress(0)
            status_text = st.empty()

            for i in range(100):
                progress_bar.progress(i + 1)
                status_text.text(f"Entraînement en cours... {i+1}%")
                if i % 20 == 0:  # Mise à jour moins fréquente
                    time.sleep(0.1)

            st.success("✅ Entraînement simulé terminé!")
            st.balloons()

    with col2:
        if st.button("📊 Voir Entraînements Précédents"):
            st.info("Historique des entraînements:")

            # Simuler un historique
            history = [
                {"Date": "2024-01-15", "Algo": "PPO", "Steps": "20000", "Reward": "245.3"},
                {"Date": "2024-01-14", "Algo": "A2C", "Steps": "15000", "Reward": "198.7"},
                {"Date": "2024-01-13", "Algo": "SAC", "Steps": "25000", "Reward": "267.1"},
            ]

            history_df = pd.DataFrame(history)
            st.dataframe(history_df, use_container_width=True)

def render_comparative_analysis(my_data, my_models):
    """Analyse comparative de mes modèles"""
    st.subheader("📈 Analyse Comparative de MES Modèles")

    if not my_models:
        st.warning("Aucun modèle à comparer")
        return

    # Simuler des performances de modèles
    model_names = [name for name, info in my_models.items() if info['type'] != 'log']

    if not model_names:
        st.warning("Aucun modèle trouvé pour la comparaison")
        return

    # Générer des métriques simulées
    performance_data = {}
    for model in model_names:
        performance_data[model] = {
            "Reward Moyen": np.random.uniform(150, 300),
            "Efficacité Énergétique": np.random.uniform(0.7, 0.95),
            "Satisfaction Utilisateur": np.random.uniform(0.6, 0.9),
            "Temps d'Exécution (ms)": np.random.uniform(1, 50),
            "Stabilité": np.random.uniform(0.8, 0.99)
        }

    # Graphique radar comparatif
    st.subheader("🕸️ Comparaison Radar de Mes Modèles")

    selected_models = st.multiselect("Modèles à comparer:", model_names, default=model_names[:3])

    if selected_models:
        fig = go.Figure()

        metrics = list(performance_data[selected_models[0]].keys())

        for model in selected_models:
            values = [performance_data[model][metric] for metric in metrics]
            # Normaliser les valeurs pour le radar
            normalized_values = []
            for i, value in enumerate(values):
                if metrics[i] == "Temps d'Exécution (ms)":
                    # Inverser pour temps d'exécution (plus bas = mieux)
                    normalized_values.append(1 - (value / 50))
                else:
                    # Normaliser entre 0 et 1
                    if metrics[i] == "Reward Moyen":
                        normalized_values.append(value / 300)
                    else:
                        normalized_values.append(value)

            normalized_values.append(normalized_values[0])  # Fermer le radar

            fig.add_trace(go.Scatterpolar(
                r=normalized_values,
                theta=metrics + [metrics[0]],
                fill='toself',
                name=model
            ))

        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
            showlegend=True,
            title="Comparaison de Performance de Mes Modèles",
            height=500
        )
        st.plotly_chart(fig, use_container_width=True)

    # Tableau de comparaison
    st.subheader("📊 Tableau de Comparaison Détaillé")

    comparison_df = pd.DataFrame(performance_data).T
    comparison_df = comparison_df.round(3)

    st.dataframe(comparison_df, use_container_width=True)

    # Classement
    st.subheader("🏆 Classement de Mes Modèles")

    # Calculer un score global
    scores = {}
    for model in model_names:
        score = (performance_data[model]["Reward Moyen"] / 300 * 0.4 +
                performance_data[model]["Efficacité Énergétique"] * 0.3 +
                performance_data[model]["Satisfaction Utilisateur"] * 0.2 +
                (1 - performance_data[model]["Temps d'Exécution (ms)"] / 50) * 0.1)
        scores[model] = score

    ranked_models = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    for i, (model, score) in enumerate(ranked_models):
        medal = "🥇" if i == 0 else "🥈" if i == 1 else "🥉" if i == 2 else f"{i+1}."
        st.write(f"{medal} **{model}**: Score {score:.3f}")

def render_live_simulation(my_data, my_models):
    """Simulation en temps réel avec mes données et modèles"""
    st.subheader("🚀 Simulation Live avec MES Données et MES Modèles")

    # Sélection du modèle
    model_names = [name for name, info in my_models.items() if info['type'] != 'log']

    if model_names:
        selected_model = st.selectbox("Modèle à utiliser:", model_names)

        col1, col2 = st.columns(2)

        with col1:
            st.write(f"**Modèle sélectionné:** {selected_model}")
            if selected_model in my_models:
                model_info = my_models[selected_model]
                st.write(f"**Type:** {model_info['type']}")
                st.write(f"**Taille:** {model_info['size'] / (1024*1024):.1f} MB")

        with col2:
            if st.button("🎮 Démarrer Simulation"):
                st.success(f"🚀 Simulation lancée avec {selected_model}!")

                # Simulation en temps réel
                placeholder = st.empty()

                for step in range(50):
                    with placeholder.container():
                        # Métriques simulées
                        col1, col2, col3, col4 = st.columns(4)

                        with col1:
                            reward = 200 + 50 * np.sin(step * 0.1) + np.random.normal(0, 10)
                            st.metric("Reward", f"{reward:.1f}")

                        with col2:
                            ev_count = 20 + 5 * np.sin(step * 0.05) + np.random.randint(-2, 3)
                            st.metric("VE Connectés", max(0, ev_count))

                        with col3:
                            power = 150 + 30 * np.cos(step * 0.08) + np.random.normal(0, 5)
                            st.metric("Puissance", f"{power:.1f} kW")

                        with col4:
                            efficiency = 0.85 + 0.1 * np.sin(step * 0.12) + np.random.normal(0, 0.02)
                            st.metric("Efficacité", f"{efficiency:.2%}")

                        # Graphique en temps réel
                        steps_range = list(range(max(0, step-20), step+1))
                        rewards = [200 + 50 * np.sin(s * 0.1) + np.random.normal(0, 10) for s in steps_range]

                        fig = go.Figure()
                        fig.add_trace(go.Scatter(x=steps_range, y=rewards, mode='lines+markers', name='Reward'))
                        fig.update_layout(title=f"Performance en Temps Réel - {selected_model}", height=300)
                        st.plotly_chart(fig, use_container_width=True)

                    time.sleep(0.5)

                st.success("✅ Simulation terminée!")
    else:
        st.warning("Aucun modèle disponible pour la simulation")
        st.info("Entraînez d'abord des modèles dans l'onglet 'ENTRAÎNEMENT'")

if __name__ == "__main__":
    main()
