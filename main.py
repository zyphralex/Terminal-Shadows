#!/usr/bin/env python3
import sys
import platform

system = platform.system()

if system in ("Windows", "Darwin"):
    print("❌ Эта игра доступна только для пользователей Linux-дистрибутивов.")
    print(f"Обнаружена ОС: {system}")
    sys.exit(1)

import os
import sys
import time
import random
import pickle
import json
from datetime import datetime

sys.path.append('story')
import re

chapters = []
try:
    files = [f for f in os.listdir('story') if re.match(r'chapter\d+\.py$', f)]
    nums = []
    for f in files:
        m = re.match(r'chapter(\d+)\.py$', f)
        if m:
            nums.append(int(m.group(1)))
    nums.sort()

    for i in nums:
        mod = f'chapter{i}'
        try:
            module = __import__(mod)
            chap = getattr(module, f'CHAPTER_{i}', None)
            if chap:
                chapters.append(chap)
            else:
                print(f"Warning: {mod} содержит нет CHAPTER_{i}")
        except Exception as e:
            print(f"Error loading {mod}: {e}")
except Exception as e:
    print(f"Error scanning story directory: {e}")

class GameData:
    def __init__(self):
        self.data_dir = os.path.expanduser("~/.terminal_shadows_ultimate")
        self.save_dir = os.path.join(self.data_dir, "saves")
        self.config_file = os.path.join(self.data_dir, "config.json")
        self.ensure_directories()
        self.load_config()
        
    def ensure_directories(self):
        os.makedirs(self.data_dir, exist_ok=True)
        os.makedirs(self.save_dir, exist_ok=True)
        
    def load_config(self):
        default_config = {
            "language": "ru",
            "difficulty": "normal",
            "autosave": True,
            "animations": True,
            "music": False
        }
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    self.config = json.load(f)
                # Обновляем конфиг если добавились новые поля
                for key, value in default_config.items():
                    if key not in self.config:
                        self.config[key] = value
            except:
                self.config = default_config
        else:
            self.config = default_config
            self.save_config()
            
    def save_config(self):
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
        
    def save_game(self, player_data, slot=0, game_mode="story"):
        """Сохраняет игру с указанием режима"""
        if slot == 0:
            save_file = os.path.join(self.save_dir, f"autosave_{game_mode}.dat")
        else:
            save_file = os.path.join(self.save_dir, f"save{slot}_{game_mode}.dat")
            
        save_data = {
            'player': player_data,
            'timestamp': datetime.now().isoformat(),
            'version': '3.0',
            'game_mode': game_mode  # Добавляем информацию о режиме
        }
        try:
            with open(save_file, 'wb') as f:
                pickle.dump(save_data, f)
            return True
        except Exception as e:
            print(f"Save error: {e}")
            return False
            
    def load_game(self, slot=0, game_mode="story"):
        """Загружает игру с указанием режима"""
        if slot == 0:
            save_file = os.path.join(self.save_dir, f"autosave_{game_mode}.dat")
        else:
            save_file = os.path.join(self.save_dir, f"save{slot}_{game_mode}.dat")
            
        if os.path.exists(save_file):
            try:
                with open(save_file, 'rb') as f:
                    return pickle.load(f)
            except Exception as e:
                print(f"Load error: {e}")
                return None
        return None
        
    def get_saves(self, game_mode="story"):
        """Возвращает список доступных сохранений для указанного режима"""
        saves = []
        
        # Проверяем автосохранение
        if os.path.exists(os.path.join(self.save_dir, f"autosave_{game_mode}.dat")):
            saves.append(0)
            
        # Проверяем ручные сохранения
        for i in range(1, 4):
            if os.path.exists(os.path.join(self.save_dir, f"save{i}_{game_mode}.dat")):
                saves.append(i)
                
        return saves

class Player:
    def __init__(self, name):
        self.name = name
        self.level = 1
        self.exp = 0
        self.bitcoins = 1000
        self.skills = {
            "hacking": 1,
            "stealth": 1,
            "programming": 1,
            "social": 1,
            "investigation": 1
        }
        self.inventory = []
        self.story_progress = 1
        self.completed_missions = []
        self.reputation = 0
        self.achievements = []
        
        # ПЕРСОНАЛЬНАЯ статистика игрока
        self.personal_stats = {
            "play_time": 0,
            "chapters_completed": 0,
            "total_bitcoins_earned": 0,
            "hacks_completed": 0,
            "items_collected": 0,
            "achievements_unlocked": 0,
            "start_date": datetime.now().isoformat(),
            "last_play_date": datetime.now().isoformat()
        }
        
    def add_exp(self, amount):
        self.exp += amount
        if self.exp >= self.level * 1000:
            old_level = self.level
            self.level_up()
            return old_level
        return None
        
    def level_up(self):
        self.level += 1
        self.exp = 0
        # При повышении уровня увеличиваем все навыки
        for skill in self.skills:
            self.skills[skill] += 1
        return f"🎉 Уровень повышен! Теперь уровень {self.level}. Все навыки +1!"
        
    def add_skill(self, skill, amount=1):
        if skill in self.skills:
            self.skills[skill] += amount
            return f"⚡ {skill.upper()} повышен до {self.skills[skill]}"
        return ""
        
    def add_bitcoins(self, amount):
        self.bitcoins += amount
        self.personal_stats["total_bitcoins_earned"] += amount
        return f"💰 +{amount} BTC"
        
    def add_achievement(self, achievement):
        if achievement not in self.achievements:
            self.achievements.append(achievement)
            self.personal_stats["achievements_unlocked"] += 1
            return f"🏆 Получено достижение: {achievement}"
        return ""
        
    def add_item(self):
        self.personal_stats["items_collected"] += 1
        
    def add_hack(self):
        self.personal_stats["hacks_completed"] += 1
        
    def update_play_time(self, play_time):
        self.personal_stats["play_time"] += play_time
        self.personal_stats["last_play_date"] = datetime.now().isoformat()

