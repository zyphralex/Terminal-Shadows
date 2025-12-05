@echo off
chcp 65001 > nul
cd /d "%~dp0"
cls

echo 🚀 TERMINAL SHADOWS ULTIMATE v3.0
echo ==================================
echo 📖 35 глав эпического сюжета
echo 🎯 Свободный режим с бесконечной игрой
echo 🤖 Анонимный гид
echo 💾 Раздельные сохранения
echo 🔄 Встроенный апдейтер
echo ==================================

if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
) else (
    echo ❌ Сначала запустите: install.bat
    pause
    exit /b 1
)

python main.py
pause