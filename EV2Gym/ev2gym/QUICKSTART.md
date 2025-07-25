# 🚀 EV2Gym - Guide de Démarrage Rapide

Ce guide vous permet de commencer à utiliser EV2Gym en quelques minutes.

## ⚡ Installation Express

### 1. Installation Automatique
```bash
# Cloner le projet
git clone <repository-url>
cd ev2gym

# Installation automatique
python install.py
```

### 2. Installation Manuelle
```bash
# Installer les dépendances
pip install -r requirements.txt

# Installer EV2Gym
pip install -e .
```

## 🎯 Premier Test

### Test Rapide
```bash
# Tester l'installation
python run_ev2gym.py test

# Première simulation
python run_ev2gym.py demo --config V2GProfitMax --agent smart --steps 50
```

## 🛠️ Interfaces Disponibles

### 1. 🎮 Script de Démonstration
```bash
# Simulation basique
python run_ev2gym.py demo

# Avec paramètres personnalisés
python run_ev2gym.py demo --config PublicPST --agent heuristic --visualize
```

### 2. 💻 Interface CLI Interactive
```bash
# Interface interactive
python run_ev2gym.py cli

# Mode comparaison d'agents
python run_ev2gym.py cli --batch
```

### 3. 🌐 Interface Web
```bash
# Lancer l'interface web (nécessite Streamlit)
python run_ev2gym.py web
```

### 4. 📓 Notebook Jupyter
```bash
# Ouvrir le notebook de démonstration
python run_ev2gym.py notebook
```

## 📊 Analyse des Résultats

### Comparer des Agents
```bash
# Comparaison automatique
python run_ev2gym.py analyze --compare_agents --config V2GProfitMax

# Avec agents spécifiques
python run_ev2gym.py analyze --compare_agents --agents random smart heuristic
```

### Analyser un Replay
```bash
# Analyser un fichier de simulation sauvegardé
python run_ev2gym.py analyze --replay_path ./replay/simulation.pkl --generate_report
```

## 🔧 Configuration Rapide

### Scénarios Prêts à l'Emploi

| Commande | Description |
|----------|-------------|
| `--config V2GProfitMax` | Maximisation profits V2G |
| `--config PublicPST` | Recharge publique |
| `--config BusinessPST` | Recharge entreprise |
| `--config V2GProfitPlusLoads` | V2G + charges flexibles |

### Agents Disponibles

| Agent | Description |
|-------|-------------|
| `random` | Actions aléatoires |
| `fast` | Charge le plus vite possible |
| `smart` | Agent intelligent basé sur les prix |
| `heuristic` | Stratégie Round Robin |

## 📈 Exemples d'Utilisation

### Exemple 1: Simulation Rapide
```bash
python run_ev2gym.py demo --config V2GProfitMax --agent smart --steps 100 --save
```

### Exemple 2: Comparaison d'Agents
```bash
python run_ev2gym.py analyze --compare_agents --config PublicPST
```

### Exemple 3: Interface Web
```bash
python run_ev2gym.py web
# Puis ouvrir http://localhost:8501 dans votre navigateur
```

## 🐍 Utilisation en Python

### Script Minimal
```python
from ev2gym.models.ev2gym_env import EV2Gym

# Créer l'environnement
env = EV2Gym(config_file="ev2gym/example_config_files/V2GProfitMax.yaml")

# Simulation simple
obs, info = env.reset()
for step in range(50):
    action = env.action_space.sample()  # Action aléatoire
    obs, reward, done, truncated, info = env.step(action)
    print(f"Étape {step}: Récompense = {reward:.2f}")
    if done:
        break

print(f"Simulation terminée après {step} étapes")
```

### Avec Agent Personnalisé
```python
from ev2gym.models.ev2gym_env import EV2Gym
import numpy as np

def agent_intelligent(env):
    """Agent qui charge quand les prix sont bas"""
    actions = np.zeros(env.number_of_ports)
    
    for i, cs in enumerate(env.charging_stations):
        prix_actuel = env.charge_prices[cs.id, env.current_step]
        
        for j in range(cs.n_ports):
            if cs.evs_connected[j] is not None:
                # Charger si prix < 0.1 €/kWh
                actions[i * cs.n_ports + j] = 1.0 if prix_actuel < 0.1 else 0.3
    
    return actions

# Utiliser l'agent
env = EV2Gym(config_file="ev2gym/example_config_files/V2GProfitMax.yaml")
obs, info = env.reset()

for step in range(100):
    action = agent_intelligent(env)
    obs, reward, done, truncated, info = env.step(action)
    if done:
        break
```

## 🔍 Résolution de Problèmes

### Problèmes Courants

#### ImportError: No module named 'ev2gym'
```bash
# Réinstaller en mode développement
pip install -e .
```

#### Erreur de configuration YAML
```bash
# Vérifier que les fichiers de config existent
ls ev2gym/example_config_files/
```

#### Streamlit non trouvé
```bash
# Installer Streamlit
pip install streamlit
```

#### Jupyter non trouvé
```bash
# Installer Jupyter
pip install jupyter
```

### Vérification de l'Installation
```bash
# Test complet
python run_ev2gym.py test

# Test des imports
python -c "import ev2gym; print('✅ EV2Gym OK')"
```

## 📚 Prochaines Étapes

1. **📖 Lire la documentation complète** : `README.md`
2. **🎓 Suivre le notebook de démonstration** : `notebooks/EV2Gym_Demo.ipynb`
3. **⚙️ Créer vos propres configurations** : Modifier les fichiers YAML
4. **🤖 Développer vos agents** : Implémenter vos stratégies de contrôle
5. **📊 Analyser les résultats** : Utiliser les outils d'analyse intégrés

## 🆘 Aide

- **🐛 Problèmes** : Consultez les issues GitHub
- **💬 Questions** : Utilisez les discussions GitHub
- **📧 Contact** : Voir les informations dans README.md

---

**Bon développement avec EV2Gym ! 🚗⚡**
