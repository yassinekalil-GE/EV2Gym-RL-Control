#!/usr/bin/env python3
"""
🚗⚡ UPLOAD DATA Dashboard

Interface pour uploader et gérer vos propres données EV2Gym
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import json
import yaml
import os
import sys
from pathlib import Path
from datetime import datetime
import zipfile
import pickle
import warnings
warnings.filterwarnings('ignore')

# Configuration de la page
st.set_page_config(
    page_title="🚗⚡ Upload Data EV2Gym",
    page_icon="📤",
    layout="wide",
    initial_sidebar_state="expanded"
)

def create_data_directories():
    """Crée les répertoires nécessaires"""
    directories = [
        "ev2gym/data",
        "models",
        "logs",
        "uploads",
        "exports"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)

def main():
    """Fonction principale"""
    
    st.title("📤 UPLOAD DATA - EV2Gym")
    st.markdown("**Interface pour uploader et gérer vos données personnelles**")
    
    # Créer les répertoires
    create_data_directories()
    
    # Interface principale
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📤 UPLOAD DONNÉES",
        "🤖 UPLOAD MODÈLES", 
        "📊 DONNÉES UPLOADÉES",
        "🔄 CONVERSION",
        "📋 GESTION FICHIERS"
    ])
    
    with tab1:
        render_data_upload()
    
    with tab2:
        render_model_upload()
    
    with tab3:
        render_uploaded_data_view()
    
    with tab4:
        render_data_conversion()
    
    with tab5:
        render_file_management()

def render_data_upload():
    """Interface d'upload de données"""
    st.subheader("📤 Upload de Vos Données")
    
    # Types de données supportés
    st.subheader("📋 Types de Données Supportés")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**📊 Données de Prix:**")
        st.write("- Prix de l'électricité (.csv)")
        st.write("- Tarifs dynamiques")
        st.write("- Coûts de réseau")
        
        st.write("**🚗 Données VE:**")
        st.write("- Spécifications véhicules (.json)")
        st.write("- Profils de charge")
        st.write("- Capacités V2G")
    
    with col2:
        st.write("**🏠 Données Réseau:**")
        st.write("- Charges résidentielles (.csv)")
        st.write("- Génération PV")
        st.write("- Profils de demande")
        
        st.write("**📈 Données Comportementales:**")
        st.write("- Distributions d'arrivée")
        st.write("- Temps de connexion")
        st.write("- Patterns d'usage")
    
    # Upload de fichiers
    st.subheader("📁 Upload de Fichiers")
    
    # Sélection du type de données
    data_type = st.selectbox("Type de données:", [
        "Prix électricité",
        "Spécifications VE", 
        "Charges résidentielles",
        "Génération PV",
        "Distribution arrivée",
        "Temps connexion",
        "Demande énergétique",
        "Autre"
    ])
    
    # Upload multiple
    uploaded_files = st.file_uploader(
        "Choisissez vos fichiers:",
        accept_multiple_files=True,
        type=['csv', 'json', 'xlsx', 'npy', 'pkl']
    )
    
    if uploaded_files:
        st.success(f"✅ {len(uploaded_files)} fichier(s) sélectionné(s)")
        
        for uploaded_file in uploaded_files:
            st.write(f"**📄 {uploaded_file.name}**")
            st.write(f"- Taille: {uploaded_file.size / 1024:.1f} KB")
            st.write(f"- Type: {uploaded_file.type}")
            
            # Prévisualisation
            if st.button(f"👁️ Prévisualiser {uploaded_file.name}"):
                try:
                    if uploaded_file.name.endswith('.csv'):
                        df = pd.read_csv(uploaded_file)
                        st.write(f"**Dimensions:** {df.shape}")
                        st.write(f"**Colonnes:** {list(df.columns)}")
                        st.dataframe(df.head(), use_container_width=True)
                        
                    elif uploaded_file.name.endswith('.json'):
                        data = json.load(uploaded_file)
                        st.write(f"**Type:** {type(data)}")
                        if isinstance(data, dict):
                            st.write(f"**Clés:** {list(data.keys())[:10]}")
                        st.json(data if len(str(data)) < 1000 else str(data)[:1000] + "...")
                        
                    elif uploaded_file.name.endswith('.xlsx'):
                        df = pd.read_excel(uploaded_file)
                        st.write(f"**Dimensions:** {df.shape}")
                        st.dataframe(df.head(), use_container_width=True)
                        
                except Exception as e:
                    st.error(f"Erreur prévisualisation: {e}")
        
        # Sauvegarde
        if st.button("💾 Sauvegarder Tous les Fichiers", type="primary"):
            saved_files = []
            
            for uploaded_file in uploaded_files:
                try:
                    # Déterminer le répertoire de destination
                    if data_type == "Prix électricité":
                        save_path = Path("ev2gym/data") / f"prices_{uploaded_file.name}"
                    elif data_type == "Spécifications VE":
                        save_path = Path("ev2gym/data") / f"ev_specs_{uploaded_file.name}"
                    elif data_type == "Charges résidentielles":
                        save_path = Path("ev2gym/data") / f"loads_{uploaded_file.name}"
                    else:
                        save_path = Path("uploads") / uploaded_file.name
                    
                    # Sauvegarder
                    with open(save_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    
                    saved_files.append(str(save_path))
                    
                except Exception as e:
                    st.error(f"Erreur sauvegarde {uploaded_file.name}: {e}")
            
            if saved_files:
                st.success(f"✅ {len(saved_files)} fichier(s) sauvegardé(s)!")
                for file_path in saved_files:
                    st.write(f"📁 {file_path}")
                
                st.balloons()

def render_model_upload():
    """Interface d'upload de modèles"""
    st.subheader("🤖 Upload de Vos Modèles")
    
    # Types de modèles
    st.subheader("🎯 Types de Modèles Supportés")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**🧠 Modèles RL:**")
        st.write("- Stable Baselines3 (.zip)")
        st.write("- PyTorch (.pth)")
        st.write("- TensorFlow (.h5)")
        
        st.write("**🎯 Modèles MPC:**")
        st.write("- Paramètres optimisés (.json)")
        st.write("- Matrices de contrôle (.npy)")
    
    with col2:
        st.write("**⚡ Modèles Heuristiques:**")
        st.write("- Règles personnalisées (.py)")
        st.write("- Paramètres (.yaml)")
        
        st.write("**📊 Modèles ML:**")
        st.write("- Scikit-learn (.pkl)")
        st.write("- XGBoost (.model)")
    
    # Upload de modèles
    model_type = st.selectbox("Type de modèle:", [
        "Stable Baselines3 (RL)",
        "PyTorch",
        "TensorFlow", 
        "Scikit-learn",
        "MPC Parameters",
        "Heuristique",
        "Autre"
    ])
    
    uploaded_models = st.file_uploader(
        "Choisissez vos modèles:",
        accept_multiple_files=True,
        type=['zip', 'pth', 'h5', 'pkl', 'json', 'npy', 'yaml', 'py']
    )
    
    if uploaded_models:
        st.success(f"✅ {len(uploaded_models)} modèle(s) sélectionné(s)")
        
        for model_file in uploaded_models:
            st.write(f"**🤖 {model_file.name}**")
            st.write(f"- Taille: {model_file.size / (1024*1024):.1f} MB")
            
            # Métadonnées du modèle
            with st.expander(f"⚙️ Métadonnées - {model_file.name}"):
                model_name = st.text_input(f"Nom du modèle:", model_file.name.split('.')[0])
                algorithm = st.text_input(f"Algorithme:", "PPO")
                training_steps = st.number_input(f"Étapes d'entraînement:", value=20000)
                performance = st.number_input(f"Performance (reward):", value=0.0)
                description = st.text_area(f"Description:", "")
                
                metadata = {
                    "name": model_name,
                    "algorithm": algorithm,
                    "training_steps": training_steps,
                    "performance": performance,
                    "description": description,
                    "upload_date": datetime.now().isoformat(),
                    "file_size": model_file.size,
                    "file_type": model_file.type
                }
        
        if st.button("💾 Sauvegarder Modèles", type="primary"):
            saved_models = []
            
            for model_file in uploaded_models:
                try:
                    # Sauvegarder le modèle
                    model_path = Path("models") / model_file.name
                    with open(model_path, "wb") as f:
                        f.write(model_file.getbuffer())
                    
                    # Sauvegarder les métadonnées
                    metadata_path = Path("models") / f"{model_file.name}.metadata.json"
                    with open(metadata_path, "w") as f:
                        json.dump(metadata, f, indent=2)
                    
                    saved_models.append(str(model_path))
                    
                except Exception as e:
                    st.error(f"Erreur sauvegarde {model_file.name}: {e}")
            
            if saved_models:
                st.success(f"✅ {len(saved_models)} modèle(s) sauvegardé(s)!")
                st.balloons()

def render_uploaded_data_view():
    """Vue des données uploadées"""
    st.subheader("📊 Vos Données Uploadées")
    
    # Scanner les répertoires
    data_files = []
    
    # Données dans ev2gym/data
    data_path = Path("ev2gym/data")
    if data_path.exists():
        for file_path in data_path.glob("*"):
            if file_path.is_file():
                data_files.append({
                    "Nom": file_path.name,
                    "Chemin": str(file_path),
                    "Taille": f"{file_path.stat().st_size / 1024:.1f} KB",
                    "Modifié": datetime.fromtimestamp(file_path.stat().st_mtime).strftime("%Y-%m-%d %H:%M"),
                    "Type": "Données"
                })
    
    # Données dans uploads
    uploads_path = Path("uploads")
    if uploads_path.exists():
        for file_path in uploads_path.glob("*"):
            if file_path.is_file():
                data_files.append({
                    "Nom": file_path.name,
                    "Chemin": str(file_path),
                    "Taille": f"{file_path.stat().st_size / 1024:.1f} KB",
                    "Modifié": datetime.fromtimestamp(file_path.stat().st_mtime).strftime("%Y-%m-%d %H:%M"),
                    "Type": "Upload"
                })
    
    # Modèles
    models_path = Path("models")
    if models_path.exists():
        for file_path in models_path.glob("*"):
            if file_path.is_file() and not file_path.name.endswith('.metadata.json'):
                data_files.append({
                    "Nom": file_path.name,
                    "Chemin": str(file_path),
                    "Taille": f"{file_path.stat().st_size / (1024*1024):.1f} MB",
                    "Modifié": datetime.fromtimestamp(file_path.stat().st_mtime).strftime("%Y-%m-%d %H:%M"),
                    "Type": "Modèle"
                })
    
    if data_files:
        # Statistiques
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_files = len(data_files)
            st.metric("Fichiers Total", total_files)
        
        with col2:
            data_count = len([f for f in data_files if f["Type"] == "Données"])
            st.metric("Fichiers Données", data_count)
        
        with col3:
            model_count = len([f for f in data_files if f["Type"] == "Modèle"])
            st.metric("Modèles", model_count)
        
        with col4:
            upload_count = len([f for f in data_files if f["Type"] == "Upload"])
            st.metric("Uploads", upload_count)
        
        # Tableau des fichiers
        files_df = pd.DataFrame(data_files)
        st.dataframe(files_df, use_container_width=True)
        
        # Actions sur les fichiers
        st.subheader("🔧 Actions sur les Fichiers")
        
        selected_file = st.selectbox("Sélectionner un fichier:", [f["Nom"] for f in data_files])
        
        if selected_file:
            file_info = next(f for f in data_files if f["Nom"] == selected_file)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("👁️ Prévisualiser"):
                    try:
                        file_path = Path(file_info["Chemin"])
                        
                        if file_path.suffix == '.csv':
                            df = pd.read_csv(file_path)
                            st.write(f"**Dimensions:** {df.shape}")
                            st.dataframe(df.head(10), use_container_width=True)
                            
                        elif file_path.suffix == '.json':
                            with open(file_path, 'r') as f:
                                data = json.load(f)
                            st.json(data if len(str(data)) < 1000 else str(data)[:1000] + "...")
                            
                    except Exception as e:
                        st.error(f"Erreur prévisualisation: {e}")
            
            with col2:
                if st.button("📥 Télécharger"):
                    try:
                        with open(file_info["Chemin"], "rb") as f:
                            st.download_button(
                                label=f"Télécharger {selected_file}",
                                data=f.read(),
                                file_name=selected_file,
                                mime="application/octet-stream"
                            )
                    except Exception as e:
                        st.error(f"Erreur téléchargement: {e}")
            
            with col3:
                if st.button("🗑️ Supprimer", type="secondary"):
                    try:
                        os.remove(file_info["Chemin"])
                        st.success(f"✅ {selected_file} supprimé!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Erreur suppression: {e}")
    
    else:
        st.info("Aucun fichier uploadé. Utilisez l'onglet 'UPLOAD DONNÉES' pour commencer.")

def render_data_conversion():
    """Interface de conversion de données"""
    st.subheader("🔄 Conversion de Données")
    
    st.write("Convertissez vos données vers les formats EV2Gym")
    
    # Conversion CSV vers format EV2Gym
    st.subheader("📊 Conversion Prix Électricité")
    
    uploaded_price_file = st.file_uploader("Fichier de prix (.csv, .xlsx):", type=['csv', 'xlsx'])
    
    if uploaded_price_file:
        try:
            if uploaded_price_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_price_file)
            else:
                df = pd.read_excel(uploaded_price_file)
            
            st.write("**Aperçu des données:**")
            st.dataframe(df.head(), use_container_width=True)
            
            # Mapping des colonnes
            st.subheader("🔗 Mapping des Colonnes")
            
            col1, col2 = st.columns(2)
            
            with col1:
                date_col = st.selectbox("Colonne Date/Heure:", df.columns)
                price_col = st.selectbox("Colonne Prix:", df.columns)
            
            with col2:
                date_format = st.text_input("Format Date:", "%Y-%m-%d %H:%M:%S")
                price_unit = st.selectbox("Unité Prix:", ["EUR/MWh", "EUR/kWh", "cents/kWh"])
            
            if st.button("🔄 Convertir"):
                try:
                    # Conversion
                    converted_df = pd.DataFrame()
                    converted_df['Datetime (Local)'] = pd.to_datetime(df[date_col], format=date_format)
                    
                    # Conversion d'unité si nécessaire
                    if price_unit == "EUR/kWh":
                        converted_df['Price (EUR/MWhe)'] = df[price_col] * 1000
                    elif price_unit == "cents/kWh":
                        converted_df['Price (EUR/MWhe)'] = df[price_col] * 10
                    else:
                        converted_df['Price (EUR/MWhe)'] = df[price_col]
                    
                    st.success("✅ Conversion réussie!")
                    st.dataframe(converted_df.head(), use_container_width=True)
                    
                    # Sauvegarder
                    if st.button("💾 Sauvegarder Format EV2Gym"):
                        output_path = Path("ev2gym/data") / "converted_prices.csv"
                        converted_df.to_csv(output_path, index=False)
                        st.success(f"✅ Sauvegardé: {output_path}")
                
                except Exception as e:
                    st.error(f"Erreur conversion: {e}")
        
        except Exception as e:
            st.error(f"Erreur lecture fichier: {e}")

