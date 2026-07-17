# 📘 Pokémon Data Extraction & Pokédex Generator

## ❗ Disclaimer

_This project is not affiliated with, endorsed by, or associated with Nintendo, Game Freak, or The Pokémon Company. All Pokémon names and related references are trademarks of their respective owners. This project uses publicly available data from PokéAPI for educational and non‑commercial purposes._

## 🧩 Overview

This project is a modular Pokédex data extraction and document generation system written in Python. It fetches Pokémon data from the **[PokéAPI](https://pokeapi.co/)**, processes it, downloads sprite images, and generates:

- **TXT summaries (English, Japanese, Kana-only Japanese)**

- **DOCX Pokédex entries (with embedded sprites)**

- **PNG sprite images**

- **ZIP archives of each output category**

The system is fully modular, allowing each output type (TXT, DOCX, ZIP) to be generated independently while sharing a single API data fetch.

## ✨ Features

| Feature                       | Description                                                                            |
| :---------------------------- | :------------------------------------------------------------------------------------- |
| **Modular Architecture**      | Separate Python modules for TXT, DOCX, logging, folder setup, and zipping.             |
| **Single API Fetch**          | All Pokémon data is fetched once and passed to generators — no redundant API calls.    |
| **Multi‑Language Output**     | Generates English (en), Japanese (ja), and Kana-only Japanese (ja-Hrkt) files.         |
| **Backup System**             | Old TXT/DOCX files are moved to a backup folder before updates.                        |
| **Validation Logic**          | TXT files are only updated if content changes; DOCX regenerates only when TXT changes. |
| **Async API Fetching**        | Fast parallel downloads using aiohttp + asyncio.                                       |
| **Height/Weight Conversion**  | Converts PokéAPI units (dm/hg) into ft/in, meters, lbs, and kg.                        |
| **Flavor Text Deduplication** | Removes duplicate entries while preserving order.                                      |
| **Sprite Downloading**        | Downloads both front_default and official_artwork images.                              |
| **Logging (Console + File)**  | Full logging stored in pokemon_output/logs/pokedex.log.                                |
| **ZIP Generation**            | Each output folder is zipped automatically at the end.                                 |

## 📁 Modular File Structure

project-root/
│
├── pokedex_generator.py # Main orchestrator
├── logger_setup.py # Logging module
├── folder_setup.py # Folder + backup creation
├── txt_generator.py # TXT generation (multi-language)
├── docx_generator.py # DOCX generation (multi-language)
├── zip_generator.py # ZIP creation
│
└── pokemon_output/
├── logs/
├── backups/
│ ├── Text_en/
│ ├── Text_ja/
│ ├── Text_ja-Hrkt/
│ ├── Docx_en/
│ ├── Docx_ja/
│ └── Docx_ja-Hrkt/
│
├── Pokemon_Sprites/
├── Pokemon_Text_en/
├── Pokemon_Text_ja/
├── Pokemon_Text_ja-Hrkt/
├── Pokemon_Docx_en/
├── Pokemon_Docx_ja/
└── Pokemon_Docx_ja-Hrkt/

## 🚀 Installation Instructions

### **Prerequisites**

- Python **3.10+**

- Internet connection (PokéAPI is online-only)

### Install Dependencies

```
pip install aiohttp python-docx
```

## ▶️ How to Run

1. Run the main orchestrator:

```
python pokedex_generator.py
```

2. After completion, check:

```
pokemon_output/
```

You will find:

- `TXT files (en, ja, ja-Hrkt)`
- `DOCX files (en, ja, ja-Hrkt)`
- `PNG sprites`
- `ZIP archives`
- `Backup history`
- `Logs`

## 📄 Example Output (TXT)

ID: 0001
Name (English): Bulbasaur
Name (Japanese): フシギダネ
Base Experience Yield: 64
Height: 2'04" (0.7 m)
Weight: 15.2 lbs (6.9 kg)
Color: green

Abilities (English):

- overgrow
- chlorophyll

Types (English):

- grass
- poison

Stats:

- hp: 45
- attack: 49
- defense: 49
- special-attack: 65
- special-defense: 65
- speed: 45

Species Information (English):

- Egg Groups: monster, plant
- Is Baby: False
- Is Legendary: False
- Is Mythical: False
- Evolution Chain: Bulbasaur → Ivysaur → Venusaur

Flavor Text (Japanese):

- うまれたときから　せなかに　しょくぶつの　タネが　うえてあって　すこしずつ　そだつ。
- ひなたで　ひるねをする　すがたを　みかける。せなかの　タネが　たいようの　ひかりで　そだつのだ。

Moves (English):

- tackle
- vine-whip
- razor-leaf
- solar-beam

## 🛠️ Technologies Used

| Technology                    | Purpose                             |
| ----------------------------- | ----------------------------------- |
| **Python 3.10+**              | Core language                       |
| **aiohttp**                   | Asynchronous HTTP requests          |
| **asyncio**                   | Parallel execution                  |
| **python-docx**               | DOCX generation                     |
| **PokéAPI**                   | Pokémon data source                 |
| **Unicode-safe file writing** | Prevents encoding errors on Windows |
| **logging**                   | Logs operations                     |

## 🤝 Contributing

Contributions are welcome!

### **Ways to contribute**

- Improve formatting
- Add new output formats (PDF, HTML, JSON)
- Add type icons
- Add game‑specific flavor text annotations
- Add CLI arguments
- Add unit tests
- Refactor into modules

### **Pull Request Guidelines**

- Keep functions small and focused
- Follow PEP8
- Include docstrings
- Test your changes
- Explain your reasoning clearly

## 🔮 Future Improvements

- Add CLI flags (--limit, --lang, --no-docx)
- Add PDF/HTML/JSON output
- Add type icons in DOCX
- Add game-specific flavor text annotations
- Combine all DOCX files into a single Pokédex book
- Add retry logic for API downtime
- Add unit tests

## 📝 CHANGELOG — v2.0 Modular Architecture Upgrade

Added

- Full modularization into separate Python files.
- Multi-language TXT generation (en, ja, ja-Hrkt).
- Multi-language DOCX generation with embedded sprites.
- Backup-before-overwrite system for TXT and DOCX.
- TXT validation and DOCX regeneration logic.
- Unified folder structure under pokemon_output/.
- Logging system (console + rotating file).
- ZIP generation for all output folders.

Changed

- API is now fetched once and shared across modules.

- TXT and DOCX generation moved out of the main script.

- Folder creation moved to its own module.

Removed

- Monolithic single-file architecture.

- Redundant API calls.
