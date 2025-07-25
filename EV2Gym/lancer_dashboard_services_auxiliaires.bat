@echo off
echo.
echo ========================================================================
echo   🚗⚡🌐 AMÉLIORATION DES SERVICES AUXILIAIRES VIA RL ET CONTRÔLE AVANCÉ
echo ========================================================================
echo.
echo ✨ DASHBOARD INTERACTIF ET INTELLIGENT EN TEMPS RÉEL
echo 📊 Optimisation des Services Auxiliaires via RL et MPC
echo 🔋 Suivi Comportement Dynamique des VE Connectés
echo ⚡ Visualisation Impact sur le Réseau Électrique
echo 🤖 Évaluation Performances des Algorithmes de Décision
echo 💰 KPI Réseau et Économiques en MAD
echo.
echo ========================================================================
echo   FONCTIONNALITÉS PRINCIPALES
echo ========================================================================
echo.
echo 🎛️ CONTRÔLES D'ENTRÉE:
echo    📊 Nombre de VE connectés (10-2000)
echo    🔌 Type de borne: AC/DC Fast/Ultra rapide
echo    ⚡ Paramètres réseau et transformateur
echo    💰 Tarification dynamique selon l'heure
echo    🤖 Choix algorithme: RL/MPC/Heuristique
echo    🌐 Scénarios réseau multiples
echo.
echo 📈 SORTIES KPI:
echo    🚗 SOC moyen/individuel, puissance V2G/G2V
echo    ⚡ Tension, courant, fréquence, THD
echo    💰 Coûts/revenus en MAD, services auxiliaires
echo    📊 Visualisations temps réel avancées
echo.
echo 🎯 TARIFICATION INTELLIGENTE:
echo    🔌 AC (lente): 1-3 MAD/kWh selon demande
echo    ⚡ DC Fast: 5-10 MAD/kWh selon demande
echo    🕐 Variation horaire automatique
echo    💡 Heures pointe/creuse/normale
echo.
echo ========================================================================
echo   LANCEMENT DU DASHBOARD
echo ========================================================================
echo.

set CHOICE=%1
if "%CHOICE%"=="" set CHOICE=principal

if "%CHOICE%"=="principal" goto PRINCIPAL
if "%CHOICE%"=="test" goto TEST
if "%CHOICE%"=="demo" goto DEMO
goto USAGE

:PRINCIPAL
echo 🚀 Lancement du Dashboard Principal
echo 📍 URL: http://localhost:8888
echo ✨ Simulation temps réel avec tous les KPI
echo.
streamlit run amelioration_services_auxiliaires_dashboard.py --server.port=8888
goto END

:TEST
echo 🧪 Mode Test - Vérification des Fonctionnalités
echo 📍 URL: http://localhost:8889
echo 🔧 Test des algorithmes et visualisations
echo.
streamlit run amelioration_services_auxiliaires_dashboard.py --server.port=8889 --server.runOnSave=true
goto END

:DEMO
echo 🎯 Mode Démonstration - Présentation
echo 📍 URL: http://localhost:8890
echo 🎪 Configuration optimisée pour démonstration
echo.
streamlit run amelioration_services_auxiliaires_dashboard.py --server.port=8890 --server.headless=false
goto END

:USAGE
echo ❌ Option invalide: %CHOICE%
echo.
echo Usage: %0 [principal^|test^|demo]
echo.
echo Options:
echo   principal  - Lancement normal du dashboard (Port 8888)
echo   test       - Mode test avec rechargement automatique (Port 8889)
echo   demo       - Mode démonstration pour présentation (Port 8890)
echo.
echo 🎯 Recommandé pour utilisation normale: principal
echo 🧪 Pour développement/test: test
echo 🎪 Pour démonstration: demo
echo.
pause
exit /b 1

:END
echo.
echo ========================================================================
echo   DASHBOARD SERVICES AUXILIAIRES ACTIF
echo ========================================================================
echo.
echo 🎓 Optimisé pour Recherche et Développement
echo 📊 Visualisations Temps Réel Avancées
echo 🔬 Intégration Authentique EV2Gym
echo 💰 Analyse Économique Complète en MAD
echo ⚡ Conformité Standards Réseau
echo 🌐 Scénarios Multiples et Algorithmes IA
echo.
echo 🎉 Prêt pour Analyse et Optimisation!
echo.
echo ========================================================================
echo   GUIDE D'UTILISATION RAPIDE
echo ========================================================================
echo.
echo 1. 🎛️ CONFIGURATION:
echo    - Ajustez le nombre de VE (sidebar)
echo    - Sélectionnez le type de borne
echo    - Choisissez l'algorithme (RL/MPC/Heuristique)
echo    - Définissez le scénario réseau
echo.
echo 2. 📊 OBSERVATION:
echo    - KPI VE: SOC, puissance, états
echo    - KPI Réseau: tension, courant, fréquence, THD
echo    - KPI Économiques: coûts, revenus, ROI en MAD
echo.
echo 3. 📈 ANALYSE:
echo    - Courbes SOC vs temps
echo    - Heatmap décisions algorithmes
echo    - Comparaison scénarios réseau
echo    - Rentabilité V2G/G2V
echo.
echo 4. 🎯 OPTIMISATION:
echo    - Testez différents algorithmes
echo    - Comparez les scénarios
echo    - Analysez l'impact économique
echo    - Optimisez les services auxiliaires
echo.
echo ========================================================================
echo.
pause
