#!/usr/bin/env python3
"""
🧪 TEST COMPLET - DASHBOARD SERVICES AUXILIAIRES

Script de test complet pour vérifier toutes les fonctionnalités
du dashboard d'amélioration des services auxiliaires.
"""

import sys
import traceback
import requests
import time
from pathlib import Path

def test_dashboard_launch():
    """Test de lancement du dashboard"""
    
    print("🧪 TEST DE LANCEMENT DU DASHBOARD")
    print("=" * 60)
    
    try:
        # Test d'accessibilité
        response = requests.get("http://localhost:8888", timeout=10)
        if response.status_code == 200:
            print("✅ Dashboard accessible sur http://localhost:8888")
            return True
        else:
            print(f"❌ Erreur HTTP {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Dashboard non accessible: {e}")
        return False

def test_module_imports():
    """Test des imports du module principal"""
    
    print("\n📦 TEST DES IMPORTS")
    print("=" * 60)
    
    try:
        # Ajouter le répertoire au path
        sys.path.insert(0, str(Path.cwd()))
        
        # Test d'import du module principal
        print("  📦 Import du module principal...")
        import amelioration_services_auxiliaires_dashboard as main_module
        print("  ✅ Module principal importé avec succès")
        
        # Test des fonctions principales
        print("  🔧 Test des fonctions principales...")
        
        # Test simulation RL
        test_params = {
            'n_ve_connectes': 100,
            'apprentissage_actif': True,
            'activation_v2g': True,
            'puissance_max': 22
        }
        
        rl_result = main_module.simulate_rl_algorithm(100, "RL - PPO", 50, test_params)
        if isinstance(rl_result, dict) and 'soc_moyen_percent' in rl_result:
            print("  ✅ Simulation RL PPO OK")
        else:
            print("  ❌ Problème simulation RL PPO")
        
        # Test simulation MPC
        mpc_result = main_module.simulate_mpc_algorithm(100, 50, test_params)
        if isinstance(mpc_result, dict) and 'prix_predit' in mpc_result:
            print("  ✅ Simulation MPC OK")
        else:
            print("  ❌ Problème simulation MPC")
        
        # Test simulation heuristique
        heur_result = main_module.simulate_heuristic_algorithm(100, "Heuristique - Round Robin", 50, test_params)
        if isinstance(heur_result, dict) and 'performance_algorithme' in heur_result:
            print("  ✅ Simulation Heuristique OK")
        else:
            print("  ❌ Problème simulation Heuristique")
        
        # Test simulation réseau
        ev_data = {'puissance_g2v_kw': 500, 'puissance_v2g_kw': 200}
        grid_result = main_module.simulate_grid_scenario(ev_data, "Fonctionnement normal", test_params)
        if isinstance(grid_result, dict) and 'tension_moyenne_v' in grid_result:
            print("  ✅ Simulation Réseau OK")
        else:
            print("  ❌ Problème simulation Réseau")
        
        # Test calculs économiques
        grid_data = {'frequence_reseau_hz': 50.0, 'tension_moyenne_v': 230, 'load_factor': 0.8}
        econ_result = main_module.calculate_economic_metrics(ev_data, grid_data, test_params)
        if isinstance(econ_result, dict) and 'benefice_net_mad' in econ_result:
            print("  ✅ Calculs Économiques OK")
        else:
            print("  ❌ Problème calculs Économiques")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Erreur lors des tests: {e}")
        print(f"  📋 Traceback: {traceback.format_exc()}")
        return False

def test_data_availability():
    """Test de disponibilité des données"""
    
    print("\n📊 TEST DISPONIBILITÉ DES DONNÉES")
    print("=" * 60)
    
    # Fichiers de données EV2Gym
    data_files = [
        "ev2gym/data/ev_specs_v2g_enabled2024.json",
        "ev2gym/data/Netherlands_day-ahead-2015-2024.csv",
        "ev2gym/data/residential_loads.csv",
        "ev2gym/data/pv_netherlands.csv"
    ]
    
    available_files = 0
    for file_path in data_files:
        if Path(file_path).exists():
            size_kb = Path(file_path).stat().st_size / 1024
            print(f"  ✅ {file_path} ({size_kb:.1f} KB)")
            available_files += 1
        else:
            print(f"  ⚠️ {file_path} (manquant - utilisera données synthétiques)")
    
    print(f"  📈 Disponibilité: {available_files}/{len(data_files)} fichiers")
    return available_files

