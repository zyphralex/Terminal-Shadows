# Terminal Shadows - Copilot Instructions

## Project Overview
**Terminal Shadows** is a cyberpunk text-based RPG game written in Python with 30 chapters of story content and a free-play sandbox mode. The architecture is modular—each chapter is an independent Python module. The game supports separate save slots for story mode and sandbox mode, with autosave functionality.

**Key Tech**: Python 3.8+, colorama, requests, pickle (serialization), JSON (config)

## Architecture & Core Patterns

### 1. Modular Chapter System
- **Location**: `story/chapter1.py` through `story/chapter30.py`
- **Pattern**: Each chapter is a dict named `CHAPTER_N` with this structure:
  ```python
  CHAPTER_X = {
      "title": "Глава X: TITLE",
      "guide_appearance": True/False,  # Controls anonymous guide appearance
      "scenes": {
          "scene_name": {
              "text": "narrative text",
              "choices": [
                  {
                      "text": "choice text with emoji",
                      "next": "next_scene_or_chapter_end",
                      "effect": {"bitcoins": 100, "exp": 50, ...}
                  }
              ]
          }
      }
  }
  ```
- **Loading**: `main.py` lines 22-27 dynamically imports all 30 chapters via `__import__()` and stores in `chapters[]`
- **When Adding**: Create new chapters following the exact structure; the engine will auto-load them if numbered correctly

### 2. Save System (Dual-Mode)
- **Location**: `GameData` class in `main.py` (lines 29-116)
- **Modes**: `"story"` and `"sandbox"` - each has separate autosave and 3 manual slots
- **Save Format**: Pickle + JSON metadata stored in `~/.terminal_shadows_ultimate/saves/`
  - Autosave: `autosave_{game_mode}.dat`
  - Manual slots: `save{1-3}_{game_mode}.dat`
- **Key Methods**:
  - `save_game(player_data, slot=0, game_mode="story")` - slot 0 = autosave
  - `load_game(slot=0, game_mode="story")` - returns None if save doesn't exist
  - `get_saves(game_mode="story")` - returns list of available slot numbers

### 3. Player Data Model
- **Location**: `Player` class in `main.py` (lines 119-192)
- **Core Stats**: `level`, `exp`, `bitcoins`, 5 skill types (hacking, stealth, programming, social, investigation)
- **Story Tracking**: `story_progress` (chapter number), `completed_missions[]`
- **Personal Stats**: Tracks `play_time`, `chapters_completed`, `achievements_unlocked`, `start_date`
- **Item System**: Simple list `inventory[]` - items stored as strings with emoji prefix (e.g., "🔑 Ключ доступа MegaCorp")

### 4. Game Engine Flow
- **Main Classes**:
  - `GameData` - file I/O, config management (JSON format, keys: language, difficulty, autosave, animations, music)
  - `Player` - state container
  - `GameEngine` - presentation logic, scene navigation, animations
- **Game Modes**:
  - `story` mode: Linear progression through chapters 1-30
  - `sandbox` mode: Unlocked after story completion; separate save state
- **Key Methods** (`GameEngine`):
  - `show_main_menu()` - menu system with choices 1-5+
  - `play_chapter(chapter_num)` - processes chapter dict, handles scene navigation
  - `hacking_animation(target)` - progress bar effect (skipped if animations disabled)
  - `type_text(text, delay)` - typewriter effect controlled by config

## Critical Developer Workflows

### Adding a New Chapter
1. Create `story/chapterN.py` with `CHAPTER_N` dict (follow chapter1.py structure)
2. Chapters auto-load in `main.py` lines 22-27 (no manual registration needed)
3. Ensure last scene has `"next": "chapter_end"` to trigger story_progress increment
4. Test by running: `./run_game.sh` and selecting story mode

### Testing Save/Load Cycle
```bash
# Manually invoke save operations in test
python3 -c "
import pickle, json
from main import GameData, Player
gd = GameData()
p = Player('test')
gd.save_game(p, slot=1, game_mode='story')
loaded = gd.load_game(slot=1, game_mode='story')
print('Player data:', loaded['player'].name if loaded else 'Failed')
"
```