def render_file_management():
    """Gestion des fichiers"""
    st.subheader("📋 Gestion des Fichiers")
    
    # Nettoyage
    st.subheader("🧹 Nettoyage")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🗑️ Nettoyer Uploads"):
            uploads_path = Path("uploads")
            if uploads_path.exists():
                for file_path in uploads_path.glob("*"):
                    if file_path.is_file():
                        file_path.unlink()
                st.success("✅ Dossier uploads nettoyé!")
    
    with col2:
        if st.button("🗑️ Nettoyer Logs"):
            logs_path = Path("logs")
            if logs_path.exists():
                for file_path in logs_path.glob("*.log"):
                    file_path.unlink()
                st.success("✅ Logs nettoyés!")
    
    # Export
    st.subheader("📦 Export")
    
    if st.button("📦 Créer Archive Complète"):
        try:
            archive_path = Path("exports") / f"ev2gym_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
            
            with zipfile.ZipFile(archive_path, 'w') as zipf:
                # Ajouter les données
                for file_path in Path("ev2gym/data").glob("*"):
                    if file_path.is_file():
                        zipf.write(file_path, f"data/{file_path.name}")
                
                # Ajouter les modèles
                for file_path in Path("models").glob("*"):
                    if file_path.is_file():
                        zipf.write(file_path, f"models/{file_path.name}")
            
            st.success(f"✅ Archive créée: {archive_path}")
            
            with open(archive_path, "rb") as f:
                st.download_button(
                    label="📥 Télécharger Archive",
                    data=f.read(),
                    file_name=archive_path.name,
                    mime="application/zip"
                )
        
        except Exception as e:
            st.error(f"Erreur création archive: {e}")

if __name__ == "__main__":
    main()
