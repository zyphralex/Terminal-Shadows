#!/bin/bash
echo "🔥 Установка TERMINAL SHADOWS v4.0 ULTIMATE EDITION 🔥"
echo "========================================================"

if ! command -v python3 &> /dev/null; then
    echo "❌ Установите Python3: sudo apt install python3 python3-venv"
    exit 1
fi

# Создание виртуального окружения
python3 -m venv venv
source venv/bin/activate

# Установка зависимостей
pip install --upgrade pip
pip install -r requirements.txt

# Создание директорий для данных
mkdir -p ~/.terminal_shadows_ultimate/saves
mkdir -p ~/.terminal_shadows_ultimate/backups

# Делаем скрипты исполняемыми
chmod +x run_game.sh
chmod +x update_game.sh

echo ""
echo "✅ УСТАНОВКА ЗАВЕРШЕНА!"
echo "🎮 Запуск игры: ./run_game.sh"
echo "🔄 Обновление: ./update_game.sh"
echo ""
echo "💾 Данные игры: ~/.terminal_shadows_ultimate/"
echo "📁 Сохранения: ~/.terminal_shadows_ultimate/saves/"
echo ""
echo "✨ НОВОЕ В v4.0 ULTIMATE EDITION:"
echo "   • 📖 40 ГЛАВ СЮЖЕТА (новые 36-40!)"
echo "   • 🎲 СЛУЧАЙНЫЕ СОБЫТИЯ (8+ сценариев)"
echo "   • 👹 БИТВЫ С БОССАМИ (8 боссов)"
echo "   • 🔨 СИСТЕМА КРАФТА (7 рецептов)"
echo "   • 🎭 ФРАКЦИИ (5 группировок)"
echo "   • 📋 ЕЖЕДНЕВНЫЕ ЗАДАНИЯ"
echo "   • 🎨 ЦВЕТНОЙ ИНТЕРФЕЙС"
echo "   • 🏆 20 ДОСТИЖЕНИЙ"