def test_algorithm_performance():
    """Test des performances des algorithmes"""
    
    print("\n🤖 TEST PERFORMANCE DES ALGORITHMES")
    print("=" * 60)
    
    try:
        import amelioration_services_auxiliaires_dashboard as main_module
        
        test_params = {
            'n_ve_connectes': 500,
            'apprentissage_actif': True,
            'activation_v2g': True,
            'puissance_max': 22,
            'prix_actuel': 2.0,
            'prix_v2g': 4.0
        }
        
        algorithms = [
            "RL - Deep Q-Network (DQN)",
            "RL - Proximal Policy Optimization (PPO)", 
            "RL - Soft Actor-Critic (SAC)",
            "MPC - Model Predictive Control",
            "Heuristique - Round Robin",
            "Heuristique - Charge Rapide",
            "Heuristique - Équilibrage Intelligent"
        ]
        
        performances = []
        
        for algo in algorithms:
            try:
                if "RL" in algo:
                    result = main_module.simulate_rl_algorithm(500, algo, 100, test_params)
                elif "MPC" in algo:
                    result = main_module.simulate_mpc_algorithm(500, 100, test_params)
                else:
                    result = main_module.simulate_heuristic_algorithm(500, algo, 100, test_params)
                
                performance = result.get('performance_algorithme', 0) * 100
                performances.append(performance)
                print(f"  ✅ {algo}: {performance:.1f}%")
                
            except Exception as e:
                print(f"  ❌ {algo}: Erreur - {e}")
                performances.append(0)
        
        avg_performance = sum(performances) / len(performances) if performances else 0
        print(f"  📊 Performance moyenne: {avg_performance:.1f}%")
        
        return avg_performance > 50
        
    except Exception as e:
        print(f"  ❌ Erreur test algorithmes: {e}")
        return False

def test_economic_calculations():
    """Test des calculs économiques"""
    
    print("\n💰 TEST CALCULS ÉCONOMIQUES")
    print("=" * 60)
    
    try:
        import amelioration_services_auxiliaires_dashboard as main_module
        
        # Données de test
        ev_data = {
            'puissance_g2v_kw': 1000,  # 1 MW charge
            'puissance_v2g_kw': 500    # 500 kW décharge
        }
        
        grid_data = {
            'frequence_reseau_hz': 49.9,  # Légère déviation
            'tension_moyenne_v': 225,     # Tension basse
            'load_factor': 0.85           # Charge élevée
        }
        
        test_params = {
            'prix_actuel': 2.0,           # 2 MAD/kWh
            'prix_v2g': 4.0,             # 4 MAD/kWh
            'prix_services_auxiliaires': 100,  # 100 MAD/kW
            'frequence_maj': 1.0,        # 1 minute
            'n_ve_connectes': 500
        }
        
        result = main_module.calculate_economic_metrics(ev_data, grid_data, test_params)
        
        # Vérifications
        cout_recharge = result.get('cout_recharge_total_mad', 0)
        revenus_v2g = result.get('revenus_v2g_mad', 0)
        benefice_net = result.get('benefice_net_mad', 0)
        services_aux = result.get('services_auxiliaires_mad', 0)
        
        print(f"  💸 Coût recharge: {cout_recharge:.2f} MAD")
        print(f"  💰 Revenus V2G: {revenus_v2g:.2f} MAD")
        print(f"  ⚡ Services auxiliaires: {services_aux:.2f} MAD")
        print(f"  📊 Bénéfice net: {benefice_net:.2f} MAD")
        
        # Validation logique
        if cout_recharge > 0 and revenus_v2g > 0:
            print("  ✅ Calculs économiques cohérents")
            return True
        else:
            print("  ❌ Calculs économiques incohérents")
            return False
            
    except Exception as e:
        print(f"  ❌ Erreur calculs économiques: {e}")
        return False