class GameEngine:
    def __init__(self):
        self.data = GameData()
        self.player = None
        self.current_chapter = None
        self.current_scene = "start"
        self.game_mode = "story"  # story или sandbox
        self.start_time = time.time()
        
    def clear_screen(self):
        os.system('clear' if os.name == 'posix' else 'cls')
        
    def print_ascii(self, art_name):
        art_file = f"data/ascii_arts/{art_name}.txt"
        if os.path.exists(art_file):
            with open(art_file, 'r', encoding='utf-8') as f:
                print(f.read())
                
    def type_text(self, text, delay=0.03):
        if self.data.config.get("animations", True):
            for char in text:
                print(char, end='', flush=True)
                time.sleep(delay)
            print()
        else:
            print(text)
            
    def show_guide(self):
        self.print_ascii("anonymous_guide")
        
    def hacking_animation(self, target):
        if not self.data.config.get("animations", True):
            print(f"Взлом {target}...")
            return
            
        print(f"\n🎯 Начинаем взлом {target}...")
        self.show_guide()
        
        frames = [
            "▌░░░░░░░░░ 10%", "▌▌░░░░░░░░ 20%", "▌▌▌░░░░░░░ 30%",
            "▌▌▌▌░░░░░░ 40%", "▌▌▌▌▌░░░░░ 50%", "▌▌▌▌▌▌░░░░ 60%", 
            "▌▌▌▌▌▌▌░░░ 70%", "▌▌▌▌▌▌▌▌░░ 80%", "▌▌▌▌▌▌▌▌▌░ 90%",
            "▌▌▌▌▌▌▌▌▌▌ 100%"
        ]
        for frame in frames:
            print(f"🖥️  {frame}", end='\r')
            time.sleep(0.2)
        print("\n")
        
    def show_main_menu(self):
        while True:
            self.clear_screen()
            self.print_ascii("main_menu")
            print("\n" + "="*60)
            print("1. 📖 СЮЖЕТНЫЙ РЕЖИМ")
            print("2. 🎯 СВОБОДНЫЙ РЕЖИМ")
            print("3. 💾 ЗАГРУЗИТЬ ИГРУ") 
            print("4. ⚙️  НАСТРОЙКИ")
            print("5. 📊 СТАТИСТИКА")
            print("6. 🔄 ПРОВЕРИТЬ ОБНОВЛЕНИЯ")
            print("7. 🚪 ВЫХОД")
            print("="*60)
            
            choice = input("\nВыберите опцию [1-7]: ").strip()
            
            if choice == "1":
                self.story_mode_menu()
            elif choice == "2":
                self.sandbox_mode_menu()
            elif choice == "3":
                self.load_game_menu()
            elif choice == "4":
                self.settings_menu()
            elif choice == "5":
                self.show_stats()
            elif choice == "6":
                self.check_updates()
            elif choice == "7":
                self.exit_game()
            else:
                print("❌ Неверный выбор!")
                input("Нажмите Enter...")
    
    def story_mode_menu(self):
        """Меню сюжетного режима"""
        while True:
            self.clear_screen()
            print("📖 СЮЖЕТНЫЙ РЕЖИМ")
            print("="*30)
            print("1. 🎮 НОВАЯ ИГРА")
            print("2. 💾 ЗАГРУЗИТЬ СЮЖЕТ")
            print("3. 🔙 НАЗАД")
            print()
            
            choice = input("Выберите опцию [1-3]: ").strip()
            
            if choice == "1":
                self.start_new_game("story")
            elif choice == "2":
                self.load_specific_game("story")
            elif choice == "3":
                return
            else:
                print("❌ Неверный выбор!")
                input("Нажмите Enter...")
    
    def sandbox_mode_menu(self):
        """Меню свободного режима"""
        while True:
            self.clear_screen()
            print("🎯 СВОБОДНЫЙ РЕЖИМ")
            print("="*30)
            print("1. 🎮 НОВАЯ ИГРА")
            print("2. 💾 ЗАГРУЗИТЬ СВОБОДНЫЙ РЕЖИМ")
            print("3. 🔙 НАЗАД")
            print()
            
            choice = input("Выберите опцию [1-3]: ").strip()
            
            if choice == "1":
                self.start_new_game("sandbox")
            elif choice == "2":
                self.load_specific_game("sandbox")
            elif choice == "3":
                return
            else:
                print("❌ Неверный выбор!")
                input("Нажмите Enter...")
    
    def start_new_game(self, mode):
        self.clear_screen()
        print("🎮 СОЗДАНИЕ ПЕРСОНАЖА")
        print("="*30)
        
        name = input("\nВведите имя вашего хакера: ").strip()
        if not name:
            name = "Neo"
            
        self.player = Player(name)
        self.game_mode = mode
        
        print(f"\n👤 Приветствую, {self.player.name}!")
        
        if mode == "story":
            print("📖 Запуск СЮЖЕТНОГО РЕЖИМА...")
            time.sleep(2)
            self.start_story_mode()
        else:
            print("🎯 Запуск СВОБОДНОГО РЕЖИМА...")
            time.sleep(2)
            self.start_sandbox_mode()
    
    def start_story_mode(self):
        """Запуск сюжетного режима"""
        # Вступительная кат-сцена
        self.clear_screen()
        self.type_text("\nГод 2049. Цифровой мир стал новой реальностью...")
        time.sleep(1)
        self.type_text("Ты находишь наследие своего дяди - легендарного хакера...")
        time.sleep(1)
        self.type_text("Его последние слова: 'Не доверяй системе, ищи правду в коде'...")
        time.sleep(1)
        self.show_guide()
        self.type_text("\nАнонимный Гид: 'Приветствую в цифровом подполье. Я буду твоим проводником.'")
        time.sleep(2)
        
        input("\n🎯 Нажмите Enter чтобы начать свое путешествие...")
        self.play_story_mode()
    
    def start_sandbox_mode(self):
        """Запуск свободного режима"""
        self.clear_screen()
        self.type_text("\n🎯 СВОБОДНЫЙ РЕЖИМ АКТИВИРОВАН")
        self.type_text("Здесь нет сюжета - только ты и бесконечные возможности цифрового мира.")
        self.type_text("Создавай свою историю, взламывай цели, развивай навыки!")
        time.sleep(2)
        
        # Даем бонусы для песочницы
        self.player.bitcoins = 5000
        self.player.level = 5
        for skill in self.player.skills:
            self.player.skills[skill] = 3
            
        print(f"\n💰 Стартовый бонус: 5000 BTC")
        print(f"🎯 Уровень повышен до 5")
        print(f"⚡ Все навыки установлены на 3")
        
        input("\n🎮 Нажмите Enter чтобы начать...")
        self.sandbox_loop()
        
    def play_story_mode(self):
        """Основной цикл сюжетного режима"""
        if not chapters:
            print("❌ Нет доступных глав для сюжетного режима! Проверьте папку `story/`.")
            input("Нажмите Enter чтобы вернуться в меню...")
            return

        for i, chapter in enumerate(chapters, 1):
            if i == self.player.story_progress:
                self.play_chapter(chapter, i)
                self.player.story_progress += 1
                self.player.personal_stats["chapters_completed"] += 1
                
                # АВТОСОХРАНЕНИЕ после каждой главы
                if self.data.config.get("autosave", True):
                    if self.data.save_game(self.player.__dict__, 0, "story"):
                        print("💾 Сюжет автоматически сохранен!")
                    else:
                        print("❌ Ошибка автосохранения!")
                    time.sleep(1)
                    
        self.print_ascii("victory")
        print("🎊 СЮЖЕТНЫЙ РЕЖИМ ЗАВЕРШЕН!")
        print("Теперь доступен СВОБОДНЫЙ РЕЖИМ с полным функционалом!")
        input("\nНажмите Enter чтобы продолжить...")
        self.sandbox_loop()
        
    def sandbox_loop(self):
        """Основной цикл свободного режима"""
        self.game_mode = "sandbox"
        
        while True:
            self.clear_screen()
            print("🎯 СВОБОДНЫЙ РЕЖИМ")
            print("="*50)
            print(f"👤 {self.player.name} | 💰 {self.player.bitcoins} BTC | 🎯 Ур. {self.player.level}")
            print("="*50)
            print()
            print("1. 🌐 ВЗЛОМ СЕРВЕРОВ")
            print("2. 🛒 МАГАЗИН")
            print("3. 📊 ПРОФИЛЬ")
            print("4. 🏆 ДОСТИЖЕНИЯ")
            print("5. 💾 СОХРАНИТЬ СВОБОДНЫЙ РЕЖИМ")
            print("6. 🏠 ГЛАВНОЕ МЕНЮ")
            print()
            
            choice = input("Выберите действие [1-6]: ").strip()
            
            if choice == "1":
                self.hacking_menu()
            elif choice == "2":
                self.shop_menu()
            elif choice == "3":
                self.profile_menu()
            elif choice == "4":
                self.achievements_menu()
            elif choice == "5":
                self.save_specific_game("sandbox")
            elif choice == "6":
                # Автосохранение при выходе
                if self.data.config.get("autosave", True):
                    self.data.save_game(self.player.__dict__, 0, "sandbox")
                return
            else:
                print("❌ Неверный выбор!")
                input("Нажмите Enter...")
    
    def play_chapter(self, chapter, chapter_num):
        self.current_scene = "start"
        
        while self.current_scene not in ["chapter_end", "next_chapter", "game_end"]:
            if self.current_scene not in chapter["scenes"]:
                print(f"Ошибка: сцена '{self.current_scene}' не найдена")
                self.current_scene = "chapter_end"
                break
                
            scene = chapter["scenes"][self.current_scene]
            
            self.clear_screen()
            print(f"📖 {chapter['title']}")
            print("="*50)
            
            # Показываем гида в определенных сценах
            if chapter.get("guide_appearance", False) and self.current_scene == "start":
                self.show_guide()
                self.type_text("\nАнонимный Гид: 'Эта миссия изменит все. Будь осторожен.'\n")
            
            self.type_text(f"\n{scene['text']}\n")
            
            if "choices" in scene and scene["choices"]:
                for i, choice in enumerate(scene["choices"], 1):
                    print(f"{i}. {choice['text']}")
                    
                print()
                try:
                    choice_num = int(input("Ваш выбор: "))
                    if 1 <= choice_num <= len(scene["choices"]):
                        selected = scene["choices"][choice_num - 1]
                        result = self.apply_effects(selected.get("effect", {}))
                        if result:
                            print(result)
                        self.current_scene = selected["next"]
                    else:
                        print("❌ Неверный выбор!")
                        input()
                except ValueError:
                    print("❌ Введите число!")
                    input()
            else:
                input("\nНажмите Enter чтобы продолжить...")
                self.current_scene = "chapter_end"
                
        if self.current_scene == "game_end":
            self.game_complete()
                
    def apply_effects(self, effects):
        results = []
        
        if "bitcoins" in effects:
            results.append(self.player.add_bitcoins(effects["bitcoins"]))
            
        if "level" in effects:
            self.player.level = effects["level"]
            results.append(f"🎉 Уровень повышен до {effects['level']}!")
            
        if "skill" in effects:
            results.append(self.player.add_skill(effects["skill"], effects.get("value", 1)))
            
        if "exp" in effects:
            old_level = self.player.add_exp(effects["exp"])
            if old_level:
                results.append(self.player.level_up())
            else:
                results.append(f"⭐ +{effects['exp']} опыта")
            
        if "item" in effects:
            self.player.inventory.append(effects["item"])
            self.player.add_item()
            results.append(f"🎒 Получен: {effects['item']}")
            
        if "reputation" in effects:
            self.player.reputation += effects["reputation"]
            results.append(f"📊 Репутация: {self.player.reputation}")
            
        if "achievement" in effects and effects["achievement"]:
            results.append(self.player.add_achievement(effects["achievement"]))
            
        time.sleep(1)
        return "\n".join(results)
        
    def hacking_menu(self):
        targets = [
            {"name": "🏢 MegaCorp Inc", "reward": 500, "difficulty": 1, "req_level": 1},
            {"name": "🏛️  Police Database", "reward": 1000, "difficulty": 2, "req_level": 2},
            {"name": "💊 Black Market", "reward": 2000, "difficulty": 3, "req_level": 3},
            {"name": "🔐 Shadow Network", "reward": 5000, "difficulty": 5, "req_level": 5},
            {"name": "🌍 Global Bank", "reward": 10000, "difficulty": 8, "req_level": 8},
            {"name": "🐉 КиберДракон", "reward": 20000, "difficulty": 10, "req_level": 10},
            {"name": "🤖 ИИ Авалон", "reward": 50000, "difficulty": 15, "req_level": 15},
            {"name": "⚛️  Квантовая Сеть", "reward": 100000, "difficulty": 20, "req_level": 20}
        ]
        
        while True:
            self.clear_screen()
            print("🎯 ВЫБОР ЦЕЛИ ДЛЯ ВЗЛОМА")
            print("="*40)
            print(f"💰 Баланс: {self.player.bitcoins} BTC")
            print("="*40)
            print()
            
            for i, target in enumerate(targets, 1):
                status = "🟢" if self.player.level >= target["req_level"] else "🔴"
                print(f"{i}. {status} {target['name']}")
                print(f"   Награда: {target['reward']} BTC | Уровень: {target['req_level']}+")
                print()
                
            print(f"{len(targets)+1}. 🔙 НАЗАД")
            print()
            
            try:
                choice = int(input("Выберите цель: "))
                if 1 <= choice <= len(targets):
                    target = targets[choice-1]
                    
                    if self.player.level < target["req_level"]:
                        print(f"❌ Требуется уровень {target['req_level']}!")
                        input("Нажмите Enter...")
                        continue
                        
                    self.hacking_animation(target["name"])
                    
                    success_chance = min(0.95, (self.player.skills["hacking"] * 0.25) / target["difficulty"])
                    
                    if random.random() < success_chance:
                        reward = target["reward"]
                        # Бонус за навыки
                        if self.player.skills["hacking"] > target["difficulty"]:
                            bonus = reward // 2
                            reward += bonus
                            print(f"🎁 Бонус за мастерство: +{bonus} BTC")
                            
                        self.player.bitcoins += reward
                        exp_gain = reward // 2
                        old_level = self.player.add_exp(exp_gain)
                        self.player.add_hack()
                        
                        print("✅ ВЗЛОМ УСПЕШЕН!")
                        print(f"💰 +{reward} BTC")
                        print(f"⭐ +{exp_gain} опыта")
                        
                        if old_level:
                            print(self.player.level_up())
                        
                        # Шанс найти предмет
                        if random.random() < 0.4:
                            items = ["🔑 Ключ шифрования", "💾 Эксплойт", "🛡️ Файрвол", "📡 Сниффер", "⚡ Ускоритель"]
                            item = random.choice(items)
                            self.player.inventory.append(item)
                            self.player.add_item()
                            print(f"🎒 Найден: {item}")
                            
                        # Проверка достижений
                        if reward >= 50000:
                            print(self.player.add_achievement("💎 Мастер взлома"))
                            
                    else:
                        penalty = min(500, self.player.bitcoins // 4)
                        self.player.bitcoins = max(0, self.player.bitcoins - penalty)
                        print("❌ ВЗЛОМ ПРОВАЛЕН!")
                        print(f"💥 Штраф: {penalty} BTC")
                        
                    input("\nНажмите Enter...")
                    
                elif choice == len(targets)+1:
                    return
                else:
                    print("❌ Неверный выбор!")
            except ValueError:
                print("❌ Введите число!")
                
    def shop_menu(self):
        items = [
            {"name": "🔍 Продвинутый сканер", "price": 2000, "skill": "hacking", "bonus": 2, "description": "Увеличивает шанс успешного взлома"},
            {"name": "🛡️  Анонимайзер", "price": 1500, "skill": "stealth", "bonus": 2, "description": "Снижает вероятность обнаружения"},
            {"name": "💻 Компилятор эксплойтов", "price": 3000, "skill": "programming", "bonus": 3, "description": "Позволяет создавать собственные эксплойты"},
            {"name": "📡 DDoS утилита", "price": 2500, "skill": "hacking", "bonus": 1, "description": "Мощный инструмент для атак на серверы"},
            {"name": "🔓 Набор социальной инженерии", "price": 1800, "skill": "social", "bonus": 2, "description": "Помогает получать информацию от людей"},
            {"name": "🕵️  Трекер", "price": 2200, "skill": "investigation", "bonus": 2, "description": "Отслеживание цифровых следов"},
            {"name": "⚡ Квантовый дешифратор", "price": 5000, "skill": "hacking", "bonus": 5, "description": "Передовая технология взлома"},
            {"name": "🧠 Нейроинтерфейс", "price": 8000, "skill": "programming", "bonus": 4, "description": "Прямое подключение к нейросетям"}
        ]
        
        while True:
            self.clear_screen()
            print("🛒 МАГАЗИН ИНСТРУМЕНТОВ")
            print("="*40)
            print(f"💰 Ваш баланс: {self.player.bitcoins} BTC")
            print("="*40)
            print()
            
            for i, item in enumerate(items, 1):
                print(f"{i}. {item['name']} - {item['price']} BTC")
                print(f"   {item['description']}")
                print(f"   Бонус: +{item['bonus']} к {item['skill']}")
                print()
                
            print(f"{len(items)+1}. 🔙 НАЗАД")
            print()
            
            try:
                choice = int(input("Выберите товар: "))
                if 1 <= choice <= len(items):
                    item = items[choice-1]
                    
                    if self.player.bitcoins >= item["price"]:
                        self.player.bitcoins -= item["price"]
                        self.player.skills[item["skill"]] += item["bonus"]
                        self.player.inventory.append(item["name"])
                        self.player.add_item()
                        
                        print(f"✅ Куплено: {item['name']}")
                        print(f"⚡ {item['skill']} повышен до {self.player.skills[item['skill']]}")
                        
                        if item["price"] >= 5000:
                            print(self.player.add_achievement("🛒 Крупный покупатель"))
                            
                    else:
                        print("❌ Недостаточно BTC!")
                        
                    input("\nНажмите Enter...")
                    
                elif choice == len(items)+1:
                    return
                else:
                    print("❌ Неверный выбор!")
            except ValueError:
                print("❌ Введите число!")
                
    def profile_menu(self):
        self.clear_screen()
        print("📊 ПРОФИЛЬ ХАКЕРА")
        print("="*40)
        print(f"👤 Имя: {self.player.name}")
        print(f"🎯 Уровень: {self.player.level}")
        print(f"💰 BTC: {self.player.bitcoins}")
        print(f"⭐ Опыт: {self.player.exp}/{(self.player.level + 1) * 1000}")
        print(f"📖 Прогресс: Глава {self.player.story_progress}/30")
        print(f"📊 Репутация: {self.player.reputation}")
        print(f"🎮 Режим: {'📖 СЮЖЕТНЫЙ' if self.game_mode == 'story' else '🎯 СВОБОДНЫЙ'}")
        print()
        
        print("🛠️  НАВЫКИ:")
        for skill, level in self.player.skills.items():
            print(f"  {skill}: {'⭐' * level} (уровень {level})")
        print()
        
        print("🎒 ИНВЕНТАРЬ:")
        if self.player.inventory:
            for i, item in enumerate(self.player.inventory, 1):
                print(f"  {i}. {item}")
        else:
            print("  Пусто")
        print()
        
        # ПЕРСОНАЛЬНАЯ статистика игрока
        print("📈 ВАША СТАТИСТИКА:")
        stats = self.player.personal_stats
        print(f"  🕐 Время игры: {int(stats['play_time'] // 60)} минут")
        print(f"  🎯 Глав завершено: {stats['chapters_completed']}")
        print(f"  💰 Всего заработано: {stats['total_bitcoins_earned']} BTC")
        print(f"  🌐 Взломов выполнено: {stats['hacks_completed']}")
        print(f"  🎒 Предметов собрано: {stats['items_collected']}")
        print(f"  🏆 Достижений: {stats['achievements_unlocked']}")
        print(f"  📅 Дата начала: {stats['start_date'][:10]}")
        print()
        
        input("Нажмите Enter для возврата...")
        
    def achievements_menu(self):
        self.clear_screen()
        print("🏆 ДОСТИЖЕНИЯ")
        print("="*40)
        print()
        
        all_achievements = [
            "💎 Мастер взлома", "🛒 Крупный покупатель", "🚀 Быстрый старт",
            "🔐 Неуязвимый", "🌐 Сетевой гуру", "💻 Программист-виртуоз",
            "🕵️  Следопыт", "🎯 Снайпер", "💰 Крипто-магнат",
            "🏁 Легенда цифрового мира"
        ]
        
        for achievement in all_achievements:
            if achievement in self.player.achievements:
                print(f"✅ {achievement}")
            else:
                print(f"❌ {achievement} [ЗАБЛОКИРОВАНО]")
        print()
        
        input("Нажмите Enter для возврата...")
    
    def save_specific_game(self, mode):
        """Сохраняет игру в указанном режиме"""
        self.clear_screen()
        print(f"💾 СОХРАНЕНИЕ {'СЮЖЕТА' if mode == 'story' else 'СВОБОДНОГО РЕЖИМА'}")
        print("="*30)
        print()
        
        # Показываем автосохранение
        autosave_file = os.path.join(self.data.save_dir, f"autosave_{mode}.dat")
        if os.path.exists(autosave_file):
            with open(autosave_file, 'rb') as f:
                save_data = pickle.load(f)
            print("0. [АВТОСОХРАНЕНИЕ] - последняя сессия")
        else:
            print("0. [АВТОСОХРАНЕНИЕ] - нет данных")
            
        # Показываем ручные сохранения
        for i in range(1, 4):
            save_file = os.path.join(self.data.save_dir, f"save{i}_{mode}.dat")
            if os.path.exists(save_file):
                with open(save_file, 'rb') as f:
                    save_data = pickle.load(f)
                print(f"{i}. [СОХРАНЕНИЕ {i}] {save_data['player']['name']} - {save_data['timestamp'][:10]}")
            else:
                print(f"{i}. [СОХРАНЕНИЕ {i}] - свободно")
                
        print("5. 🔙 НАЗАД")
        print()
        
        try:
            choice = int(input("Выберите слот: "))
            if 0 <= choice <= 3:
                if self.data.save_game(self.player.__dict__, choice, mode):
                    slot_name = "автосохранение" if choice == 0 else f"слот {choice}"
                    mode_name = "сюжет" if mode == "story" else "свободный режим"
                    print(f"✅ {mode_name} сохранен в {slot_name}!")
                else:
                    print("❌ Ошибка сохранения!")
            elif choice == 5:
                return
            else:
                print("❌ Неверный выбор!")
        except ValueError:
            print("❌ Введите число!")
            
        input("\nНажмите Enter...")
        
    def load_specific_game(self, mode):
        """Загружает игру из указанного режима"""
        saves = self.data.get_saves(mode)
        if not saves:
            print(f"❌ Нет сохранений для {'сюжетного режима' if mode == 'story' else 'свободного режима'}!")
            input("Нажмите Enter...")
            return
            
        self.clear_screen()
        print(f"💾 ЗАГРУЗКА {'СЮЖЕТА' if mode == 'story' else 'СВОБОДНОГО РЕЖИМА'}")
        print("="*30)
        print()
        
        # Показываем автосохранение
        autosave_file = os.path.join(self.data.save_dir, f"autosave_{mode}.dat")
        if os.path.exists(autosave_file):
            with open(autosave_file, 'rb') as f:
                save_data = pickle.load(f)
            print("0. [АВТОСОХРАНЕНИЕ]")
            print(f"   Имя: {save_data['player']['name']} | Ур. {save_data['player']['level']}")
            print(f"   Прогресс: Глава {save_data['player']['story_progress']} | {save_data['timestamp'][:10]}")
            print()
            
        # Показываем ручные сохранения
        for i in range(1, 4):
            save_file = os.path.join(self.data.save_dir, f"save{i}_{mode}.dat")
            if os.path.exists(save_file):
                with open(save_file, 'rb') as f:
                    save_data = pickle.load(f)
                print(f"{i}. [СОХРАНЕНИЕ {i}]")
                print(f"   Имя: {save_data['player']['name']} | Ур. {save_data['player']['level']}")
                print(f"   Прогресс: Глава {save_data['player']['story_progress']} | {save_data['timestamp'][:10]}")
                print()
                
        print("5. 🔙 НАЗАД")
        print()
        
        try:
            choice = int(input("Выберите слот: "))
            if 0 <= choice <= 3:
                save_data = self.data.load_game(choice, mode)
                if save_data:
                    self.player = Player("")
                    self.player.__dict__.update(save_data['player'])
                    self.game_mode = mode
                    print(f"✅ {'Сюжетный режим' if mode == 'story' else 'Свободный режим'} загружен!")
                    input("Нажмите Enter...")
                    
                    if mode == "story":
                        self.play_story_mode()
                    else:
                        self.sandbox_loop()
                else:
                    print("❌ Ошибка загрузки!")
                    input("Нажмите Enter...")
            elif choice == 5:
                return
            else:
                print("❌ Неверный выбор!")
                input("Нажмите Enter...")
        except ValueError:
            print("❌ Введите число!")
            input("Нажмите Enter...")
    
    def load_game_menu(self):
        """Общее меню загрузки с выбором режима"""
        self.clear_screen()
        print("💾 ЗАГРУЗКА ИГРЫ")
        print("="*30)
        print()
        
        # Проверяем сохранения для каждого режима
        story_saves = self.data.get_saves("story")
        sandbox_saves = self.data.get_saves("sandbox")
        
        print("📖 СЮЖЕТНЫЙ РЕЖИМ:")
        if story_saves:
            print("   ✅ Есть сохранения")
        else:
            print("   ❌ Нет сохранений")
            
        print("🎯 СВОБОДНЫЙ РЕЖИМ:")
        if sandbox_saves:
            print("   ✅ Есть сохранения")
        else:
            print("   ❌ Нет сохранений")
        print()
        
        print("1. 📖 Загрузить сюжетный режим")
        print("2. 🎯 Загрузить свободный режим")
        print("3. 🔙 Назад")
        print()
        
        choice = input("Выберите опцию [1-3]: ").strip()
        
        if choice == "1":
            self.load_specific_game("story")
        elif choice == "2":
            self.load_specific_game("sandbox")
        elif choice == "3":
            return
        else:
            print("❌ Неверный выбор!")
            input("Нажмите Enter...")
            
    def check_updates(self):
        """Проверка обновлений через апдейтер"""
        self.clear_screen()
        print("🔄 ПРОВЕРКА ОБНОВЛЕНИЙ")
        print("="*30)
        print()
        
        # Проверяем наличие апдейтера
        if os.path.exists("updater.py"):
            print("✅ Апдейтер найден")
            print("🚀 Запуск проверки обновлений...")
            time.sleep(2)
            
            # Запускаем апдейтер
            os.system("python3 updater.py")
        else:
            print("❌ Апдейтер не найден")
            print("📥 Скачайте последнюю версию с GitHub")
            print("🌐 https://github.com/yourusername/terminal-shadows")
            
        input("\nНажмите Enter для возврата...")
            
    def settings_menu(self):
        while True:
            self.clear_screen()
            print("⚙️  НАСТРОЙКИ")
            print("="*30)
            print(f"Язык: {self.data.config['language']}")
            print(f"Сложность: {self.data.config['difficulty']}")
            print(f"Автосохранение: {'Вкл' if self.data.config['autosave'] else 'Выкл'}")
            print(f"Анимации: {'Вкл' if self.data.config['animations'] else 'Выкл'}")
            print()
            print("1. Сменить язык")
            print("2. Изменить сложность")
            print("3. Автосохранение")
            print("4. Анимации")
            print("5. 🗑️  СБРОС СОХРАНЕНИЙ")
            print("6. 🔙 НАЗАД")
            print()
            
            choice = input("Выберите опцию [1-6]: ").strip()
            
            if choice == "1":
                self.data.config['language'] = "ru" if self.data.config['language'] == "en" else "en"
                self.data.save_config()
                print("✅ Язык изменен!")
                input()
            elif choice == "2":
                difficulties = ["легкая", "нормальная", "сложная"]
                current = self.data.config['difficulty']
                next_diff = difficulties[(difficulties.index(current) + 1) % len(difficulties)]
                self.data.config['difficulty'] = next_diff
                self.data.save_config()
                print(f"✅ Сложность изменена на {next_diff}!")
                input()
            elif choice == "3":
                self.data.config['autosave'] = not self.data.config['autosave']
                self.data.save_config()
                print(f"✅ Автосохранение: {'включено' if self.data.config['autosave'] else 'выключено'}!")
                input()
            elif choice == "4":
                self.data.config['animations'] = not self.data.config['animations']
                self.data.save_config()
                print(f"✅ Анимации: {'включены' if self.data.config['animations'] else 'выключены'}!")
                input()
            elif choice == "5":
                if input("❌ Удалить ВСЕ сохранения? (y/N): ").lower() == 'y':
                    # Удаляем все сохранения
                    for mode in ["story", "sandbox"]:
                        # Удаляем автосохранение
                        autosave_file = os.path.join(self.data.save_dir, f"autosave_{mode}.dat")
                        if os.path.exists(autosave_file):
                            os.remove(autosave_file)
                        # Удаляем ручные сохранения
                        for i in range(1, 4):
                            save_file = os.path.join(self.data.save_dir, f"save{i}_{mode}.dat")
                            if os.path.exists(save_file):
                                os.remove(save_file)
                    print("✅ Все сохранения удалены!")
                    input()
            elif choice == "6":
                return
            else:
                print("❌ Неверный выбор!")
                input("Нажмите Enter...")
                
    def show_stats(self):
        self.clear_screen()
        print("📊 ГЛОБАЛЬНАЯ СТАТИСТИКА")
        print("="*30)
        print()
        print(f"🎮 Всего глав: {len(chapters)}")
        print("🎯 Целей для взлома: 8")
        print("🛒 Товаров в магазине: 8")
        print("⚡ Навыков для прокачки: 5")
        print("🏆 Достижений: 10")
        print("💾 Режимы: СЮЖЕТНЫЙ и СВОБОДНЫЙ")
        print()
        print("🚀 Особенности:")
        print("  • 30 глав эпического сюжета")
        print("  • Свободный режим с бесконечными возможностями")
        print("  • Раздельная система сохранений")
        print("  • Автосохранения после каждой главы")
        print("  • Персональная статистика для каждого игрока")
        print()
        input("Нажмите Enter для возврата...")
        
    def game_complete(self):
        self.clear_screen()
        print("🎊 ПОЗДРАВЛЯЕМ!")
        print("="*30)
        print()
        print("🏁 ВЫ ЗАВЕРШИЛИ СЮЖЕТНЫЙ РЕЖИМ TERMINAL SHADOWS!")
        print()
        print("📊 ВАШИ РЕЗУЛЬТАТЫ:")
        print(f"  👤 Имя: {self.player.name}")
        print(f"  🎯 Финальный уровень: {self.player.level}")
        print(f"  💰 Накоплено BTC: {self.player.bitcoins}")
        print(f"  🏆 Достижений: {len(self.player.achievements)}/10")
        print(f"  📖 Пройдено глав: 30/30")
        print()
        
        # Финальная статистика
        stats = self.player.personal_stats
        print("📈 ВАША ФИНАЛЬНАЯ СТАТИСТИКА:")
        print(f"  🕐 Всего времени в игре: {int(stats['play_time'] // 60)} минут")
        print(f"  💰 Всего заработано BTC: {stats['total_bitcoins_earned']}")
        print(f"  🌐 Выполнено взломов: {stats['hacks_completed']}")
        print(f"  🎒 Собрано предметов: {stats['items_collected']}")
        print()
        
        print("🌟 Спасибо за игру!")
        print("Теперь доступен СВОБОДНЫЙ РЕЖИМ с полным функционалом!")
        print()
        input("Нажмите Enter чтобы продолжить...")
        self.sandbox_loop()
            
    def exit_game(self):
        # Обновляем время игры перед выходом
        play_time = time.time() - self.start_time
        if self.player:
            self.player.update_play_time(play_time)
            # Сохраняем игру при выходе
            if self.data.config.get("autosave", True) and self.game_mode:
                self.data.save_game(self.player.__dict__, 0, self.game_mode)
        
        self.clear_screen()
        print("👋 До новых встреч в цифровом подполье!")
        print("TERMINAL SHADOWS: DIGITAL GHOST v3.0")
        if self.player:
            print(f"🕐 Всего сыграно: {int(self.player.personal_stats['play_time'] // 60)} минут")
        time.sleep(2)
        sys.exit(0)

if __name__ == "__main__":
    try:
        game = GameEngine()
        game.show_main_menu()
    except KeyboardInterrupt:
        print("\n👋 Выход...")
        game.exit_game()
    except Exception as e:
        print(f"\n❌ Критическая ошибка: {e}")
        import traceback
        traceback.print_exc()
