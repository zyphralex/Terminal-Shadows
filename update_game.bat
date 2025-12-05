@echo off
chcp 65001 > nul
cd /d "%~dp0"
cls

echo 🔄 Запуск апдейтера Terminal Shadows...
echo ======================================

if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
) else (
    echo ❌ Виртуальное окружение не найдено
    echo 📥 Запустите сначала: install.bat
    pause
    exit /b 1
)

:: Проверяем наличие апдейтера
if not exist "updater.py" (
    echo ❌ Апдейтер не найден!
    echo 📥 Скачайте полную версию игры с GitHub
    pause
    exit /b 1
)

:: Запускаем апдейтер
python updater.py
pause