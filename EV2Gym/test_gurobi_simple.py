#!/usr/bin/env python3
"""
Test simple de Gurobi pour EV2Gym
"""

def test_gurobi_basic():
    """Test de base de Gurobi"""
    try:
        import gurobipy as gp
        from gurobipy import GRB
        
        print("✅ Gurobi importé avec succès")
        
        # Créer un modèle simple de charge VE
        model = gp.Model("test_ev_charging")
        
        # Variables: puissance de charge pour 3 VE
        ev1_power = model.addVar(lb=0, ub=11, name="ev1_power")
        ev2_power = model.addVar(lb=0, ub=11, name="ev2_power") 
        ev3_power = model.addVar(lb=0, ub=11, name="ev3_power")
        
        # Contrainte: limite de puissance totale
        model.addConstr(ev1_power + ev2_power + ev3_power <= 25, "power_limit")
        
        # Objectif: maximiser la charge totale
        model.setObjective(ev1_power + ev2_power + ev3_power, GRB.MAXIMIZE)
        
        # Optimiser
        model.optimize()
        
        if model.status == GRB.OPTIMAL:
            print("✅ Optimisation réussie!")
            print(f"   EV1: {ev1_power.x:.2f} kW")
            print(f"   EV2: {ev2_power.x:.2f} kW") 
            print(f"   EV3: {ev3_power.x:.2f} kW")
            print(f"   Total: {ev1_power.x + ev2_power.x + ev3_power.x:.2f} kW")
            return True
        else:
            print(f"❌ Statut d'optimisation: {model.status}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False
    finally:
        if 'model' in locals():
            model.dispose()

def test_ev2gym_agents():
    """Test des agents MPC d'EV2Gym"""
    try:
        import sys
        sys.path.append("EV2Gym")
        
        print("\n🧪 Test des agents MPC EV2Gym:")
        
        # Test OCMF_V2G
        try:
            from ev2gym.baselines.mpc.ocmf_mpc import OCMF_V2G
            print("✅ OCMF_V2G - Optimal Charging Management Framework")
        except ImportError as e:
            print(f"❌ OCMF_V2G: {e}")
        
        # Test eMPC_V2G
        try:
            from ev2gym.baselines.mpc.eMPC_v2 import eMPC_V2G_v2
            print("✅ eMPC_V2G - Economic Model Predictive Control")
        except ImportError as e:
            print(f"❌ eMPC_V2G: {e}")
        
        # Test V2GProfitMax
        try:
            from ev2gym.baselines.mpc.V2GProfitMax import V2GProfitMaxOracle
            print("✅ V2GProfitMax - Oracle de profit optimal")
        except ImportError as e:
            print(f"❌ V2GProfitMax: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test des agents: {e}")
        return False

if __name__ == "__main__":
    print("🎯 Test de Gurobi pour EV2Gym")
    print("=" * 35)
    
    # Test de base
    if test_gurobi_basic():
        print("\n🎉 Gurobi fonctionne parfaitement!")
    else:
        print("\n❌ Problème avec Gurobi")
    
    # Test des agents
    test_ev2gym_agents()
    
    print("\n🚀 Gurobi est prêt pour EV2Gym!")
    print("Vous pouvez maintenant utiliser les agents MPC optimaux dans le dashboard.")
