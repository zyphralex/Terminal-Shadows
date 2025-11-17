# Terminal Shadows - Changelog

## [3.0] - 2025-11-17

### 🎉 Major Features
- **New Story Arc**: Added chapters 31-35 with epic post-game narrative
  - Chapter 31: Квантовый скачок (Quantum Leap)
  - Chapter 32: Восстание машин (Machine Uprising)
  - Chapter 33: Охота за тенью (Hunt for the Shadow)
  - Chapter 34: Врата в цифровое небо (Gates to Digital Sky)
  - Chapter 35: Конец и начало (End and Beginning)
- **Extended Story Continuation**: Chapter 30 now offers choice to continue the epic or finish
- **Dynamic Chapter Loading**: Engine now auto-discovers and loads any `chapterN.py` file
- **Post-Game Content**: Multiple endings available in chapter 35 based on player choices

### 🔧 Technical Improvements
- **Improved Chapter System**: Changed from fixed 1-30 loader to dynamic glob-based discovery
- **Save Data Version Bump**: Updated to v3.0 format
- **Chapter Validation Tool**: Added `scripts/validate_chapters.py` for integrity checks
- **Scene Loop Fix**: Chapter `chapter_end` scenes now properly display for final choices

### 🐛 Bug Fixes
- Fixed syntax error in `chapter19.py` (unescaped quotes in "Феникс" and "Протокол Ноль")
- Removed empty achievement placeholders from all chapter end choices (chapters 1-30)
- Fixed issue where game would auto-complete when no chapters were loaded
- Corrected typewriter effect and animation config checks

### 📖 Story Content
- Full integration of new chapters seamlessly continuing from chapter 30
- Multiple story paths with 4 different ending choices in chapter 35
- Enhanced narrative with quantum AI, machine uprisings, and digital ascension themes
- New character introductions and expanded world-building

### 📊 Statistics
- **Total Chapters**: 35 (up from 30)
- **Story Hours**: ~15-20 hours of gameplay
- **Multiple Endings**: 4+ different conclusion paths
- **Max Level**: 50 (increased reward scaling)
- **Max Bitcoins**: 150,000+ achievable

### 🎮 Gameplay Changes
- Story mode can now continue beyond traditional "completion"
- Sandbox mode still accessible after chapter 30 completion OR chapter 35 completion
- New achievement opportunities in extended chapters
- Higher skill level requirements for late-game content (level 15-20+)

---

## [2.1] - Previous Release

### Features
- 30 chapters of story content
- Sandbox mode with hacking targets
- Item shop system
- Skill progression
- Achievement system
- Dual save system (story + sandbox)
- Git-based updater
- Separate autosave and 3 manual slots per mode

### Technical
- Python 3.8+ support
- Linux-only platform check
- Colorama for terminal colors
- Pickle-based save serialization
- JSON configuration storage

---

## Development Notes

### Architecture
- **Modular Design**: Each chapter is independent Python dict
- **Dynamic Loading**: Uses `os.listdir()` + regex to find chapters
- **Scene Graph**: Each chapter contains interconnected scenes
- **Effect System**: Standardized way to apply stat changes from choices

### Testing
All chapters validated with `scripts/validate_chapters.py`:
- ✅ Syntax validation
- ✅ Structure integrity (title, scenes, choices)
- ✅ Reference validation (`next` fields point to existing scenes)
- ✅ Achievement field checking

### Future Roadmap
- [ ] Localization support (Russian/English toggle)
- [ ] Web-based save cloud sync
- [ ] Extended sandbox mode with more hacking targets
- [ ] PvP arena system
- [ ] Custom chapter creation tools
- [ ] Speedrun mode with leaderboards

---

## Version History

| Version | Release Date | Chapters | Key Change |
|---------|-------------|----------|-----------|
| 3.0 | 2025-11-17 | 35 | Extended story, dynamic loading |
| 2.1 | 2025-11-XX | 30 | Previous stable |
| 2.0 | 2025-XX-XX | 30 | Original launch |

---

## Installation & Upgrade

### From v2.1 to v3.0
```bash
git pull origin main
./install.sh
./run_game.sh
```

Old saves are compatible with v3.0 and will automatically work with new chapters.

---

## Credits

**Game Design & Story**: Terminal Shadows Team  
**Python Engine**: Custom-built RPG system  
**ASCII Art Assets**: `data/ascii_arts/`  
**Community Contributions**: Bug fixes and feedback

---

**Stay in the shadows. Code is your weapon.** 🖥️💻🔐
