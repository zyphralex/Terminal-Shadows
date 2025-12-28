@echo off
chcp 65001 > nul
cd /d "%~dp0"
cls

echo 🔄 Запуск апдейтера Terminal Shadows v4.0
echo ==========================================
echo.

if exist "venv\Scripts\activate.bat" (
    echo ✅ Активация виртуального окружения...
    call venv\Scripts\activate.bat
    echo ✅ Окружение активировано
) else (
    echo.
    echo ❌ Виртуальное окружение не найдено
    echo 📥 Запустите сначала: install.bat
    echo.
    pause
    exit /b 1
)

:: Проверяем наличие апдейтера
if not exist "updater.py" (
    echo.
    echo ❌ Апдейтер не найден!
    echo 📥 Скачайте полную версию игры с GitHub:
    echo    https://github.com/zyphralex/Terminal-Shadows
    echo.
    pause
    exit /b 1
)

echo.
echo 🚀 Запуск апдейтера...
echo.

:: Запускаем апдейтер
python updater.py

if %errorlevel% neq 0 (
    echo.
    echo ❌ Ошибка при обновлении! Код: %errorlevel%
    echo.
)

pause