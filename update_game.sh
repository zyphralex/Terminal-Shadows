#!/bin/bash
cd "$(dirname "$0")"
echo "🔄 Запуск апдейтера Terminal Shadows v4.0"
echo "=========================================="
echo ""

if [ -f "venv/bin/activate" ]; then
    echo "✅ Активация виртуального окружения..."
    source venv/bin/activate
else
    echo "❌ Виртуальное окружение не найдено"
    echo "📥 Запустите сначала: ./install.sh"
    echo ""
    read -p "Нажмите Enter для выхода..."
    exit 1
fi

# Проверяем наличие апдейтера
if [ ! -f "updater.py" ]; then
    echo "❌ Апдейтер не найден!"
    echo "📥 Скачайте полную версию игры с GitHub:"
    echo "   https://github.com/zyphralex/Terminal-Shadows"
    echo ""
    read -p "Нажмите Enter для выхода..."
    exit 1
fi

echo ""
echo "🚀 Запуск апдейтера..."
echo ""

# Запускаем апдейтер
python3 updater.py
EXIT_CODE=$?

if [ $EXIT_CODE -ne 0 ]; then
    echo ""
    echo "❌ Ошибка при обновлении! Код: $EXIT_CODE"
    echo ""
fi

read -p "Нажмите Enter для выхода..."
