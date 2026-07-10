# 📘 Pokémon Data Extraction & Pokédex Document Generator

## ❗ Disclaimer 

*This project is not affiliated with, endorsed by, or associated with Nintendo,
Game Freak, or The Pokémon Company. All Pokémon names and related references
are trademarks of their respective owners. This project uses publicly available
data from PokéAPI for educational and non-commercial purposes.*


## 🧩 Overview

This project is a **Pokédex data extraction and document generation tool** written in Python. It fetches detailed Pokémon data from the **[PokéAPI](https://pokeapi.co/)**, processes and formats that data, downloads sprite images, and generates:

- **TXT summaries**
- **DOCX Pokédex entries**
- **PNG sprite images**

for the **original 151 Pokémon**.

The output is clean, human‑readable, and structured like a modern Pokédex entry.

## ✨ Features

|Feature|Description|
|---|---|
|**Async API Fetching**|Fast parallel downloads using `aiohttp` + `asyncio`.|
|**Height/Weight Conversion**|Converts PokéAPI units (dm/hg) into ft/in, meters, lbs, and kg.|
|**Flavor Text Deduplication**|Removes duplicate English entries while preserving order.|
|**Sprite Downloading**|Downloads both `front_default` and `official_artwork` images.|
|**TXT + DOCX Generation**|Creates clean, readable Pokédex entries with embedded images.|
|**File Guards**|Prevents overwriting existing TXT, DOCX, or PNG files.|
|**Unified Species Section**|Egg groups, legendary status, baby status, mythical status, evolution chain.|

## 🚀 Installation Instructions

### **Prerequisites**

- Python **3.10+**    
- Internet connection (PokéAPI is online-only)

### **Install Dependencies**

```
pip install aiohttp python-docx
pip install python-docx
```

## ▶️ How to Run

1. Save the script as:

```
pokedex_generator.py
```

2. Run it:

```
python pokedex_generator.py
```

3. After completion, check the folder:

```
pokemon_output/
```

You will find:

- `001_Bulbasaur.txt`
- `001_Bulbasaur.docx`
- `001_Bulbasaur_front_default.png`
- `001_Bulbasaur_artwork.png`
- …and so on up to **151 Pokémon**.

## 📁 Folder Structure

```
project-root/
│
├── pokedex_generator.py
├── README.md
│
└── pokemon_output/
    ├── 001_Bulbasaur.txt
    ├── 001_Bulbasaur.docx
    ├── 001_Bulbasaur_front_default.png
    ├── 001_Bulbasaur_artwork.png
    ├── ...
    └── 151_Mew.docx
```

## 🛠️ Technologies Used

|Technology|Purpose|
|---|---|
|**Python 3.10+**|Core language|
|**aiohttp**|Asynchronous HTTP requests|
|**asyncio**|Parallel execution|
|**python-docx**|DOCX generation|
|**PokéAPI**|Pokémon data source|
|**Unicode-safe file writing**|Prevents encoding errors on Windows|

## 🔍 Deep Dive — How the Script Works

### **1. Fetch Pokémon list**

The script requests:

```
https://pokeapi.co/api/v2/pokemon?limit=151
```

This returns URLs for each Pokémon’s detailed data.

### **2. Fetch detailed Pokémon data (async)**

Using `aiohttp` + `asyncio`, the script downloads:

- Pokémon core data
- Species data
- Evolution chain data

Async fetching makes the script **fast**, even with 151 Pokémon.

### **3. Extract and dedupe flavor text**

The script:

- Filters for English entries
- Removes duplicates flavor text entries
- Preserves order
- Cleans whitespace

This produces a clean lore section.

### **4. Convert height and weight**

PokéAPI returns:

- Height in **decimeters (dm)**
- Weight in **hectograms (hg)**

The script converts them into:

- ft/in
- meters
- lbs
- kg

### **5. Build unified Species Information section**

Includes:

- Egg groups
- Is Baby
- Is Legendary
- Is Mythical
- Evolution chain

### **6. Download sprite images**

Two images are downloaded:

- `front_default` (sprite image)
- `official_artwork`

Saved as PNG files.

### **7. Generate TXT files**

TXT files contain:

- Core info
- Abilities
- Types
- Stats
- Species Information
- Flavor text
- Moves

### **8. Generate DOCX files**

DOCX files contain:

- Left‑aligned images
- Full summary text

### **9. File guards**

Prevents overwriting existing files.

## 📄 Example Output (TXT)

```
ID: 1
Name: Bulbasaur
Base Experience Yield: 64
Height: 2'04" (0.7 m)
Weight: 15.2 lbs (6.9 kg)
Color: green

Abilities:
 - overgrow
 - chlorophyll

Types:
 - grass
 - poison

Stats:
 - hp: 45
 - attack: 49
 - defense: 49
 - special-attack: 65
 - special-defense: 65
 - speed: 45

Species Information:
 - Egg Groups: monster, plant
 - Is Baby: False
 - Is Legendary: False
 - Is Mythical: False
 - Evolution Chain: Bulbasaur → Ivysaur → Venusaur

Flavor Text in the games (English):
 - A strange seed was planted on its back at birth. The plant sprouts and grows with this POKéMON.
 - It can go for days without eating a single morsel. In the bulb on its back, it stores energy.
 - The seed on its back is filled with nutrients. The seed grows steadily larger as its body grows.
 - It carries a seed on its back right from birth. As it grows older, the seed also grows larger.
 - While it is young, it uses the nutrients that are stored in the seeds on its back in order to grow.
 - BULBASAUR can be seen napping in bright sunlight. There is a seed on its back. By soaking up the sun’s rays, the seed grows progressively larger.
 - There is a plant seed on its back right from the day this POKéMON is born. The seed slowly grows larger.
 - For some time after its birth, it grows by gaining nourishment from the seed on its back.
 - A strange seed was planted on its back at birth. The plant sprouts and grows with this Pokémon.
 - Bulbasaur can be seen napping in bright sunlight. There is a seed on its back. By soaking up the sun’s rays, the seed grows progressively larger.
 - There is a plant seed on its back right from the day this Pokémon is born. The seed slowly grows larger.
 - While it is young, it uses the nutrients that are stored in the seed on its back in order to grow.

Moves (full list):
 - tackle
 - vine-whip
 - razor-leaf
 - solar-beam
 ...
```

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

### **Recommended enhancements**

- Alphabetize moves
- Add type icons in DOCX
- Add bold section headers in DOCX
- Add game names to flavor text
- Combine all DOCX files into a single Pokédex book
- Add retry logic for API downtime
- Add CLI flags (e.g., `--limit 151`, `--no-docx`)

## 🔧 Refactoring Recommendations

Your script is already clean, but here are improvements that would make it even more maintainable:

### ✔ Break into modules

Suggested structure:

```
src/
  fetch.py
  parse.py
  convert.py
  write_txt.py
  write_docx.py
  main.py
```

### ✔ Use dataclasses

Represent Pokémon as structured objects.

### ✔ Add logging

Replace `print()` with `logging`.

### ✔ Add configuration file

Let users choose:

- number of Pokémon
- output formats
- whether to download images
- whether to dedupe flavor text

### ✔ Add unit tests

Especially for:

- height conversion
- weight conversion
- dedupe logic
