@echo off
chcp 65001 > nul
cls

echo 🔥 Установка TERMINAL SHADOWS v4.0 ULTIMATE EDITION 🔥
echo ========================================================

:: Проверка наличия Python
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python не установлен или не добавлен в PATH!
    echo Скачайте его с python.org и не забудьте галочку "Add Python to PATH"
    pause
    exit /b 1
)

echo 📦 Создание виртуального окружения...
python -m venv venv

echo 🔌 Активация окружения...
call venv\Scripts\activate.bat

echo 📥 Установка зависимостей...
python -m pip install --upgrade pip
pip install -r requirements.txt

echo 📁 Создание папок для сохранений...
if not exist "%USERPROFILE%\.terminal_shadows_ultimate\saves" mkdir "%USERPROFILE%\.terminal_shadows_ultimate\saves"
if not exist "%USERPROFILE%\.terminal_shadows_ultimate\backups" mkdir "%USERPROFILE%\.terminal_shadows_ultimate\backups"

echo.
echo ✅ УСТАНОВКА ЗАВЕРШЕНА!
echo 🎮 Запуск игры: run_game.bat
echo 🔄 Обновление: update_game.bat
echo.
echo 💾 Данные игры: %USERPROFILE%\.terminal_shadows_ultimate\
echo 📁 Сохранения: %USERPROFILE%\.terminal_shadows_ultimate\saves\
echo.
echo ✨ НОВОЕ В v4.0 ULTIMATE EDITION:
echo    • 📖 40 ГЛАВ СЮЖЕТА (новые 36-40!)
echo    • 🎲 СЛУЧАЙНЫЕ СОБЫТИЯ (8+ сценариев)
echo    • 👹 БИТВЫ С БОССАМИ (8 боссов)
echo    • 🔨 СИСТЕМА КРАФТА (7 рецептов)
echo    • 🎭 ФРАКЦИИ (5 группировок)
echo    • 📋 ЕЖЕДНЕВНЫЕ ЗАДАНИЯ
echo    • 🎨 ЦВЕТНОЙ ИНТЕРФЕЙС
echo    • 🏆 20 ДОСТИЖЕНИЙ
echo.
pause