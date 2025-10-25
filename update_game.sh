#!/bin/bash
cd "$(dirname "$0")"
echo "🔄 Запуск апдейтера Terminal Shadows..."
echo "======================================"

if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
else
    echo "❌ Виртуальное окружение не найдено"
    echo "📥 Запустите сначала: ./install.sh"
    exit 1
fi

# Проверяем наличие апдейтера
if [ ! -f "updater.py" ]; then
    echo "❌ Апдейтер не найден!"
    echo "📥 Скачайте полную версию игры с GitHub"
    exit 1
fi

# Запускаем апдейтер
python3 updater.py
