#!/bin/bash
cd "$(dirname "$0")"
echo "🚀 TERMINAL SHADOWS ULTIMATE v2.0"
echo "=================================="
echo "📖 30 глав эпического сюжета"
echo "🎯 Свободный режим с бесконечной игрой"
echo "🤖 Анонимный гид"
echo "💾 Раздельные сохранения"
echo "🔄 Встроенный апдейтер"
echo "=================================="

if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
else
    echo "❌ Сначала запустите: ./install.sh"
    exit 1
fi

python3 main.py
