#!/bin/bash
cd "$(dirname "$0")"
echo "🔥 TERMINAL SHADOWS v4.0 ULTIMATE EDITION 🔥"
echo "=============================================="
echo "📖 40 глав | 🎲 События | 👹 Боссы"
echo "🔨 Крафт | 🎭 Фракции | 🏆 20 достижений"
echo "=============================================="

if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
else
    echo "❌ Сначала запустите: ./install.sh"
    exit 1
fi

python3 main.py
