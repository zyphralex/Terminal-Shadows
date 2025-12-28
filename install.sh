#!/bin/bash
set -e  # Exit on error

echo "🔥 Установка TERMINAL SHADOWS v4.0 ULTIMATE EDITION 🔥"
echo "========================================================"
echo ""

# Проверка Python3
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 не найден!"
    echo "📥 Установите: sudo apt install python3 python3-venv python3-pip"
    exit 1
fi

echo "✅ Python3 найден: $(python3 --version)"
echo ""

# Создание виртуального окружения
echo "📦 Создание виртуального окружения..."
if python3 -m venv venv; then
    echo "✅ Виртуальное окружение создано"
else
    echo "❌ Ошибка создания окружения"
    exit 1
fi

echo "🔌 Активация окружения..."
source venv/bin/activate

# Установка зависимостей
echo "📥 Обновление pip..."
pip install --upgrade pip --quiet

echo "📥 Установка зависимостей..."
if pip install -r requirements.txt; then
    echo "✅ Зависимости установлены"
else
    echo "❌ Ошибка установки зависимостей"
    exit 1
fi

# Создание директорий для данных
echo "📁 Создание директорий для данных..."
mkdir -p ~/.terminal_shadows_ultimate/saves
mkdir -p ~/.terminal_shadows_ultimate/backups

# Делаем скрипты исполняемыми
echo "🔧 Настройка прав доступа..."
chmod +x run_game.sh 2>/dev/null || true
chmod +x update_game.sh 2>/dev/null || true

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