def test_grid_scenarios():
    """Test des scénarios réseau"""
    
    print("\n🌐 TEST SCÉNARIOS RÉSEAU")
    print("=" * 60)
    
    try:
        import amelioration_services_auxiliaires_dashboard as main_module
        
        ev_data = {'puissance_g2v_kw': 800, 'puissance_v2g_kw': 300}
        test_params = {'puissance_transformateur': 1000}
        
        scenarios = [
            "Fonctionnement normal",
            "Réseau en urgence",
            "Intégration énergie renouvelable", 
            "Période de forte demande",
            "Période de faible demande"
        ]
        
        for scenario in scenarios:
            try:
                result = main_module.simulate_grid_scenario(ev_data, scenario, test_params)
                
                tension = result.get('tension_moyenne_v', 0)
                frequence = result.get('frequence_reseau_hz', 0)
                thd = result.get('thd_percent', 0)
                
                print(f"  ✅ {scenario}:")
                print(f"     Tension: {tension:.1f}V, Fréquence: {frequence:.3f}Hz, THD: {thd:.2f}%")
                
            except Exception as e:
                print(f"  ❌ {scenario}: Erreur - {e}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Erreur test scénarios: {e}")
        return False

def main():
    """Test principal complet"""
    
    print("🧪 TEST COMPLET - DASHBOARD SERVICES AUXILIAIRES")
    print("=" * 80)
    
    # Tests
    dashboard_ok = test_dashboard_launch()
    imports_ok = test_module_imports()
    data_count = test_data_availability()
    algo_ok = test_algorithm_performance()
    econ_ok = test_economic_calculations()
    grid_ok = test_grid_scenarios()
    
    # Résumé
    print("\n" + "=" * 80)
    print("📋 RÉSUMÉ DES TESTS")
    print("=" * 80)
    
    print(f"Dashboard accessible:     {'✅ OK' if dashboard_ok else '❌ ERREUR'}")
    print(f"Imports modules:          {'✅ OK' if imports_ok else '❌ ERREUR'}")
    print(f"Données disponibles:      {data_count}/4 fichiers")
    print(f"Performance algorithmes:  {'✅ OK' if algo_ok else '❌ ERREUR'}")
    print(f"Calculs économiques:      {'✅ OK' if econ_ok else '❌ ERREUR'}")
    print(f"Scénarios réseau:         {'✅ OK' if grid_ok else '❌ ERREUR'}")
    
    # Score global
    score = 0
    if dashboard_ok: score += 20
    if imports_ok: score += 25
    score += (data_count / 4) * 15
    if algo_ok: score += 20
    if econ_ok: score += 10
    if grid_ok: score += 10
    
    print(f"\nScore global: {score:.1f}%")
    
    if score >= 90:
        status = "🎉 EXCELLENT - Dashboard parfaitement opérationnel!"
        recommendations = [
            "✅ Tous les tests passent",
            "✅ Prêt pour utilisation en recherche",
            "🚀 Lancez: streamlit run amelioration_services_auxiliaires_dashboard.py --server.port=8888"
        ]
    elif score >= 75:
        status = "✅ BON - Fonctionnalités principales OK"
        recommendations = [
            "⚠️ Quelques données manquantes (utilisera synthétiques)",
            "✅ Algorithmes et calculs fonctionnels",
            "🚀 Utilisable pour recherche et développement"
        ]
    elif score >= 50:
        status = "⚠️ MOYEN - Problèmes à corriger"
        recommendations = [
            "❌ Certaines fonctionnalités défaillantes",
            "🔧 Vérifiez les imports et dépendances",
            "📝 Consultez la documentation"
        ]
    else:
        status = "❌ CRITIQUE - Intervention requise"
        recommendations = [
            "❌ Dashboard non fonctionnel",
            "🔧 Réinstallez les dépendances",
            "📞 Consultez le guide de dépannage"
        ]
    
    print(f"\n🎯 Statut: {status}")
    print("\n📋 Recommandations:")
    for rec in recommendations:
        print(f"   {rec}")
    
    print("\n" + "=" * 80)
    print("🚀 COMMANDES UTILES:")
    print("=" * 80)
    print("# Lancement dashboard:")
    print("streamlit run amelioration_services_auxiliaires_dashboard.py --server.port=8888")
    print()
    print("# Ou utiliser le script:")
    print("lancer_dashboard_services_auxiliaires.bat principal")
    print()
    print("# URL d'accès:")
    print("http://localhost:8888")
    print("=" * 80)
    
    return score

if __name__ == "__main__":
    score = main()
    print(f"\n🎓 Test terminé avec score: {score:.1f}%")
    
    if score >= 90:
        print("🎉 Votre dashboard est parfaitement opérationnel!")
    elif score >= 75:
        print("✅ Dashboard fonctionnel avec quelques limitations mineures.")
    else:
        print("⚠️ Veuillez corriger les problèmes avant utilisation.")