### Running the Game
- **Story/Sandbox**: `./run_game.sh` → launches main menu
- **Direct Python**: `python3 main.py`
- **Update Check**: `./update_game.sh` → runs updater.py (git-based)

### Configuration
- Stored in: `~/.terminal_shadows_ultimate/config.json`
- User-configurable: `language` (ru/en planned), `difficulty`, `autosave`, `animations`, `music`
- Defaults loaded if missing/corrupted (graceful fallback in `load_config()`)

## Important Conventions & Patterns

### 1. Emoji Usage
- Every choice text starts with emoji (🚀, 🛠️, 🤝, 🔍, etc.)
- Scene effects in `effect{}`: bitcoins, exp, level, skill (with value), reputation, item
- Items are descriptive strings with emoji prefix (standardized)

### 2. Effect System in Choices
```python
"effect": {
    "bitcoins": 1500,           # Exact integer
    "exp": 750,                 # Exact integer
    "level": 2,                 # Absolute level or increment
    "skill": "stealth",         # One skill type
    "value": 3,                 # Skill points
    "reputation": 75,           # Reputation gain
    "item": "🔑 Key Name"       # Exact item string
}
```
- Multiple effects can coexist
- Applied via `apply_effects()` (called during scene processing in engine)

### 3. Platform Restrictions
- **Linux-only enforcement** in `main.py` lines 8-11
- Checks `platform.system()` and exits if Windows/Darwin detected
- Note: Game works on Termux (Android) as fallback

### 4. Directory Structure
```
~/.terminal_shadows_ultimate/
├── saves/              # autosave_*.dat + save{1-3}_*.dat
├── backups/            # timestamped backups (updater)
├── config.json         # user settings
└── (game data)
```

## External Dependencies & Integration Points

### Dependencies (requirements.txt)
- **colorama** ≥0.4.4 - colored terminal output (used in story scenes)
- **requests** ≥2.25.1 - HTTP calls (used by updater.py for version checks)

### Updater System (updater.py)
- Git-based: clones `github.com/zyphralex/Terminal-Shadows` to temp folder
- Backs up `~/.terminal_shadows_ultimate/saves/` before update
- Versioning: reads from `version.txt` file
- Run via `./update_game.sh` script

### ASCII Art Assets
- Location: `data/ascii_arts/`
- Used by: `print_ascii(art_name)` method in GameEngine
- Files: `main_menu.txt`, `anonymous_guide.txt`, `hacking.txt`, `victory.txt`
- Encoding: UTF-8 (supports Cyrillic)

## Testing & Validation Patterns

### Chapter Validation
- Check that all scenes referenced in `"next"` keys actually exist in scenes dict
- Verify effect fields use only valid keys (no typos)
- Ensure terminal story flows to `"chapter_end"` eventually

### Save/Load Testing
- Test autosave on mode switch (story ↔ sandbox)
- Verify 3 manual slots are independent per mode
- Check backward compatibility when loading old save versions

### Configuration Resilience
- Missing config.json → defaults loaded automatically
- Corrupted JSON → exception caught, defaults applied
- New config keys in updates → merged with existing values

## Common Pitfalls & Gotchas

1. **Chapter Import Failure**: If a chapter has syntax errors, the import silently fails and that chapter is skipped. Check console output for `Error loading chapter X`.
2. **Save Slot Confusion**: Manual slots are 1-3, autosave is slot 0. Using slot 0 with `game_mode` param is required for proper separation.
3. **Effect Application**: Effects are read directly from chapter dicts—no validation. Misspelled effect keys are silently ignored.
4. **Animation Config**: The `type_text()` and `hacking_animation()` methods check `config["animations"]` at runtime; disabling doesn't require restart.
5. **Platform Check**: Runs before colorama import. If porting to Windows, remove lines 8-11 and handle terminal colors differently.

## Key Files Reference

| File | Purpose |
|------|---------|
| `main.py` | Game engine, player state, save/load logic |
| `updater.py` | Git-based version update system |
| `story/chapter*.py` | 30 chapter (or more) narrative dicts |
| `data/ascii_arts/*.txt` | Visual assets |
| `requirements.txt` | pip dependencies |
| `version.txt` | Current game version |
