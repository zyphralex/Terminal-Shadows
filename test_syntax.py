#!/usr/bin/env python3
import sys
import os

print("🔍 Проверка синтаксиса Terminal Shadows...")
print("=" * 50)

errors = []

print("\n1. Проверка main.py...")
try:
    import main
    print("✅ main.py - синтаксис корректен")
except Exception as e:
    print(f"❌ main.py - ошибка: {e}")
    errors.append(f"main.py: {e}")

print("\n2. Проверка глав...")
sys.path.append('story')
chapter_count = 0
for i in range(1, 41):
    try:
        mod = __import__(f'chapter{i}')
        chap = getattr(mod, f'CHAPTER_{i}', None)
        if chap:
            chapter_count += 1
            print(f"✅ Глава {i}: OK")
        else:
            print(f"⚠️  Глава {i}: нет CHAPTER_{i}")
    except Exception as e:
        print(f"❌ Глава {i}: {e}")
        errors.append(f"chapter{i}: {e}")

print(f"\n📊 Всего глав загружено: {chapter_count}/40")

print("\n3. Проверка зависимостей...")
try:
    import colorama
    print("✅ colorama установлен")
except:
    print("⚠️  colorama не установлен (необязательно)")

try:
    import requests
    print("✅ requests установлен")
except:
    print("⚠️  requests не установлен (необязательно)")

if errors:
    print(f"\n❌ Найдено ошибок: {len(errors)}")
    for err in errors:
        print(f"  - {err}")
else:
    print("\n✅ Все проверки пройдены успешно!")

print("\n" + "=" * 50)
