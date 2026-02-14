# X4 ShipMatrix

A comprehensive Python application for parsing and analyzing X4: Foundations ship data with **multi-language support** and **intelligent data extraction**.

##  Key Features

- ** Multi-Language Support**: Automatic detection of 14+ languages (English, German, French, Spanish, Italian, Russian, Polish, Czech, Turkish, Japanese, Korean, Chinese)
- ** Smart Data Extraction**: Direct CAT/DAT file reading with XRCatTool integration
- ** Clean GUI Interface**: Windowed application without console windows
- ** Advanced Ship Analysis**: Calculate travel speeds, compare ships and engines
- **� Visual Comparisons**: Interactive charts showing cargo/speed rankings for top 5 ships
- ** Intelligent Filtering**: Cascading dropdowns that auto-filter engines by ship size
- **� Flexible Updates**: Automatic or manual update options
- ** Intelligent Detection**: Auto-finds X4 installation and language preferences

##  For End Users (Standalone Version)

### Quick Start
1. **Download** from [Releases](https://github.com/jongreg288/X4_Ship_Parse/releases)
2. **Choose your package**:
   - **Full Package** (`X4_Ship_Parser.exe` + `X4_Updater.exe`) - 93 MB total
   - **Standalone Package** (`X4_Ship_Parser.exe` only) - 78.5 MB
3. **Run** `X4_Ship_Parser.exe`
4. **Automatic setup** - detects X4 installation and language preferences

### System Requirements
- **OS**: Windows 10/11 (64-bit)
- **Game**: X4: Foundations installed (Steam, Epic Games, GOG)
- **Space**: ~2 GB free space for extracted data
- **Network**: Optional (only for automatic updates)

## For Developers (Source Code)

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Game Data Setup

The application **automatically extracts** game data using integrated XRCatTool:

**Automatic Setup:**
- Detects X4 installation from Steam, Epic Games, or GOG
- Extracts only required files from CAT/DAT archives
- Sets up language-specific text files
- Creates optimized data structure

**Manual Setup (if needed):**
```
data/
├── assets/
│   ├── props/
│   │   ├── Engines/macros/ → *.xml (engine definitions)
│   │   └── StorageModules/ → *.xml (cargo modules)
│   └── units/
│       ├── size_l/macros/ → ship_*.xml (large ships)
│       ├── size_m/macros/ → ship_*.xml (medium ships)
│       └── size_s/macros/ → ship_*.xml (small ships)
└── t/ → 0001-l{language_id}.xml (localization)
```

### 3. Run the Application

```bash
# Development mode
python main.py

# Or use launcher (includes setup wizard)
python launcher.py
```

##  Usage

### Main Interface
1. **Launch**: Run `python main.py` or `X4_Ship_Parser.exe`
2. **Language**: Automatically detects your language or use Settings → Language
3. **Ship Selection**: Choose from 4 categories (Fighters, Container, Solid, Liquid)
4. **Engine Selection**: Smart filtering shows only compatible engines for your ship's size class
5. **Analysis**: View detailed travel speeds and cargo/speed ratios
6. **Visual Comparison**: Interactive bar chart displays top 5 ships of same size with selected engine

### New Features (v0.1.3)
- **Smart Engine Filtering**: Engine dropdown automatically filters by ship size (S/M/L/XL)
- **Visual Rankings**: Bar chart shows how your ship compares to top 5 similar ships
- **Improved Engine Names**: Cleaner format showing faction, size, type, and variant
- **Enhanced Tooltips**: More detailed information on hover

### Language Support
- **Automatic Detection**: Reads X4 config, Steam settings, or system locale
- **Manual Override**: Settings → Language → Choose from 14+ languages
- **Real-time Switching**: Change languages without restart

### Travel Speed Formula
```
travel_speed = (forward_thrust × travel_thrust × engine_connections) / drag_forward
```

**Variables:**
- `forward_thrust`: Engine's main thrust output
- `travel_thrust`: Engine's travel drive efficiency  
- `engine_connections`: Ship's engine mount points
- `drag_forward`: Ship's aerodynamic resistance

##  Project Structure

```
X4_Ship_Parse/
├──  Distribution
│   ├── dist/                     # Built executables & user files
│   │   ├── X4_Ship_Parser.exe   # Main application (64.6 MB)
│   │   ├── X4_Updater.exe       # Update checker (14.4 MB)
│   │   ├── XRCatTool.exe        # Data extraction tool
│   │   └── README_USERS.txt     # User instructions
│   └── releases/                # Release management
│
├──  Source Code  
│   ├── main.py                  # Application entry point
│   ├── standalone_updater.py    # Update checker source
│   └── src/                     # Core modules
│       ├── gui.py              # PyQt6 interface + language selection
│       ├── data_parser.py      # XML parsing + text resolution
│       ├── language_detector.py # Multi-language support
│       ├── x4_data_extractor.py # CAT/DAT extraction
│       ├── logic.py            # Physics calculations
│       └── ...                 # Other source files
│
├──  Build System
│   └── build_scripts/          # Build configuration
│       ├── build_both.py       # Build both executables  
│       ├── build_exe.py        # Build main executable
│       ├── X4_Ship_Parser.spec # Main app build config
│       ├── X4_Updater.spec     # Updater build config
│       └── version_info.txt    # Windows version metadata
│
├──  Documentation
│   └── docs/                   # All documentation
│       ├── LANGUAGE_SUPPORT.md # Multi-language guide
│       ├── UPDATE_MANAGEMENT.md # Update system guide
│       ├── UPDATE_SUMMARY.md   # Development summary
│       └── RELEASE_SETUP.md    # GitHub release guide
│
├──  Testing
│   └── tests/                  # Test files
│       ├── test_final_filtering.py
│       └── test_language_detection.py
│
├──  Game Data (Auto-generated)
│   └── data/                   # X4 extracted data
│
└──  Configuration
    ├── README.md               # This file
    ├── requirements.txt        # Python dependencies
    └── .gitignore             # Git ignore rules
```

##  Building Executables

### Recommended (single command)
```bash
python build_scripts/release_prerelease.py
```

This is the canonical workflow for 0.x releases. See `docs/BUILD_RELEASE_WORKFLOW.md`.

### Single Executable (Main App Only)
```bash
cd build_scripts
python build_exe.py
# Creates: dist/X4_Ship_Parser.exe (64.6 MB)
```

### Dual Executables (Full Package)
```bash
cd build_scripts
python build_both.py  
# Creates: dist/X4_Ship_Parser.exe + X4_Updater.exe (79 MB total)
```

### Build Features
- **Windowed Mode**: No console windows (uses `runw.exe` bootloader)
- **Language Detection**: Bundles language detector and text mappings
- **XRCatTool Integration**: Includes data extraction tools
- **Optimized Size**: Removes unnecessary network dependencies from main app

##  Development

### Testing & Debugging
```bash
# Development mode with full output
python main.py

# Setup wizard testing
python launcher.py

# Language detection testing  
python test_language_detection.py

# Parser debugging
python debug_parser.py
```

### Adding Features
1. **Language Support**: Edit `app/language_detector.py` mappings
2. **Ship Analysis**: Modify `app/logic.py` calculations  
3. **Data Parsing**: Update `app/data_parser.py` extraction
4. **GUI Features**: Enhance `app/gui.py` interface

## License

This project is for educational/modding purposes. X4: Foundations and its data files are property of Egosoft.
