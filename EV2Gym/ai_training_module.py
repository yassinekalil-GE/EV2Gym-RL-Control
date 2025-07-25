#!/usr/bin/env python3
"""
Module d'Entraînement IA pour EV2Gym

Entraîne des modèles d'apprentissage automatique basés sur les données réelles
pour prédire les comportements optimaux de charge des VE.
"""

import pandas as pd
import numpy as np
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import joblib
from pathlib import Path
import json
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class EVChargingPredictor:
    """Prédicteur de charge optimale pour véhicules électriques"""
    
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.feature_names = []
        self.is_trained = False
        
    def prepare_features(self, real_data):
        """Prépare les features à partir des données réelles"""
        features = []
        
        # Features des prix de l'électricité
        if 'electricity_prices' in real_data:
            prices_df = real_data['electricity_prices'].copy()
            prices_df['hour'] = prices_df['Datetime (Local)'].dt.hour
            prices_df['day_of_week'] = prices_df['Datetime (Local)'].dt.dayofweek
            prices_df['month'] = prices_df['Datetime (Local)'].dt.month
            
            # Calculer des features dérivées
            prices_df['price_ma_24h'] = prices_df['Price (EUR/MWhe)'].rolling(24).mean()
            prices_df['price_std_24h'] = prices_df['Price (EUR/MWhe)'].rolling(24).std()
            prices_df['price_trend'] = prices_df['Price (EUR/MWhe)'].diff()
            
            # Supprimer les NaN
            prices_df = prices_df.dropna()
            
            features.append(prices_df[[
                'Price (EUR/MWhe)', 'hour', 'day_of_week', 'month',
                'price_ma_24h', 'price_std_24h', 'price_trend'
            ]])
        
        # Features des charges résidentielles
        if 'residential_loads' in real_data:
            loads_df = real_data['residential_loads']
            
            # Calculer des statistiques par heure
            hourly_stats = []
            for hour in range(24):
                hour_data = loads_df.iloc[:, hour]
                hourly_stats.append({
                    'hour': hour,
                    'avg_load': hour_data.mean(),
                    'std_load': hour_data.std(),
                    'max_load': hour_data.max(),
                    'min_load': hour_data.min()
                })
            
            loads_features = pd.DataFrame(hourly_stats)
            features.append(loads_features)
        
        # Combiner toutes les features
        if features:
            combined_features = features[0]
            for i in range(1, len(features)):
                # Merger sur l'heure si possible
                if 'hour' in combined_features.columns and 'hour' in features[i].columns:
                    combined_features = combined_features.merge(features[i], on='hour', how='inner')
                else:
                    # Sinon, concaténer
                    combined_features = pd.concat([combined_features, features[i]], axis=1)
            
            return combined_features
        
        return pd.DataFrame()
    
    def create_target_variable(self, features_df):
        """Crée la variable cible (charge optimale) basée sur les prix"""
        if 'Price (EUR/MWhe)' in features_df.columns:
            # Stratégie simple: charger quand les prix sont bas
            price_percentile_25 = features_df['Price (EUR/MWhe)'].quantile(0.25)
            price_percentile_75 = features_df['Price (EUR/MWhe)'].quantile(0.75)
            
            # Cible: 1 = charge recommandée, 0 = pas de charge, -1 = décharge (V2G)
            target = np.where(
                features_df['Price (EUR/MWhe)'] <= price_percentile_25, 1,  # Charge
                np.where(
                    features_df['Price (EUR/MWhe)'] >= price_percentile_75, -1,  # Décharge
                    0  # Attendre
                )
            )
            
            return target
        
        return np.zeros(len(features_df))
    
    def train_model(self, real_data, model_type='random_forest'):
        """Entraîne le modèle de prédiction"""
        
        # Préparer les données
        features_df = self.prepare_features(real_data)
        
        if features_df.empty:
            raise ValueError("Impossible de créer des features à partir des données")
        
        # Créer la variable cible
        target = self.create_target_variable(features_df)
        
        # Supprimer les colonnes non numériques
        numeric_features = features_df.select_dtypes(include=[np.number])
        
        # Diviser en train/test
        X_train, X_test, y_train, y_test = train_test_split(
            numeric_features, target, test_size=0.2, random_state=42
        )
        
        # Normaliser les features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Choisir et entraîner le modèle
        if model_type == 'random_forest':
            self.model = RandomForestRegressor(
                n_estimators=100,
                max_depth=10,
                random_state=42,
                n_jobs=-1
            )
        elif model_type == 'gradient_boosting':
            self.model = GradientBoostingRegressor(
                n_estimators=100,
                max_depth=6,
                learning_rate=0.1,
                random_state=42
            )
        
        # Entraîner
        self.model.fit(X_train_scaled, y_train)
        
        # Prédire sur le test set
        y_pred = self.model.predict(X_test_scaled)
        
        # Calculer les métriques
        metrics = {
            'mse': mean_squared_error(y_test, y_pred),
            'mae': mean_absolute_error(y_test, y_pred),
            'r2': r2_score(y_test, y_pred),
            'cv_score': cross_val_score(self.model, X_train_scaled, y_train, cv=5).mean()
        }
        
        self.feature_names = numeric_features.columns.tolist()
        self.is_trained = True
        
        return metrics, X_test, y_test, y_pred
    
    def predict_optimal_charging(self, features):
        """Prédit la stratégie de charge optimale"""
        if not self.is_trained:
            raise ValueError("Le modèle n'est pas encore entraîné")
        
        features_scaled = self.scaler.transform(features)
        prediction = self.model.predict(features_scaled)
        
        return prediction
    
    def get_feature_importance(self):
        """Retourne l'importance des features"""
        if not self.is_trained or not hasattr(self.model, 'feature_importances_'):
            return None
        
        importance_df = pd.DataFrame({
            'feature': self.feature_names,
            'importance': self.model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        return importance_df
    
    def save_model(self, filepath):
        """Sauvegarde le modèle entraîné"""
        if not self.is_trained:
            raise ValueError("Le modèle n'est pas encore entraîné")
        
        model_data = {
            'model': self.model,
            'scaler': self.scaler,
            'feature_names': self.feature_names,
            'timestamp': datetime.now().isoformat()
        }
        
        joblib.dump(model_data, filepath)
    
    def load_model(self, filepath):
        """Charge un modèle pré-entraîné"""
        model_data = joblib.load(filepath)
        
        self.model = model_data['model']
        self.scaler = model_data['scaler']
        self.feature_names = model_data['feature_names']
        self.is_trained = True

def render_ai_training_interface(real_data):
    """Interface Streamlit pour l'entraînement IA"""
    
    st.subheader("🤖 Entraînement de Modèles IA")
    
    if not real_data:
        st.warning("Aucune donnée disponible pour l'entraînement")
        return
    
    # Initialiser le prédicteur
    if 'predictor' not in st.session_state:
        st.session_state.predictor = EVChargingPredictor()
    
    predictor = st.session_state.predictor
    
    # Configuration de l'entraînement
    st.subheader("⚙️ Configuration de l'Entraînement")
    
    col1, col2 = st.columns(2)
    
    with col1:
        model_type = st.selectbox(
            "Type de modèle:",
            ['random_forest', 'gradient_boosting'],
            format_func=lambda x: {
                'random_forest': '🌳 Random Forest',
                'gradient_boosting': '📈 Gradient Boosting'
            }[x]
        )
    
    with col2:
        use_all_data = st.checkbox("Utiliser toutes les données", value=True)
    
    # Bouton d'entraînement
    if st.button("🚀 Démarrer l'Entraînement", type="primary"):
        
        with st.spinner("Entraînement en cours..."):
            try:
                # Entraîner le modèle
                metrics, X_test, y_test, y_pred = predictor.train_model(
                    real_data, model_type
                )
                
                st.success("✅ Entraînement terminé avec succès!")
                
                # Afficher les métriques
                st.subheader("📊 Métriques de Performance")
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("R² Score", f"{metrics['r2']:.3f}")
                with col2:
                    st.metric("MSE", f"{metrics['mse']:.3f}")
                with col3:
                    st.metric("MAE", f"{metrics['mae']:.3f}")
                with col4:
                    st.metric("CV Score", f"{metrics['cv_score']:.3f}")
                
                # Graphique de prédiction vs réalité
                fig = go.Figure()
                
                fig.add_trace(go.Scatter(
                    x=y_test,
                    y=y_pred,
                    mode='markers',
                    name='Prédictions',
                    marker=dict(color='blue', opacity=0.6)
                ))
                
                # Ligne de référence parfaite
                min_val = min(y_test.min(), y_pred.min())
                max_val = max(y_test.max(), y_pred.max())
                fig.add_trace(go.Scatter(
                    x=[min_val, max_val],
                    y=[min_val, max_val],
                    mode='lines',
                    name='Prédiction Parfaite',
                    line=dict(color='red', dash='dash')
                ))
                
                fig.update_layout(
                    title="Prédictions vs Valeurs Réelles",
                    xaxis_title="Valeurs Réelles",
                    yaxis_title="Prédictions",
                    height=400
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Importance des features
                importance_df = predictor.get_feature_importance()
                if importance_df is not None:
                    st.subheader("🎯 Importance des Features")
                    
                    fig_importance = go.Figure()
                    fig_importance.add_trace(go.Bar(
                        x=importance_df['importance'][:10],
                        y=importance_df['feature'][:10],
                        orientation='h',
                        marker_color='green'
                    ))
                    
                    fig_importance.update_layout(
                        title="Top 10 des Features les Plus Importantes",
                        xaxis_title="Importance",
                        height=400
                    )
                    
                    st.plotly_chart(fig_importance, use_container_width=True)
                
                # Sauvegarder le modèle
                if st.button("💾 Sauvegarder le Modèle"):
                    model_path = f"models/ev_charging_model_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pkl"
                    Path("models").mkdir(exist_ok=True)
                    predictor.save_model(model_path)
                    st.success(f"Modèle sauvegardé: {model_path}")
                
            except Exception as e:
                st.error(f"❌ Erreur lors de l'entraînement: {e}")
    
    # Section de prédiction en temps réel
    if predictor.is_trained:
        st.subheader("🔮 Prédiction en Temps Réel")
        
        st.info("Utilisez le modèle entraîné pour prédire la stratégie de charge optimale")
        
        # Interface pour tester des prédictions
        col1, col2 = st.columns(2)
        
        with col1:
            test_price = st.number_input("Prix actuel (€/MWh):", value=50.0, min_value=0.0)
            test_hour = st.slider("Heure:", 0, 23, 12)
        
        with col2:
            test_day = st.slider("Jour de la semaine:", 0, 6, 1)
            test_month = st.slider("Mois:", 1, 12, 6)
        
        if st.button("🎯 Prédire Stratégie"):
            # Créer un échantillon de test
            test_features = pd.DataFrame({
                'Price (EUR/MWhe)': [test_price],
                'hour': [test_hour],
                'day_of_week': [test_day],
                'month': [test_month]
            })
            
            # Ajouter des features manquantes avec des valeurs par défaut
            for feature in predictor.feature_names:
                if feature not in test_features.columns:
                    test_features[feature] = 0.0
            
            # Réorganiser les colonnes
            test_features = test_features[predictor.feature_names]
            
            try:
                prediction = predictor.predict_optimal_charging(test_features)[0]
                
                if prediction > 0.5:
                    st.success("🔋 **Recommandation: CHARGER**")
                    st.write("Les conditions sont favorables pour charger le véhicule")
                elif prediction < -0.5:
                    st.info("⚡ **Recommandation: DÉCHARGER (V2G)**")
                    st.write("Les prix sont élevés, décharger vers le réseau est profitable")
                else:
                    st.warning("⏸️ **Recommandation: ATTENDRE**")
                    st.write("Conditions neutres, attendre un meilleur moment")
                
                st.metric("Score de Prédiction", f"{prediction:.3f}")
                
            except Exception as e:
                st.error(f"Erreur lors de la prédiction: {e}")

def main():
    """Fonction principale pour tester le module"""
    st.title("🤖 Module d'Entraînement IA - EV2Gym")
    
    # Simuler des données pour le test
    test_data = {
        'electricity_prices': pd.DataFrame({
            'Datetime (Local)': pd.date_range('2024-01-01', periods=1000, freq='H'),
            'Price (EUR/MWhe)': np.random.normal(50, 20, 1000)
        })
    }
    
    render_ai_training_interface(test_data)

if __name__ == "__main__":
    main()
