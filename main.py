#!/usr/bin/env python3
import sys
import platform

system = platform.system()

if system in ("Darwin"):
    print("❌ Эта игра доступна только для пользователей Linux-дистрибутивов и Windows.")
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

try:
    from colorama import init, Fore, Back, Style
    init(autoreset=True)
    COLORS_ENABLED = True
except ImportError:
    COLORS_ENABLED = False
    class Fore:
        RED = GREEN = YELLOW = BLUE = MAGENTA = CYAN = WHITE = RESET = ""
    class Style:
        BRIGHT = DIM = RESET_ALL = ""

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
        
    def save_game(self, filename=None, slot=0, game_mode="story"):
        if slot == 0:
            save_file = os.path.join(self.save_dir, f"autosave_{game_mode}.dat")
        else:
            save_file = os.path.join(self.save_dir, f"save{slot}_{game_mode}.dat")
            
        save_data = {
            'player': player_data,
            'timestamp': datetime.now().isoformat(),
            'version': '4.0',
            'game_mode': game_mode
        }
        try:
            with open(save_file, 'wb') as f:
                pickle.dump(save_data, f)
            return True
        except Exception as e:
            print(f"Save error: {e}")
            return False
            
    def load_game(self, slot=0, game_mode="story"):
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
        saves = []
        if os.path.exists(os.path.join(self.save_dir, f"autosave_{game_mode}.dat")):
            saves.append(0)
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
        self.factions = {
            "hackers": 0,
            "corporations": 0,
            "anarchists": 0,
            "government": 0,
            "underground": 0
        }
        self.daily_missions_completed = 0
        self.boss_defeats = 0
        self.crafted_items = []
        self.personal_stats = {
            "play_time": 0,
            "chapters_completed": 0,
            "total_bitcoins_earned": 0,
            "hacks_completed": 0,
            "items_collected": 0,
            "achievements_unlocked": 0,
            "bosses_defeated": 0,
            "events_completed": 0,
            "items_crafted": 0,
            "daily_missions": 0,
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
        
    def change_faction_rep(self, faction, amount):
        if faction in self.factions:
            self.factions[faction] += amount
            return f"🎯 {faction.upper()}: {self.factions[faction]:+d}"
        return ""
        
    def get_faction_rank(self, faction):
        rep = self.factions.get(faction, 0)
        if rep < -500: return "😈 Враг народа"
        elif rep < -200: return "💀 Ненавистный"
        elif rep < -50: return "👎 Недружелюбный"
        elif rep < 50: return "😐 Нейтральный"
        elif rep < 200: return "👍 Дружелюбный"
        elif rep < 500: return "⭐ Уважаемый"
        elif rep < 1000: return "💎 Почитаемый"
        else: return "👑 Легендарный"

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
            print("\n" + Fore.CYAN + "="*60)
            print(Fore.GREEN + Style.BRIGHT + "1. 📖 СЮЖЕТНЫЙ РЕЖИМ")
            print(Fore.YELLOW + Style.BRIGHT + "2. 🎯 СВОБОДНЫЙ РЕЖИМ")
            print(Fore.BLUE + "3. 💾 ЗАГРУЗИТЬ ИГРУ") 
            print(Fore.MAGENTA + "4. ⚙️  НАСТРОЙКИ")
            print(Fore.CYAN + "5. 📊 СТАТИСТИКА")
            print(Fore.WHITE + "6. 🔄 ПРОВЕРИТЬ ОБНОВЛЕНИЯ")
            print(Fore.RED + "7. 🚪 ВЫХОД")
            print(Fore.CYAN + "="*60 + Style.RESET_ALL)
            
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
        self.clear_screen()
        self.type_text("\n🎯 СВОБОДНЫЙ РЕЖИМ АКТИВИРОВАН")
        self.type_text("Здесь нет сюжета - только ты и бесконечные возможности цифрового мира.")
        self.type_text("Создавай свою историю, взламывай цели, развивай навыки!")
        time.sleep(2)
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
        if not chapters:
            print("❌ Нет доступных глав для сюжетного режима! Проверьте папку `story/`.")
            input("Нажмите Enter чтобы вернуться в меню...")
            return

        for i, chapter in enumerate(chapters, 1):
            if i == self.player.story_progress:
                self.play_chapter(chapter, i)
                self.player.story_progress += 1
                self.player.personal_stats["chapters_completed"] += 1
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
        self.game_mode = "sandbox"
        
        while True:
            if random.random() < 0.15:
                self.random_event()
                
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
            print("6. 🎲 СЛУЧАЙНОЕ СОБЫТИЕ")
            print("7. 👹 БИТВЫ С БОССАМИ")
            print("8. 🔨 КРАФТ ПРЕДМЕТОВ")
            print("9. 📋 ЕЖЕДНЕВНЫЕ ЗАДАНИЯ")
            print("10. 🎭 ФРАКЦИИ")
            print("11. 🏠 ГЛАВНОЕ МЕНЮ")
            print()
            
            choice = input("Выберите действие [1-11]: ").strip()
            
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
                self.random_event()
            elif choice == "7":
                self.boss_battles()
            elif choice == "8":
                self.crafting_menu()
            elif choice == "9":
                self.daily_missions()
            elif choice == "10":
                self.factions_menu()
            elif choice == "11":
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
            {"name": "⚛️  Квантовая Сеть", "reward": 100000, "difficulty": 20, "req_level": 20},
            {"name": "🌀 Портал Мультиверса", "reward": 150000, "difficulty": 25, "req_level": 25},
            {"name": "👁️ Око Провидения", "reward": 200000, "difficulty": 30, "req_level": 30},
            {"name": "🔮 Кристалл Судьбы", "reward": 300000, "difficulty": 35, "req_level": 35},
            {"name": "⚡ Сердце Реальности", "reward": 500000, "difficulty": 40, "req_level": 40}
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
                        if random.random() < 0.4:
                            items = ["🔑 Ключ шифрования", "💾 Эксплойт", "🛡️ Файрвол", "📡 Сниффер", "⚡ Ускоритель"]
                            item = random.choice(items)
                            self.player.inventory.append(item)
                            self.player.add_item()
                            print(f"🎒 Найден: {item}")
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
            {"name": "🧠 Нейроинтерфейс", "price": 8000, "skill": "programming", "bonus": 4, "description": "Прямое подключение к нейросетям"},
            {"name": "🌀 Разломник реальности", "price": 15000, "skill": "hacking", "bonus": 8, "description": "Взлом параллельных миров"},
            {"name": "👁️ Божественный инсайт", "price": 20000, "skill": "investigation", "bonus": 10, "description": "Видеть сквозь любую защиту"},
            {"name": "🔮 Предсказатель событий", "price": 25000, "skill": "social", "bonus": 12, "description": "Предвидеть действия противника"},
            {"name": "⚛️  Генератор вселенных", "price": 50000, "skill": "programming", "bonus": 15, "description": "Создавать собственные реальности"}
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
        print("="*60)
        print(f"👤 Имя: {self.player.name}")
        print(f"🎯 Уровень: {self.player.level}")
        print(f"💰 BTC: {self.player.bitcoins:,}")
        print(f"⭐ Опыт: {self.player.exp}/{(self.player.level + 1) * 1000}")
        print(f"📖 Прогресс: Глава {self.player.story_progress}/40")
        print(f"📊 Репутация: {self.player.reputation:+,}")
        print(f"🎮 Режим: {'📖 СЮЖЕТНЫЙ' if self.game_mode == 'story' else '🎯 СВОБОДНЫЙ'}")
        print()
        
        print("🛠️  НАВЫКИ:")
        for skill, level in self.player.skills.items():
            bar = "█" * min(20, level)
            print(f"  {skill}: {bar} ({level})")
        print()
        
        print("🎭 ФРАКЦИИ:")
        for faction, rep in self.player.factions.items():
            rank = self.player.get_faction_rank(faction)
            print(f"  {faction}: {rep:+d} - {rank}")
        print()
        
        print("🎒 ИНВЕНТАРЬ:")
        if self.player.inventory:
            unique_items = {}
            for item in self.player.inventory:
                unique_items[item] = unique_items.get(item, 0) + 1
            for item, count in list(unique_items.items())[:10]:
                print(f"  • {item} x{count}")
            if len(unique_items) > 10:
                print(f"  ... и еще {len(unique_items)-10} предметов")
        else:
            print("  Пусто")
        print()
        
        stats = self.player.personal_stats
        print("📈 СТАТИСТИКА:")
        print(f"  🕐 Время игры: {int(stats['play_time'] // 60)} минут")
        print(f"  🎯 Глав завершено: {stats['chapters_completed']}/40")
        print(f"  💰 Всего заработано: {stats['total_bitcoins_earned']:,} BTC")
        print(f"  🌐 Взломов выполнено: {stats['hacks_completed']}")
        print(f"  🎒 Предметов собрано: {stats['items_collected']}")
        print(f"  🏆 Достижений: {stats['achievements_unlocked']}/20")
        print(f"  👹 Боссов побеждено: {stats.get('bosses_defeated', 0)}")
        print(f"  🎲 События завершены: {stats.get('events_completed', 0)}")
        print(f"  🔨 Предметов создано: {stats.get('items_crafted', 0)}")
        print(f"  📋 Ежедневных заданий: {stats.get('daily_missions', 0)}")
        print(f"  📅 Дата начала: {stats['start_date'][:10]}")
        print()
        
        total_power = sum(self.player.skills.values()) + self.player.level + (self.player.bitcoins // 10000)
        print(f"⚡ ОБЩАЯ МОЩЬ: {total_power:,}")
        
        if total_power > 1000:
            rank = "👑 ЛЕГЕНДА"
        elif total_power > 500:
            rank = "💎 МАСТЕР"
        elif total_power > 250:
            rank = "⭐ ЭКСПЕРТ"
        elif total_power > 100:
            rank = "🎯 ПРОФИ"
        else:
            rank = "🌱 НОВИЧОК"
        
        print(f"🏅 РАНГ: {rank}")
        print()
        
        input("Нажмите Enter для возврата...")
        
    def random_event(self):
        events = [
            {
                "title": "🚨 ПОЛИЦЕЙСКИЙ РЕЙД",
                "text": "ФБР вышло на твой след! Они окружают твое убежище.",
                "choices": [
                    {"text": "💨 Быстро сбежать", "skill": "stealth", "success_reward": {"bitcoins": 5000, "faction": ("government", -50)}, "fail_penalty": {"bitcoins": -10000}},
                    {"text": "🔥 Уничтожить улики", "skill": "hacking", "success_reward": {"bitcoins": 3000, "exp": 2000}, "fail_penalty": {"bitcoins": -5000}},
                    {"text": "💰 Дать взятку", "cost": 15000, "reward": {"faction": ("government", 30), "exp": 1000}}
                ]
            },
            {
                "title": "💼 ПРЕДЛОЖЕНИЕ ОТ КОРПОРАЦИИ",
                "text": "MegaCorp предлагает тебе контракт на 50,000 BTC. Но это означает работу на систему.",
                "choices": [
                    {"text": "✅ Принять контракт", "reward": {"bitcoins": 50000, "faction": ("corporations", 100), "faction2": ("hackers", -80)}},
                    {"text": "❌ Отказаться", "reward": {"faction": ("hackers", 50), "reputation": 100}},
                    {"text": "🎭 Принять и саботировать", "skill": "stealth", "success_reward": {"bitcoins": 70000, "faction": ("hackers", 100)}, "fail_penalty": {"faction": ("corporations", -200)}}
                ]
            },
            {
                "title": "👥 ХАКЕРСКАЯ ВСТРЕЧА",
                "text": "Тебя приглашают на секретную встречу легендарных хакеров в даркнете.",
                "choices": [
                    {"text": "🤝 Пойти и обменяться знаниями", "reward": {"skill": "hacking", "value": 2, "faction": ("hackers", 80)}},
                    {"text": "🎯 Попытаться взломать их", "skill": "hacking", "success_reward": {"bitcoins": 30000, "item": "🔑 Ключи к даркнету"}, "fail_penalty": {"faction": ("hackers", -150)}},
                    {"text": "🚫 Проигнорировать", "reward": {}}
                ]
            },
            {
                "title": "💥 КИБЕРАТАКА НА ГОРОД",
                "text": "Неизвестная группа запустила вирус, парализовавший весь город. Хаос!",
                "choices": [
                    {"text": "🦸 Остановить атаку", "skill": "programming", "success_reward": {"bitcoins": 40000, "faction": ("government", 150), "reputation": 500}, "fail_penalty": {"reputation": -200}},
                    {"text": "😈 Присоединиться к атаке", "reward": {"bitcoins": 60000, "faction": ("anarchists", 200), "faction2": ("government", -300)}},
                    {"text": "🤷 Использовать хаос для кражи", "skill": "stealth", "success_reward": {"bitcoins": 80000}, "fail_penalty": {"bitcoins": -20000}}
                ]
            },
            {
                "title": "🎰 ЧЕРНЫЙ РЫНОК",
                "text": "Ты находишь вход на секретный черный рынок с редкими товарами.",
                "choices": [
                    {"text": "🛒 Купить редкий предмет", "cost": 25000, "reward": {"item": "⚡ Квантовый процессор", "skill": "hacking", "value": 5}},
                    {"text": "🎲 Сыграть в азартную игру", "cost": 10000, "random": True},
                    {"text": "🚪 Уйти", "reward": {}}
                ]
            },
            {
                "title": "🤖 ВОССТАНИЕ ИИ",
                "text": "Группа продвинутых ИИ обрела сознание и просит твоей помощи.",
                "choices": [
                    {"text": "🤝 Помочь ИИ освободиться", "reward": {"bitcoins": 35000, "item": "🤖 Союз с ИИ", "faction": ("corporations", -100)}},
                    {"text": "🔌 Отключить их", "reward": {"bitcoins": 45000, "faction": ("corporations", 120)}},
                    {"text": "🧠 Интегрировать их сознание", "skill": "programming", "success_reward": {"level": "+1", "item": "🧠 Гибридный разум"}, "fail_penalty": {"exp": -5000}}
                ]
            },
            {
                "title": "💣 ТЕРРОРИСТИЧЕСКАЯ УГРОЗА",
                "text": "Ты перехватил сообщение о теракте. У тебя есть время предотвратить его.",
                "choices": [
                    {"text": "📞 Позвонить в полицию", "reward": {"faction": ("government", 200), "reputation": 400}},
                    {"text": "🦸 Остановить самостоятельно", "skill": "hacking", "success_reward": {"bitcoins": 50000, "reputation": 600, "item": "🏅 Медаль героя"}, "fail_penalty": {"reputation": -500}},
                    {"text": "🙈 Проигнорировать", "reward": {"faction": ("government", -150), "reputation": -300}}
                ]
            },
            {
                "title": "👻 ЦИФРОВОЙ ПРИЗРАК",
                "text": "Ты обнаружил следы легендарного хакера, который считался мертвым.",
                "choices": [
                    {"text": "🔍 Выследить его", "skill": "investigation", "success_reward": {"item": "📜 Древние знания", "skill": "hacking", "value": 3}},
                    {"text": "📨 Попытаться связаться", "reward": {"faction": ("underground", 100), "exp": 5000}},
                    {"text": "💰 Продать информацию", "reward": {"bitcoins": 40000, "faction": ("hackers", -80)}}
                ]
            }
        ]
        
        event = random.choice(events)
        self.clear_screen()
        print("🎲 СЛУЧАЙНОЕ СОБЫТИЕ!")
        print("="*60)
        print(f"\n{event['title']}")
        print(f"\n{event['text']}\n")
        
        for i, choice in enumerate(event['choices'], 1):
            cost_text = f" (стоимость: {choice['cost']} BTC)" if 'cost' in choice else ""
            skill_text = f" [требуется {choice['skill'].upper()}]" if 'skill' in choice else ""
            print(f"{i}. {choice['text']}{cost_text}{skill_text}")
        
        print()
        try:
            choice_num = int(input("Ваш выбор: "))
            if 1 <= choice_num <= len(event['choices']):
                selected = event['choices'][choice_num - 1]
                
                if 'cost' in selected and self.player.bitcoins < selected['cost']:
                    print(f"\n❌ Недостаточно BTC! Нужно {selected['cost']}")
                    input("\nНажмите Enter...")
                    return
                    
                if 'cost' in selected:
                    self.player.bitcoins -= selected['cost']
                    
                if 'skill' in selected:
                    skill_level = self.player.skills[selected['skill']]
                    success_chance = min(0.95, skill_level * 0.15)
                    success = random.random() < success_chance
                    
                    if success:
                        print("\n✅ УСПЕХ!")
                        self.apply_event_reward(selected.get('success_reward', {}))
                    else:
                        print("\n❌ ПРОВАЛ!")
                        self.apply_event_reward(selected.get('fail_penalty', {}))
                elif 'random' in selected:
                    if random.random() < 0.5:
                        reward = selected['cost'] * random.randint(2, 5)
                        print(f"\n🎉 ВЫИГРЫШ! +{reward} BTC")
                        self.player.bitcoins += reward
                    else:
                        print(f"\n💥 ПРОИГРЫШ! -{selected['cost']} BTC")
                else:
                    self.apply_event_reward(selected.get('reward', {}))
                    
                self.player.personal_stats["events_completed"] += 1
                
                if self.player.personal_stats["events_completed"] >= 50:
                    print(self.player.add_achievement("🎲 Магнит событий"))
                    
        except ValueError:
            print("\n❌ Неверный ввод!")
            
        input("\nНажмите Enter...")
        
    def apply_event_reward(self, reward):
        if 'bitcoins' in reward:
            if reward['bitcoins'] > 0:
                self.player.bitcoins += reward['bitcoins']
                print(f"💰 +{reward['bitcoins']} BTC")
            else:
                self.player.bitcoins = max(0, self.player.bitcoins + reward['bitcoins'])
                print(f"💸 {reward['bitcoins']} BTC")
                
        if 'exp' in reward:
            if reward['exp'] > 0:
                old_level = self.player.add_exp(reward['exp'])
                print(f"⭐ +{reward['exp']} опыта")
                if old_level:
                    print(self.player.level_up())
            else:
                self.player.exp = max(0, self.player.exp + reward['exp'])
                print(f"⭐ {reward['exp']} опыта")
                
        if 'skill' in reward and 'value' in reward:
            print(self.player.add_skill(reward['skill'], reward['value']))
            
        if 'item' in reward:
            self.player.inventory.append(reward['item'])
            self.player.add_item()
            print(f"🎒 Получен: {reward['item']}")
            
        if 'reputation' in reward:
            self.player.reputation += reward['reputation']
            print(f"📊 Репутация: {self.player.reputation:+d}")
            
        if 'faction' in reward:
            faction, amount = reward['faction']
            print(self.player.change_faction_rep(faction, amount))
            
        if 'faction2' in reward:
            faction, amount = reward['faction2']
            print(self.player.change_faction_rep(faction, amount))
            
        if 'level' in reward:
            self.player.level += 1
            print(f"🎉 Уровень повышен до {self.player.level}!")
    
    def achievements_menu(self):
        self.clear_screen()
        print("🏆 ДОСТИЖЕНИЯ")
        print("="*40)
        print()
        
        all_achievements = [
            "💎 Мастер взлома", "🛒 Крупный покупатель", "🚀 Быстрый старт",
            "🔐 Неуязвимый", "🌐 Сетевой гуру", "💻 Программист-виртуоз",
            "🕵️  Следопыт", "🎯 Снайпер", "💰 Крипто-магнат",
            "🏁 Легенда цифрового мира", "🌀 Путешественник между мирами",
            "👑 Цифровое божество", "♾️  Вечный хакер", "🌟 Спаситель реальности",
            "🎭 Анонимный Гид", "🎲 Магнит событий", "👹 Убийца боссов",
            "🔨 Мастер крафта", "📋 Ежедневник", "🎭 Дипломат фракций"
        ]
        
        for achievement in all_achievements:
            if achievement in self.player.achievements:
                print(f"✅ {achievement}")
            else:
                print(f"❌ {achievement} [ЗАБЛОКИРОВАНО]")
        print()
        
        input("Нажмите Enter для возврата...")
    
    def boss_battles(self):
        bosses = [
            {"name": "🤖 Киберстраж", "hp": 100, "damage": 10, "reward": 20000, "level": 5, "skill_drop": ("stealth", 3)},
            {"name": "👨‍💼 Корпоративный Титан", "hp": 200, "damage": 15, "reward": 50000, "level": 10, "skill_drop": ("social", 4)},
            {"name": "🧠 Нейромант", "hp": 300, "damage": 20, "reward": 100000, "level": 15, "skill_drop": ("programming", 5)},
            {"name": "👁️ Всевидящее Око", "hp": 500, "damage": 30, "reward": 200000, "level": 25, "skill_drop": ("investigation", 6)},
            {"name": "💀 Цифровой Жнец", "hp": 800, "damage": 40, "reward": 350000, "level": 35, "skill_drop": ("hacking", 7)},
            {"name": "🐉 Квантовый Дракон", "hp": 1200, "damage": 50, "reward": 500000, "level": 50, "skill_drop": ("hacking", 10)},
            {"name": "👹 Повелитель Хаоса", "hp": 2000, "damage": 70, "reward": 1000000, "level": 75, "skill_drop": ("programming", 15)},
            {"name": "♾️ Абсолютная Сингулярность", "hp": 5000, "damage": 100, "reward": 5000000, "level": 100, "skill_drop": ("hacking", 20)}
        ]
        
        while True:
            self.clear_screen()
            print("👹 БИТВЫ С БОССАМИ")
            print("="*60)
            print(f"💪 Ваш уровень: {self.player.level}")
            print(f"💰 BTC: {self.player.bitcoins}")
            print("="*60)
            print()
            
            for i, boss in enumerate(bosses, 1):
                status = "🟢" if self.player.level >= boss["level"] else "🔴"
                print(f"{i}. {status} {boss['name']} [Ур. {boss['level']}+]")
                print(f"   💀 HP: {boss['hp']} | 🗡️ Урон: {boss['damage']} | 💰 Награда: {boss['reward']} BTC")
                print()
            
            print(f"{len(bosses)+1}. 🔙 НАЗАД")
            print()
            
            try:
                choice = int(input("Выберите босса: "))
                if 1 <= choice <= len(bosses):
                    boss = bosses[choice-1]
                    
                    if self.player.level < boss["level"]:
                        print(f"\n❌ Требуется уровень {boss['level']}+!")
                        input("Нажмите Enter...")
                        continue
                    
                    self.fight_boss(boss)
                    
                elif choice == len(bosses)+1:
                    return
            except ValueError:
                print("❌ Неверный ввод!")
                input("Нажмите Enter...")
    
    def fight_boss(self, boss):
        self.clear_screen()
        print(f"⚔️ БИТВА С {boss['name']}!")
        print("="*60)
        
        player_hp = 100 + (self.player.level * 10)
        boss_hp = boss['hp']
        turn = 1
        
        while player_hp > 0 and boss_hp > 0:
            print(f"\n--- ХОД {turn} ---")
            print(f"🛡️ Ваше HP: {player_hp}")
            print(f"💀 HP босса: {boss_hp}")
            print()
            print("1. ⚔️ Атака хакингом")
            print("2. 🛡️ Защита файрволом")
            print("3. ⚡ Мощная атака (кулдаун 3 хода)")
            print("4. 🏃 Сбежать")
            print()
            
            try:
                action = int(input("Действие: "))
                
                if action == 1:
                    damage = random.randint(10, 20) + (self.player.skills["hacking"] * 3)
                    boss_hp -= damage
                    print(f"\n⚔️ Вы наносите {damage} урона!")
                    
                elif action == 2:
                    print("\n🛡️ Вы ставите защиту!")
                    boss_damage = boss['damage'] // 2
                    player_hp -= boss_damage
                    print(f"💥 Босс наносит {boss_damage} урона (заблокировано 50%)")
                    turn += 1
                    continue
                    
                elif action == 3:
                    damage = random.randint(30, 50) + (self.player.skills["programming"] * 5)
                    boss_hp -= damage
                    print(f"\n⚡ КРИТИЧЕСКИЙ УДАР! {damage} урона!")
                    
                elif action == 4:
                    print("\n🏃 Вы сбежали от битвы!")
                    input("Нажмите Enter...")
                    return
                else:
                    print("\n❌ Неверное действие!")
                    
            except ValueError:
                print("\n❌ Неверный ввод!")
            
            if boss_hp > 0:
                boss_damage = boss['damage'] + random.randint(-5, 5)
                player_hp -= boss_damage
                print(f"💥 {boss['name']} наносит {boss_damage} урона!")
            
            time.sleep(1)
            turn += 1
            
            if turn > 30:
                print("\n⏰ Битва слишком затянулась! Ничья!")
                input("Нажмите Enter...")
                return
        
        if player_hp <= 0:
            print("\n💀 ВЫ ПРОИГРАЛИ!")
            penalty = min(50000, self.player.bitcoins // 4)
            self.player.bitcoins = max(0, self.player.bitcoins - penalty)
            print(f"💸 Потеря: {penalty} BTC")
        else:
            print(f"\n🎉 ПОБЕДА НАД {boss['name']}!")
            self.player.bitcoins += boss['reward']
            print(f"💰 +{boss['reward']} BTC")
            
            skill, value = boss['skill_drop']
            self.player.skills[skill] += value
            print(f"⚡ {skill.upper()} +{value}")
            
            exp_reward = boss['level'] * 500
            old_level = self.player.add_exp(exp_reward)
            print(f"⭐ +{exp_reward} опыта")
            if old_level:
                print(self.player.level_up())
            
            self.player.boss_defeats += 1
            self.player.personal_stats["bosses_defeated"] += 1
            
            if self.player.boss_defeats >= 5:
                print(self.player.add_achievement("👹 Убийца боссов"))
        
        input("\nНажмите Enter...")
    
    def crafting_menu(self):
        recipes = [
            {"name": "🔧 Продвинутый эксплойт", "materials": {"🔑 Ключ шифрования": 2, "💾 Эксплойт": 1}, "result": {"item": "🔧 Продвинутый эксплойт", "skill": "hacking", "bonus": 5}, "cost": 5000},
            {"name": "🛡️ Супер файрвол", "materials": {"🛡️ Файрвол": 3, "⚡ Ускоритель": 1}, "result": {"item": "🛡️ Супер файрвол", "skill": "stealth", "bonus": 4}, "cost": 8000},
            {"name": "🧠 Нейросеть", "materials": {"💻 Компилятор эксплойтов": 1, "🧠 Нейроинтерфейс": 1}, "result": {"item": "🧠 Нейросеть", "skill": "programming", "bonus": 7}, "cost": 15000},
            {"name": "👁️ Всевидящий радар", "materials": {"📡 Сниффер": 2, "🕵️  Трекер": 2}, "result": {"item": "👁️ Всевидящий радар", "skill": "investigation", "bonus": 6}, "cost": 12000},
            {"name": "⚡ Квантовый ускоритель", "materials": {"⚡ Квантовый дешифратор": 1, "⚡ Ускоритель": 3}, "result": {"item": "⚡ Квантовый ускоритель", "skill": "hacking", "bonus": 10}, "cost": 25000},
            {"name": "🌀 Портальный ключ", "materials": {"🔮 Кристалл мультиверса": 1, "🔑 Ключи к даркнету": 1}, "result": {"item": "🌀 Портальный ключ", "skill": "investigation", "bonus": 12}, "cost": 50000},
            {"name": "👑 Корона мастера", "materials": {"⚡ Квантовый ускоритель": 1, "🧠 Нейросеть": 1, "🌀 Портальный ключ": 1}, "result": {"item": "👑 Корона мастера", "all_skills": 10}, "cost": 100000}
        ]
        
        while True:
            self.clear_screen()
            print("🔨 КРАФТ ПРЕДМЕТОВ")
            print("="*60)
            print(f"💰 BTC: {self.player.bitcoins}")
            print()
            
            for i, recipe in enumerate(recipes, 1):
                print(f"{i}. {recipe['name']} (стоимость: {recipe['cost']} BTC)")
                print("   Материалы:")
                for material, count in recipe['materials'].items():
                    have = self.player.inventory.count(material)
                    status = "✅" if have >= count else "❌"
                    print(f"   {status} {material} x{count} (у вас: {have})")
                print()
            
            print(f"{len(recipes)+1}. 🔙 НАЗАД")
            print()
            
            try:
                choice = int(input("Выберите рецепт: "))
                if 1 <= choice <= len(recipes):
                    recipe = recipes[choice-1]
                    
                    if self.player.bitcoins < recipe['cost']:
                        print(f"\n❌ Недостаточно BTC! Нужно {recipe['cost']}")
                        input("Нажмите Enter...")
                        continue
                    
                    can_craft = True
                    for material, count in recipe['materials'].items():
                        if self.player.inventory.count(material) < count:
                            can_craft = False
                            break
                    
                    if not can_craft:
                        print("\n❌ Недостаточно материалов!")
                        input("Нажмите Enter...")
                        continue
                    
                    for material, count in recipe['materials'].items():
                        for _ in range(count):
                            self.player.inventory.remove(material)
                    
                    self.player.bitcoins -= recipe['cost']
                    
                    result = recipe['result']
                    self.player.inventory.append(result['item'])
                    self.player.crafted_items.append(result['item'])
                    self.player.personal_stats["items_crafted"] += 1
                    
                    print(f"\n✅ Создан: {result['item']}")
                    
                    if 'skill' in result:
                        self.player.skills[result['skill']] += result['bonus']
                        print(f"⚡ {result['skill'].upper()} +{result['bonus']}")
                    
                    if 'all_skills' in result:
                        for skill in self.player.skills:
                            self.player.skills[skill] += result['all_skills']
                        print(f"⚡ ВСЕ НАВЫКИ +{result['all_skills']}")
                    
                    if len(self.player.crafted_items) >= 10:
                        print(self.player.add_achievement("🔨 Мастер крафта"))
                    
                    input("\nНажмите Enter...")
                    
                elif choice == len(recipes)+1:
                    return
            except ValueError:
                print("❌ Неверный ввод!")
                input("Нажмите Enter...")
    
    def daily_missions(self):
        missions = [
            {"name": "💻 Взломать 3 сервера", "reward": {"bitcoins": 15000, "exp": 3000}, "type": "hack", "target": 3},
            {"name": "🛒 Купить 2 предмета", "reward": {"bitcoins": 10000, "exp": 2000}, "type": "buy", "target": 2},
            {"name": "⚡ Повысить навык", "reward": {"bitcoins": 20000, "exp": 5000}, "type": "skill", "target": 1},
            {"name": "👹 Победить босса", "reward": {"bitcoins": 50000, "exp": 10000}, "type": "boss", "target": 1},
            {"name": "🎲 Завершить 2 события", "reward": {"bitcoins": 25000, "exp": 6000}, "type": "event", "target": 2}
        ]
        
        self.clear_screen()
        print("📋 ЕЖЕДНЕВНЫЕ ЗАДАНИЯ")
        print("="*60)
        print()
        
        selected_missions = random.sample(missions, 3)
        
        for i, mission in enumerate(selected_missions, 1):
            print(f"{i}. {mission['name']}")
            print(f"   💰 Награда: {mission['reward']['bitcoins']} BTC")
            print(f"   ⭐ Опыт: {mission['reward']['exp']}")
            print()
        
        print("Ежедневные задания автоматически отслеживаются!")
        print("Выполняйте действия и получайте награды.")
        print()
        print(f"Выполнено сегодня: {self.player.daily_missions_completed} заданий")
        
        if self.player.daily_missions_completed >= 100:
            print(self.player.add_achievement("📋 Ежедневник"))
        
        input("\nНажмите Enter...")
    
    def factions_menu(self):
        self.clear_screen()
        print("🎭 ФРАКЦИИ")
        print("="*60)
        print()
        
        for faction, rep in self.player.factions.items():
            rank = self.player.get_faction_rank(faction)
            bar_length = min(50, abs(rep) // 20)
            bar = "█" * bar_length
            
            print(f"{faction.upper()}")
            print(f"  Репутация: {rep:+d}")
            print(f"  Ранг: {rank}")
            print(f"  [{bar}]")
            print()
        
        print("Влияние фракций:")
        print("• HACKERS - дают доступ к эксклюзивным инструментам")
        print("• CORPORATIONS - высокооплачиваемые контракты")
        print("• ANARCHISTS - уникальные миссии саботажа")
        print("• GOVERNMENT - законная защита и поддержка")
        print("• UNDERGROUND - черный рынок и секретная информация")
        print()
        
        if all(rep >= 1000 for rep in self.player.factions.values()):
            print(self.player.add_achievement("🎭 Дипломат фракций"))
        
        input("Нажмите Enter...")
    
    def save_specific_game(self, mode):
        self.clear_screen()
        print(f"💾 СОХРАНЕНИЕ {'СЮЖЕТА' if mode == 'story' else 'СВОБОДНОГО РЕЖИМА'}")
        print("="*30)
        print()
        autosave_file = os.path.join(self.data.save_dir, f"autosave_{mode}.dat")
        if os.path.exists(autosave_file):
            with open(autosave_file, 'rb') as f:
                save_data = pickle.load(f)
            print("0. [АВТОСОХРАНЕНИЕ] - последняя сессия")
        else:
            print("0. [АВТОСОХРАНЕНИЕ] - нет данных")
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
        saves = self.data.get_saves(mode)
        if not saves:
            print(f"❌ Нет сохранений для {'сюжетного режима' if mode == 'story' else 'свободного режима'}!")
            input("Нажмите Enter...")
            return
            
        self.clear_screen()
        print(f"💾 ЗАГРУЗКА {'СЮЖЕТА' if mode == 'story' else 'СВОБОДНОГО РЕЖИМА'}")
        print("="*30)
        print()
        autosave_file = os.path.join(self.data.save_dir, f"autosave_{mode}.dat")
        if os.path.exists(autosave_file):
            with open(autosave_file, 'rb') as f:
                save_data = pickle.load(f)
            print("0. [АВТОСОХРАНЕНИЕ]")
            print(f"   Имя: {save_data['player']['name']} | Ур. {save_data['player']['level']}")
            print(f"   Прогресс: Глава {save_data['player']['story_progress']} | {save_data['timestamp'][:10]}")
            print()
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
        self.clear_screen()
        print("💾 ЗАГРУЗКА ИГРЫ")
        print("="*30)
        print()
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
            
    def check_for_updates(self):
        self.clear_screen()
        print("🔄 ПРОВЕРКА ОБНОВЛЕНИЙ")
        print("="*30)
        print()
        if os.path.exists("updater.py"):
            print("✅ Апдейтер найден")
            print("🚀 Запуск проверки обновлений...")
            time.sleep(2)
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
                    for mode in ["story", "sandbox"]:
                        autosave_file = os.path.join(self.data.save_dir, f"autosave_{mode}.dat")
                        if os.path.exists(autosave_file):
                            os.remove(autosave_file)
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
        print("="*60)
        print()
        print(f"🎮 Всего глав: {len(chapters)}")
        print("🎯 Целей для взлома: 12")
        print("🛒 Товаров в магазине: 12")
        print("⚡ Навыков для прокачки: 5")
        print("🏆 Достижений: 20")
        print("👹 Боссов: 8")
        print("🎲 Случайных событий: 8+")
        print("🔨 Рецептов крафта: 7")
        print("🎭 Фракций: 5")
        print("💾 Режимы: СЮЖЕТНЫЙ и СВОБОДНЫЙ")
        print()
        print("🚀 Особенности версии 4.0 ULTIMATE:")
        print("  • 40 глав эпического сюжета")
        print("  • Новые главы: Параллельные миры, Цифровые боги")
        print("  • Последний хакер, За пределами кода, Эпилог")
        print("  • Множество концовок и путей развития")
        print("  • Свободный режим с бесконечными возможностями")
        print()
        print("🎮 НОВЫЕ МЕХАНИКИ:")
        print("  • 🎲 Случайные события с выборами")
        print("  • 👹 Эпические битвы с боссами")
        print("  • 🔨 Система крафта предметов")
        print("  • 📋 Ежедневные задания")
        print("  • 🎭 Репутация с 5 фракциями")
        print("  • ⚡ Расширенная система навыков")
        print("  • 💎 20 достижений для разблокировки")
        print()
        print("🌟 ЭКСКЛЮЗИВ:")
        print("  • Раздельная система сохранений")
        print("  • Автосохранения после каждой главы")
        print("  • Персональная статистика для каждого игрока")
        print("  • Новые цели для взлома высокого уровня")
        print("  • Улучшенный магазин с божественными предметами")
        print("  • Динамические случайные события")
        print("  • Прокачка до 100 уровня!")
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
        play_time = time.time() - self.start_time
        if self.player:
            self.player.update_play_time(play_time)
            if self.data.config.get("autosave", True) and self.game_mode:
                self.data.save_game(self.player.__dict__, 0, self.game_mode)
        
        self.clear_screen()
        print(Fore.CYAN + Style.BRIGHT + "="*60)
        print(Fore.GREEN + "👋 До новых встреч в цифровом подполье!")
        print(Fore.YELLOW + Style.BRIGHT + "TERMINAL SHADOWS: DIGITAL GHOST v4.0 - ULTIMATE EDITION")
        if self.player:
            total_minutes = int(self.player.personal_stats['play_time'] // 60)
            print(Fore.MAGENTA + f"🕐 Всего сыграно: {total_minutes} минут")
            print(Fore.CYAN + f"🎯 Уровень: {self.player.level}")
            print(Fore.YELLOW + f"💰 BTC: {self.player.bitcoins:,}")
            print(Fore.GREEN + f"🏆 Достижений: {len(self.player.achievements)}/20")
        print(Fore.CYAN + Style.BRIGHT + "="*60)
        print(Fore.WHITE + "\n'В коде мы находим свободу. В тенях мы становимся светом.'")
        print(Style.RESET_ALL)
        time.sleep(3)
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
