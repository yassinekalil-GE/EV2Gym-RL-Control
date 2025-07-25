# 🚗⚡ EV2Gym - Simulateur de Recharge Intelligente V2G

**EV2Gym** est une plateforme de simulation réaliste, modulaire et hautement personnalisable pour tester et optimiser des stratégies de recharge intelligente de véhicules électriques (VE) dans un contexte Vehicle-to-Grid (V2G).

## 🌟 Caractéristiques Principales

- **🔋 Simulation V2G Réaliste** : Modélisation complète des flux bidirectionnels d'énergie
- **🏗️ Architecture Modulaire** : Composants indépendants (VE, stations, transformateurs)
- **🤖 Compatible RL** : Intégration native avec Gymnasium pour l'apprentissage par renforcement
- **📊 Données Réelles** : Basé sur des données du marché électrique néerlandais
- **⚙️ Hautement Configurable** : Configuration via fichiers YAML
- **📈 Visualisations Avancées** : Outils de rendu et d'analyse intégrés

## 🚀 Installation Rapide

### Prérequis
- Python 3.8+
- pip ou conda

### Installation de Base
```bash
# Cloner le repository
git clone <repository-url>
cd ev2gym

# Installer les dépendances de base
pip install -r requirements.txt

# Installer le package en mode développement
pip install -e .
```

### Installation Complète (avec toutes les fonctionnalités)
```bash
# Installation avec toutes les dépendances optionnelles
pip install -e ".[all]"
```

### Installation par Composants
```bash
# Pour l'optimisation mathématique
pip install -e ".[optimization]"

# Pour l'apprentissage automatique
pip install -e ".[ml]"

# Pour l'interface web
pip install -e ".[web]"

# Pour Jupyter
pip install -e ".[jupyter]"
```

## 🎯 Utilisation Rapide

### 1. Script de Démonstration Simple
```bash
# Simulation basique avec agent intelligent
python tools/demo.py --config V2GProfitMax --agent smart --steps 100

# Simulation avec visualisation
python tools/demo.py --config PublicPST --agent heuristic --visualize --save
```

### 2. Interface CLI Interactive
```bash
# Lancer l'interface interactive
python tools/cli.py

# Mode comparaison d'agents
python tools/cli.py --batch
```

### 3. Interface Web Streamlit
```bash
# Lancer l'interface web
streamlit run tools/web_app.py
```

### 4. Notebook Jupyter
```bash
# Ouvrir le notebook de démonstration
jupyter notebook notebooks/EV2Gym_Demo.ipynb
```

## 📋 Scénarios Disponibles

| Scénario | Description | Fichier Config |
|----------|-------------|----------------|
| **V2GProfitMax** | Maximisation des profits V2G | `V2GProfitMax.yaml` |
| **PublicPST** | Recharge publique avec suivi de consigne | `PublicPST.yaml` |
| **BusinessPST** | Recharge en entreprise | `BusinessPST.yaml` |
| **V2GProfitPlusLoads** | V2G avec charges flexibles | `V2GProfitPlusLoads.yaml` |

## 🤖 Agents de Contrôle

### Agents Simples
- **Random** : Actions aléatoires
- **Fast** : Charge le plus rapidement possible
- **Smart** : Agent intelligent basé sur les prix

### Heuristiques
- **Round Robin** : Distribution équitable
- **ChargeAsFastAsPossible** : Charge maximale
- **ChargeAsLateAsPossible** : Charge différée

### Agents RL (avec Stable-Baselines3)
- **PPO** : Proximal Policy Optimization
- **DDPG** : Deep Deterministic Policy Gradient
- **SAC** : Soft Actor-Critic

## 📊 Analyse des Résultats

### Analyse d'une Simulation
```bash
# Analyser un fichier replay
python tools/analysis.py --replay_path ./replay/simulation.pkl --generate_report

# Comparer plusieurs agents
python tools/analysis.py --compare_agents --config V2GProfitMax --agents random smart heuristic
```

