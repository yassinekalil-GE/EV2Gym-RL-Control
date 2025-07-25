# 🚗⚡ EV2Gym - Advanced Electric Vehicle Grid Integration Platform

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-red.svg)](https://streamlit.io)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)]()

<div align="center">
<img src="https://github.com/StavrosOrf/EV2Gym/assets/17108978/86e921ad-d711-4dbb-b7b9-c69dee20da11" width="55%"/>
</div>

## 📋 Table des Matières

- [🎯 Vue d'Ensemble](#-vue-densemble)
- [✨ Fonctionnalités](#-fonctionnalités)
- [🏗️ Architecture](#️-architecture)
- [🚀 Installation](#-installation)
- [📊 Dashboards Disponibles](#-dashboards-disponibles)
- [🎮 Utilisation](#-utilisation)
- [🤖 Agents Disponibles](#-agents-disponibles)
- [📈 Données et Scénarios](#-données-et-scénarios)
- [🔧 Configuration](#-configuration)
- [📚 Documentation](#-documentation)
- [🤝 Contribution](#-contribution)
- [📄 Licence](#-licence)

## 🎯 Vue d'Ensemble

**EV2Gym** est une plateforme de simulation réaliste, modulaire et hautement personnalisable, conçue pour tester et optimiser des stratégies de recharge intelligente de véhicules électriques (VE) dans un contexte **Vehicle-to-Grid (V2G)**. 

### 🌟 Nouveautés de cette Version

Cette version étend EV2Gym avec des **dashboards interactifs ultra-sophistiqués** qui permettent :

- 🧠 **Agents d'apprentissage par renforcement** (PPO, A2C, SAC, DDPG)
- 🎯 **Contrôle prédictif (MPC)** avec optimisation Gurobi
- ⚡ **Algorithmes heuristiques** pour comparaison
- 📊 **Dashboards interactifs** pour visualisation et contrôle temps réel
- 🌐 **Services auxiliaires** (régulation fréquence, support tension)
- 📈 **Analyse de scénarios** et optimisation économique
- 🔋 **Monitoring SOC et puissance** en temps réel
- ⚡ **Gestion fréquence réseau** et régulation automatique

## ✨ Fonctionnalités

### 🎛️ Simulation Avancée
- **Environnement Gymnasium** compatible avec tous les agents RL
- **Modèles VE réalistes** (Tesla Model 3, BMW i3, Nissan Leaf, Audi e-tron, etc.)
- **Données réelles** : Prix électricité Pays-Bas (2015-2024), spécifications VE 2024
- **Topologie réseau** configurable (transformateurs, stations, ports)
- **Comportements utilisateurs** basés sur données réelles

### 🤖 Agents Intelligents
- **RL** : PPO, A2C, SAC, TD3, DDPG avec Stable Baselines3
- **MPC** : OCMF_V2G, eMPC_V2G, V2GProfitMax avec Gurobi
- **Heuristiques** : ChargeAsFastAsPossible, RoundRobin, RandomAgent
- **Entraînement parallèle** et comparaison de performance

### 📊 Dashboards Interactifs Ultra-Sophistiqués
- **🚗⚡ Dashboard Principal** : Vue d'ensemble et contrôle complet
- **🔋 Power & SOC** : Puissance et état de charge détaillés avec modes V2G/G2V
- **⚡ Advanced Grid** : Fréquence réseau, tension triphasée, courant bornes
- **📤 Upload Data** : Interface d'import de données personnelles
- **📈 Analyse Comparative** : Performance multi-agents avec graphiques radar

### ⚡ Services Auxiliaires Avancés
- **Régulation de fréquence** (±0.1 Hz) avec réponse automatique
- **Support de tension** (±2%) triphasé
- **Réserve tournante** et suivi de charge
- **Écrêtage des pics** et équilibrage intelligent
- **Intégration renouvelables** optimisée

## 🏗️ Architecture

```
EV2Gym/
├── 📁 ev2gym/                    # Core EV2Gym Original
│   ├── 📁 models/                # Environnement et modèles
│   │   ├── ev2gym_env.py         # Environnement principal Gymnasium
│   │   ├── ev.py                 # Modèle véhicule électrique
│   │   ├── charging_station.py   # Modèle station de charge
│   │   └── transformer.py        # Modèle transformateur
│   ├── 📁 baselines/             # Agents de référence
│   │   ├── 📁 heuristics/        # Agents heuristiques
│   │   └── 📁 mpc/               # Agents MPC (Gurobi)
│   ├── 📁 rl_agent/              # Agents RL
│   │   ├── state.py              # Définition des états
│   │   └── reward.py             # Fonctions de récompense
│   ├── 📁 data/                  # Données réelles
│   │   ├── Netherlands_day-ahead-2015-2024.csv
│   │   ├── ev_specs_v2g_enabled2024.json
│   │   └── residential_loads.csv
│   └── 📁 example_config_files/  # Configurations YAML
├── 📊 DASHBOARDS ULTRA-SOPHISTIQUÉS
│   ├── my_data_dashboard.py      # 🚗⚡ Dashboard Principal
│   ├── ev_power_soc_dashboard.py # 🔋 Power & SOC Avancé
│   ├── advanced_grid_dashboard.py# ⚡ Grid Ultra-Complet
│   ├── upload_data_dashboard.py  # 📤 Upload Interface
│   └── ultimate_ev2gym_dashboard.py # 🎯 Dashboard Ultimate
├── 📁 models/                    # Modèles entraînés
├── 📁 logs/                      # Logs d'entraînement
├── train_stable_baselines.py     # Script d'entraînement
├── install_gurobi.py             # Installation Gurobi automatique
└── README.md                     # Ce fichier
```

## 🚀 Installation

### Prérequis
- Python 3.8+
- Git

### Installation Rapide

```bash
# Cloner le repository
git clone https://github.com/StavrosOrf/EV2Gym.git
cd EV2Gym

# Installer les dépendances de base
pip install streamlit pandas numpy plotly scikit-learn
pip install stable-baselines3 gymnasium

# Installer Gurobi (optionnel, pour agents MPC optimaux)
python install_gurobi.py

# Lancer le dashboard principal
streamlit run my_data_dashboard.py --server.port=8504
```

### Installation Complète avec Environnement Virtuel

```bash
# Créer environnement virtuel
python -m venv ev2gym_env
source ev2gym_env/bin/activate  # Linux/Mac
# ou
ev2gym_env\Scripts\activate     # Windows

# Installation complète
pip install -r requirements.txt
pip install gurobipy  # Pour agents MPC optimaux

# Vérification
python -c "import ev2gym; print('EV2Gym installé avec succès!')"
```

## 📊 Dashboards Disponibles

### 1. 🚗⚡ Dashboard Principal (`port 8504`)
```bash
streamlit run my_data_dashboard.py --server.port=8504
```
**Fonctionnalités :**
- **Vue d'ensemble** complète du système EV2Gym
- **Données réelles** exploitées automatiquement (prix, VE, charges)
- **Modèles entraînés** détectés et analysés
- **Interface d'entraînement** intégrée avec configuration
- **Simulation live** avec vos modèles

### 2. 🔋 Power & SOC Dashboard (`port 8506`)
```bash
streamlit run ev_power_soc_dashboard.py --server.port=8506
```
**Fonctionnalités :**
- **SOC détaillé** par véhicule avec alertes automatiques
- **Puissance temps réel** V2G/G2V avec graphiques colorés
- **Modes de fonctionnement** (Idle, Charge, Décharge) en temps réel
- **Analyse économique** avec revenus V2G calculés
- **20 modèles VE réalistes** (Tesla, BMW, Nissan, Audi, etc.)

### 3. ⚡ Advanced Grid Dashboard (`port 8507`)
```bash
streamlit run advanced_grid_dashboard.py --server.port=8507
```
**Fonctionnalités Ultra-Avancées :**
- **Fréquence réseau** (49.0-51.0 Hz) avec régulation automatique
- **Tensions triphasées** (L1, L2, L3) avec monitoring
- **Courant par borne** avec limites et alertes
- **6 scénarios complets** (Normal, Forte demande, Urgence, etc.)
- **Services auxiliaires** avec calcul de revenus
- **Capacités VE détaillées** (batterie, AC, DC, V2G)

### 4. 📤 Upload Data Dashboard (`port 8505`)
```bash
streamlit run upload_data_dashboard.py --server.port=8505
```
**Fonctionnalités :**
- **Upload données** personnelles (.csv, .json, .xlsx)
- **Upload modèles** (.zip, .pkl, .pth) avec métadonnées
- **Conversion automatique** vers format EV2Gym
- **Gestion fichiers** complète avec prévisualisation

## 🎮 Utilisation

### Démarrage Ultra-Rapide

1. **Lancer le dashboard principal** :
```bash
streamlit run my_data_dashboard.py --server.port=8504
```

2. **Ouvrir dans le navigateur** : http://localhost:8504

3. **Explorer les onglets** :
   - 📊 **MES DONNÉES** : Visualiser vos données réelles
   - 🤖 **MES MODÈLES** : Voir vos modèles entraînés
   - 🎯 **ENTRAÎNEMENT** : Lancer de nouveaux entraînements
   - 📈 **ANALYSE COMPARATIVE** : Comparer les performances
   - 🚀 **SIMULATION LIVE** : Tester en temps réel

### Entraînement d'Agents

```bash
# Entraîner un agent PPO avec configuration V2G
python train_stable_baselines.py \
    --algorithm ppo \
    --train_steps 20000 \
    --config_file ev2gym/example_config_files/V2GProfitPlusLoads.yaml \
    --device cuda:0 \
    --run_name ppo_v2g_experiment

# Entraîner plusieurs agents en parallèle
python train_stable_baselines.py --algorithm a2c --train_steps 15000
python train_stable_baselines.py --algorithm sac --train_steps 25000
```

### Utilisation Programmatique Avancée

```python
from ev2gym.models.ev2gym_env import EV2Gym
from ev2gym.baselines.heuristics import ChargeAsFastAsPossible
from ev2gym.baselines.mpc.V2GProfitMax import V2GProfitMaxOracle

# Créer l'environnement avec configuration V2G
env = EV2Gym(config_file="ev2gym/example_config_files/V2GProfitPlusLoads.yaml")

# Utiliser un agent heuristique
agent = ChargeAsFastAsPossible()

# Ou un agent MPC optimal (nécessite Gurobi)
# agent = V2GProfitMaxOracle()

# Simulation avec monitoring
for step in range(1000):
    actions = agent.get_action(env)
    obs, reward, done, truncated, info = env.step(actions)
    
    # Monitoring avancé
    if step % 100 == 0:
        print(f"Step {step}: Reward={reward:.2f}, EVs={len(env.evs)}")
    
    if done or truncated:
        break

print(f"Simulation terminée après {step} étapes")
print(f"Récompense totale: {env.total_reward:.2f}")
```

## 🤖 Agents Disponibles

### 🧠 Agents RL (Apprentissage par Renforcement)
| Agent | Description | Avantages | Inconvénients | Performance |
|-------|-------------|-----------|---------------|-------------|
| **PPO** | Proximal Policy Optimization | Stable, performant | Temps d'entraînement | ⭐⭐⭐⭐⭐ |
| **A2C** | Advantage Actor-Critic | Rapide à entraîner | Moins stable | ⭐⭐⭐⭐ |
| **SAC** | Soft Actor-Critic | Très performant | Complexe | ⭐⭐⭐⭐⭐ |
| **TD3** | Twin Delayed DDPG | Bon pour contrôle continu | Sensible hyperparamètres | ⭐⭐⭐⭐ |

### 🎯 Agents MPC (Model Predictive Control)
| Agent | Description | Optimisation | Gurobi Requis | Performance |
|-------|-------------|--------------|---------------|-------------|
| **OCMF_V2G** | Optimal Charging Management | Charge/décharge optimale | ✅ | ⭐⭐⭐⭐⭐ |
| **eMPC_V2G** | Economic MPC | Profit économique | ✅ | ⭐⭐⭐⭐⭐ |
| **V2GProfitMax** | Oracle optimal | Solution mathématique | ✅ | ⭐⭐⭐⭐⭐ |

### ⚡ Agents Heuristiques
| Agent | Description | Temps d'exécution | Performance | Utilité |
|-------|-------------|-------------------|-------------|---------|
| **ChargeAsFastAsPossible** | Charge maximale | < 1ms | ⭐⭐⭐ | Baseline |
| **RoundRobin** | Rotation équitable | < 1ms | ⭐⭐⭐ | Équitable |
| **RandomAgent** | Actions aléatoires | < 1ms | ⭐ | Référence |

## 📈 Données et Scénarios

### 📊 Données Réelles Incluses

- **Prix électricité** : Pays-Bas 2015-2024 (100k+ points historiques)
- **Spécifications VE** : 50+ modèles 2024 avec capacités V2G détaillées
- **Charges résidentielles** : Profils réels 24h avec variations saisonnières
- **Génération PV** : Données solaires Pays-Bas avec météo
- **Comportements utilisateurs** : Arrivées, demandes, temps de connexion réels

### 🎭 Scénarios de Test Avancés

| Scénario | Fréquence (Hz) | Tension (V) | Charge | Description |
|----------|----------------|-------------|--------|-------------|
| **Normal** | 49.9 - 50.1 | 225 - 235 | 1.0x | Fonctionnement standard |
| **Forte Demande** | 49.7 - 49.9 | 220 - 230 | 1.5x | Pic de consommation |
| **Faible Demande** | 50.1 - 50.3 | 235 - 245 | 0.5x | Faible consommation |
| **Défaut Réseau** | 49.5 - 49.8 | 210 - 225 | 1.2x | Défaut réseau |
| **Pic Renouvelable** | 50.2 - 50.4 | 240 - 250 | 0.3x | Forte production PV/éolien |
| **Urgence** | 49.2 - 49.5 | 200 - 220 | 1.8x | Situation d'urgence |

## 🔧 Configuration

### Fichiers de Configuration YAML

```yaml
# Exemple : V2GProfitPlusLoads.yaml
simulation:
  simulation_length: 1440  # 24h en minutes
  timescale: 1            # 1 minute par pas
  random_seed: 42

network:
  number_of_transformers: 2
  number_of_charging_stations: 25
  charging_stations_per_transformer: 12
  voltage_levels: [230, 400, 800]  # V

ev_specifications:
  ev_specs_file: "ev_specs_v2g_enabled2024.json"
  spawn_rate: 2.0
  v2g_enabled: true
  max_charging_power: 22  # kW

pricing:
  electricity_prices_file: "Netherlands_day-ahead-2015-2024.csv"
  v2g_price_multiplier: 1.1
  ancillary_services_enabled: true

loads:
  residential_loads_file: "residential_loads.csv"
  pv_generation_file: "pv_netherlands.csv"
  load_balancing_enabled: true

grid_services:
  frequency_regulation: true
  voltage_support: true
  peak_shaving: true
  spinning_reserve: true
```

## 📚 Documentation

### 📊 Métriques de Performance Avancées

| Métrique | Description | Unité | Objectif |
|----------|-------------|-------|----------|
| **Reward** | Récompense cumulée | Points | Maximiser |
| **Efficacité Énergétique** | Énergie utile / Énergie totale | % | > 90% |
| **Satisfaction Utilisateur** | Besoins satisfaits / Besoins totaux | % | > 85% |
| **Stabilité Réseau** | Déviations fréquence/tension | Index | > 0.95 |
| **Revenus V2G** | Gains par services auxiliaires | €/jour | Maximiser |
| **Utilisation V2G** | Capacité V2G utilisée | % | 60-80% |

### 🔗 API Reference Complète

```python
# Environnement principal
class EV2Gym(gymnasium.Env):
    def __init__(self, config_file: str, save_replay: bool = False)
    def step(self, actions: np.ndarray) -> Tuple[np.ndarray, float, bool, bool, dict]
    def reset(self) -> Tuple[np.ndarray, dict]
    def render(self, mode: str = "human")
    def get_grid_state(self) -> dict
    def get_ev_states(self) -> List[dict]

# Agent interface
class BaseAgent:
    def get_action(self, env: EV2Gym) -> np.ndarray
    def train(self, env: EV2Gym, steps: int)
    def save(self, path: str)
    def load(self, path: str)
    def evaluate(self, env: EV2Gym, episodes: int) -> dict
```

## 🤝 Contribution

Nous accueillons les contributions ! Voici comment participer :

### 🔧 Développement

```bash
# Fork et clone
git clone https://github.com/StavrosOrf/EV2Gym.git
cd EV2Gym

# Créer une branche
git checkout -b feature/nouvelle-fonctionnalite

# Développer et tester
python -m pytest tests/

# Commit et push
git commit -m "Ajouter nouvelle fonctionnalité"
git push origin feature/nouvelle-fonctionnalite
```

### 📝 Types de Contributions Recherchées

- 🐛 **Bug fixes** : Corrections de bugs
- ✨ **Nouvelles fonctionnalités** : Agents, dashboards, métriques
- 📚 **Documentation** : Guides, exemples, API
- 🧪 **Tests** : Tests unitaires, intégration
- 🎨 **Interface** : Améliorations UI/UX dashboards

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

## 🙏 Remerciements

- **Stable Baselines3** pour les algorithmes RL
- **Gurobi** pour l'optimisation MPC
- **Streamlit** pour les dashboards interactifs
- **Plotly** pour les visualisations avancées
- **Gymnasium** pour l'interface d'environnement

## 📞 Contact

- **GitHub** : [EV2Gym Repository](https://github.com/StavrosOrf/EV2Gym)
- **Paper Original** : [EV2Gym Paper](https://arxiv.org/abs/2404.01849)
- **MPC Paper** : [MPC Algorithms](https://arxiv.org/abs/2405.11963)

---

<div align="center">

**🚗⚡ EV2Gym - Powering the Future of Electric Vehicle Grid Integration**

*Avec Dashboards Ultra-Sophistiqués pour Visualisation et Contrôle Temps Réel*

[![GitHub stars](https://img.shields.io/github/stars/StavrosOrf/EV2Gym.svg?style=social&label=Star)](https://github.com/StavrosOrf/EV2Gym)
[![GitHub forks](https://img.shields.io/github/forks/StavrosOrf/EV2Gym.svg?style=social&label=Fork)](https://github.com/StavrosOrf/EV2Gym/fork)

</div>
