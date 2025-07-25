@echo off
REM Script de démarrage EV2Gym Dashboard Ultra-Professionnel
REM Usage: start_dashboard.bat [auto-soc|auto-grid|both]

echo 🚗⚡ EV2Gym Dashboard Ultra-Professionnel Launcher
echo =====================================================

set DASHBOARD=%1
if "%DASHBOARD%"=="" set DASHBOARD=both

if "%DASHBOARD%"=="auto-soc" goto AUTO_SOC
if "%DASHBOARD%"=="auto-grid" goto AUTO_GRID
if "%DASHBOARD%"=="both" goto BOTH
if "%DASHBOARD%"=="8506" goto AUTO_SOC
if "%DASHBOARD%"=="8507" goto AUTO_GRID
goto USAGE

:AUTO_SOC
echo 🔋⚡ Démarrage Dashboard SOC & Power AUTO (8506)
echo 📍 URL: http://localhost:8506
echo ✨ Simulation automatique avec modèles authentiques
echo 🎯 Paramètres critiques optimisés pour jury
streamlit run professional_auto_soc_dashboard.py --server.port=8506
goto END

:AUTO_GRID
echo 🌐⚡ Démarrage Dashboard Grid Impact AUTO (8507)
echo 📍 URL: http://localhost:8507
echo ✨ Simulation automatique réseau électrique
echo 🎯 Services auxiliaires et stabilité réseau
streamlit run professional_auto_grid_dashboard.py --server.port=8507
goto END

:BOTH
echo 🚀 Démarrage des DEUX dashboards ultra-professionnels
echo.
echo 🔋 Dashboard SOC & Power AUTO: http://localhost:8506
echo 🌐 Dashboard Grid Impact AUTO: http://localhost:8507
echo.
echo ✨ Simulation automatique complète
echo 🎯 Prêt pour présentation jury
echo.
start "SOC Dashboard" streamlit run professional_auto_soc_dashboard.py --server.port=8506
timeout /t 3 /nobreak >nul
start "Grid Dashboard" streamlit run professional_auto_grid_dashboard.py --server.port=8507
echo.
echo 🎉 Les deux dashboards sont en cours de démarrage...
echo 📍 SOC & Power: http://localhost:8506
echo 📍 Grid Impact: http://localhost:8507
goto END

:USAGE
echo ❌ Option non reconnue: %DASHBOARD%
echo.
echo Usage: %0 [auto-soc^|auto-grid^|both]
echo   auto-soc  - Dashboard SOC & Power AUTO (8506)
echo   auto-grid - Dashboard Grid Impact AUTO (8507)
echo   both      - Les deux dashboards simultanément
echo   8506      - Alias pour auto-soc
echo   8507      - Alias pour auto-grid
echo.
echo 🎯 Recommandé pour jury: both
pause
exit /b 1

:END
echo.
echo 🎉 Dashboard(s) EV2Gym Ultra-Professionnel(s) prêt(s) !
echo 🎓 Optimisé pour présentation jury de thèse
pause