### Métriques Disponibles
- **Économiques** : Profits, coûts, revenus V2G
- **Énergétiques** : Consommation, efficacité, pertes
- **Opérationnelles** : Satisfaction utilisateur, utilisation des ports
- **Contraintes** : Surcharges transformateurs, violations limites

## 🔧 Configuration Personnalisée

### Structure d'un Fichier de Configuration
```yaml
# Paramètres de simulation
timescale: 15  # minutes par étape
simulation_length: 112  # nombre d'étapes

# Réseau de charge
number_of_charging_stations: 25
number_of_transformers: 1
v2g_enabled: true

# Scénario
scenario: workplace  # public, private, workplace
spawn_multiplier: 5

# Paramètres économiques
discharge_price_factor: 1.2

# Charges flexibles et génération
inflexible_loads:
  include: true
  capacity_multiplier_mean: 1.0

solar_power:
  include: true
  capacity_multiplier_mean: 1.0
```

### Fonctions Personnalisées

#### État Personnalisé (`rl_agent/state.py`)
```python
def custom_state_function(env):
    """Définir un espace d'état personnalisé"""
    # Votre logique ici
    return observation_vector
```

#### Récompense Personnalisée (`rl_agent/reward.py`)
```python
def custom_reward_function(env, costs, satisfaction, penalties):
    """Définir une fonction de récompense personnalisée"""
    # Votre logique ici
    return reward_value
```

## 📈 Exemples d'Utilisation

### Exemple 1: Simulation Basique
```python
from ev2gym.models.ev2gym_env import EV2Gym

# Créer l'environnement
env = EV2Gym(config_file="ev2gym/example_config_files/V2GProfitMax.yaml")

# Boucle de simulation
obs, info = env.reset()
for step in range(100):
    action = env.action_space.sample()  # Action aléatoire
    obs, reward, done, truncated, info = env.step(action)
    if done:
        break

print(f"Simulation terminée après {step} étapes")
```

### Exemple 2: Entraînement RL avec Stable-Baselines3
```python
from stable_baselines3 import PPO
from ev2gym.models.ev2gym_env import EV2Gym

# Créer l'environnement
env = EV2Gym(config_file="ev2gym/example_config_files/PublicPST.yaml")

# Créer et entraîner l'agent
model = PPO("MlpPolicy", env, verbose=1)
model.learn(total_timesteps=10000)

# Tester l'agent entraîné
obs, info = env.reset()
for _ in range(100):
    action, _states = model.predict(obs)
    obs, reward, done, truncated, info = env.step(action)
    if done:
        break
```

## 🛠️ Outils Disponibles

| Outil | Description | Commande |
|-------|-------------|----------|
| **demo.py** | Script de démonstration | `python tools/demo.py` |
| **cli.py** | Interface CLI interactive | `python tools/cli.py` |
| **web_app.py** | Interface web Streamlit | `streamlit run tools/web_app.py` |
| **analysis.py** | Outils d'analyse | `python tools/analysis.py` |

## 📚 Documentation Détaillée

### Architecture du Système
- **`models/ev2gym_env.py`** : Environnement principal Gymnasium
- **`models/ev.py`** : Modèle de véhicule électrique
- **`models/ev_charger.py`** : Modèle de station de charge
- **`models/transformer.py`** : Modèle de transformateur
- **`rl_agent/`** : Fonctions d'état et de récompense
- **`baselines/`** : Algorithmes de référence (MPC, heuristiques)
- **`data/`** : Données réelles (prix, profils, spécifications)

### Flux de Simulation
1. **Initialisation** : Chargement config → Création environnement
2. **Reset** : Initialisation état → Spawn initial des VE
3. **Boucle Principale** : Action agent → Step environnement → Mise à jour état
4. **Terminaison** : Conditions d'arrêt → Statistiques finales

## 🤝 Contribution

Les contributions sont les bienvenues ! Veuillez consulter le guide de contribution pour plus de détails.

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 📞 Support

- **Issues** : Utilisez le système d'issues GitHub
- **Documentation** : Consultez les notebooks et exemples
- **Communauté** : Rejoignez les discussions

---

**EV2Gym** - Accélérer la recherche en recharge intelligente de véhicules électriques 🚗⚡
