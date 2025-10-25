#!/bin/bash
echo "🐧 Установка TERMINAL SHADOWS ULTIMATE v2.0..."
echo "=============================================="

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
echo "✨ ОСОБЕННОСТИ v2.0:"
echo "   • 📖 СЮЖЕТНЫЙ РЕЖИМ (30 глав)"
echo "   • 🎯 СВОБОДНЫЙ РЕЖИМ (бесконечная игра)"
echo "   • 💾 Раздельные сохранения для каждого режима"
echo "   • 🤖 Анонимный гид"
echo "   • 🔄 Встроенный апдейтер"
