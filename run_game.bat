@echo off
chcp 65001 > nul
cd /d "%~dp0"
cls

echo 🔥 TERMINAL SHADOWS v4.0 ULTIMATE EDITION 🔥
echo ==============================================
echo 📖 40 глав ^| 🎲 События ^| 👹 Боссы
echo 🔨 Крафт ^| 🎭 Фракции ^| 🏆 20 достижений
echo ==============================================
echo.

if exist "venv\Scripts\activate.bat" (
    echo ✅ Активация виртуального окружения...
    call venv\Scripts\activate.bat
    echo ✅ Окружение активировано
) else (
    echo.
    echo ❌ Виртуальное окружение не найдено!
    echo 📥 Сначала запустите: install.bat
    echo.
    pause
    exit /b 1
)

echo.
echo 🚀 Запуск игры...
echo.

python main.py

if %errorlevel% neq 0 (
    echo.
    echo ❌ Ошибка при запуске игры! Код ошибки: %errorlevel%
    echo 📝 Проверьте что Python установлен и все зависимости на месте
    echo.
)

pause