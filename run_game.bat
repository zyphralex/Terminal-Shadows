@echo off
chcp 65001 > nul
cd /d "%~dp0"
cls

echo 🔥 TERMINAL SHADOWS v4.0 ULTIMATE EDITION 🔥
echo ==============================================
echo 📖 40 глав | 🎲 События | 👹 Боссы
echo 🔨 Крафт | 🎭 Фракции | 🏆 20 достижений
echo ==============================================

if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
) else (
    echo ❌ Сначала запустите: install.bat
    pause
    exit /b 1
)

python main.py
pause