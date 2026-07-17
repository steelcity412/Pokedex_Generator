import os
import shutil

# -----------------------------
# Utility helpers
# -----------------------------

def normalize_text(text: str) -> str:
    """
    Normalizes whitespace and line endings so comparisons are stable.
    Prevents false positives when checking for changes.
    """
    lines = text.replace('\r\n', '\n').replace('\r', '\n').split('\n')
    normalized_lines = [' '.join(line.split()) for line in lines]
    return '\n'.join(normalized_lines).strip()


def backup_file_if_exists(src_path, backup_dir, logger):
    """
    Moves old TXT files into backup folder before overwriting.
    Preserves history of changes.
    """
    if os.path.exists(src_path):
        os.makedirs(backup_dir, exist_ok=True)
        base_name = os.path.basename(src_path)
        backup_path = os.path.join(backup_dir, base_name)
        shutil.move(src_path, backup_path)
        logger.info(f"Backed up old TXT to: {backup_path}")


# -----------------------------
# Data extraction helpers
# -----------------------------

def dm_to_height(dm):
    """Convert decimeters → feet/inches + meters."""
    meters = dm / 10
    total_inches = meters * 39.3701
    feet = int(total_inches // 12)
    inches = int(round(total_inches % 12))
    return f"{feet}'{inches:02}\" ({meters:.1f} m)"


def hg_to_weight(hg):
    """Convert hectograms → lbs + kg."""
    kg = hg / 10
    lbs = kg * 2.20462
    return f"{lbs:.1f} lbs ({kg:.1f} kg)"


def extract_flavor_texts(species_json, lang_code):
    """Extract and dedupe flavor text for a given language."""
    entries = species_json.get("flavor_text_entries", [])
    raw_entries = [
        e["flavor_text"].replace("\n", " ").replace("\f", " ")
        for e in entries
        if e["language"]["name"] == lang_code
    ]
    seen = set()
    unique = []
    for ft in raw_entries:
        if ft not in seen:
            seen.add(ft)
            unique.append(ft)
    return unique


def extract_evolution_chain(evo_json):
    """Extract evolution chain in order."""
    chain = []
    current = evo_json.get("chain")
    while current:
        chain.append(current["species"]["name"])
        current = current["evolves_to"][0] if current.get("evolves_to") else None
    return chain


def get_localized_name(species_json, lang_code):
    """Get localized Pokémon name for ja or ja-Hrkt."""
    for entry in species_json.get("names", []):
        if entry["language"]["name"] == lang_code:
            return entry["name"]
    return None


# -----------------------------
# Summary builders
# -----------------------------

def build_summary_en(p, species, evo_chain, flavor_en):
    """
    Build English TXT summary for a Pokémon.
    """
    pokemon_id = p["id"]
    name = p["name"].capitalize()
    abilities = [a["ability"]["name"] for a in p["abilities"]]
    types = [t["type"]["name"] for t in p["types"]]
    stats = {s["stat"]["name"]: s["base_stat"] for s in p["stats"]}
    moves = [m["move"]["name"] for m in p["moves"]]
    color = species["color"]["name"]
    egg_groups = [g["name"] for g in species["egg_groups"]]
    height_str = dm_to_height(p["height"])
    weight_str = hg_to_weight(p["weight"])

    lines = [
        f"ID: {pokemon_id}",
        f"Name: {name}",
        f"Base Experience Yield: {p['base_experience']}",
        f"Height: {height_str}",
        f"Weight: {weight_str}",
        f"Color: {color}",
        "",
        "Abilities:",
        *[f" - {a}" for a in abilities],
        "",
        "Types:",
        *[f" - {t}" for t in types],
        "",
        "Stats:",
        *[f" - {k}: {v}" for k, v in stats.items()],
        "",
        "Species Information:",
        f" - Egg Groups: {', '.join(egg_groups)}",
        f" - Is Baby: {species['is_baby']}",
        f" - Is Legendary: {species['is_legendary']}",
        f" - Is Mythical: {species['is_mythical']}",
        f" - Evolution Chain: {' → '.join([e.capitalize() for e in evo_chain])}",
        "",
        "Flavor Text (English):",
        *[f" - {ft}" for ft in flavor_en],
        "",
        "Moves:",
        *[f" - {m}" for m in moves],
    ]
    return "\n".join(lines)


def build_summary_ja(p, species, evo_chain, flavor, lang_label, lang_code):
    """
    Build Japanese TXT summary (ja or ja-Hrkt).
    Includes English fallback where Japanese data is missing.
    """
    pokemon_id = p["id"]
    name_en = p["name"].capitalize()
    name_local = get_localized_name(species, lang_code) or name_en
    abilities = [a["ability"]["name"] for a in p["abilities"]]
    types = [t["type"]["name"] for t in p["types"]]
    stats = {s["stat"]["name"]: s["base_stat"] for s in p["stats"]}
    moves = [m["move"]["name"] for m in p["moves"]]
    color = species["color"]["name"]
    egg_groups = [g["name"] for g in species["egg_groups"]]
    height_str = dm_to_height(p["height"])
    weight_str = hg_to_weight(p["weight"])

    lines = [
        f"ID: {pokemon_id}",
        f"Name (English): {name_en}",
        f"Name ({lang_label}): {name_local}",
        f"Base Experience Yield: {p['base_experience']}",
        f"Height: {height_str}",
        f"Weight: {weight_str}",
        f"Color: {color}",
        "",
        "Abilities (English):",
        *[f" - {a}" for a in abilities],
        "",
        "Types (English):",
        *[f" - {t}" for t in types],
        "",
        "Stats:",
        *[f" - {k}: {v}" for k, v in stats.items()],
        "",
        "Species Information (English):",
        f" - Egg Groups: {', '.join(egg_groups)}",
        f" - Is Baby: {species['is_baby']}",
        f" - Is Legendary: {species['is_legendary']}",
        f" - Is Mythical: {species['is_mythical']}",
        f" - Evolution Chain: {' → '.join([e.capitalize() for e in evo_chain])}",
        "",
        f"Flavor Text ({lang_label}):",
    ]

    if flavor:
        lines.extend([f" - {ft}" for ft in flavor])
    else:
        lines.append(" - (No localized flavor text available; English fallback used)")

    lines.extend([
        "",
        "Moves (English):",
        *[f" - {m}" for m in moves],
    ])

    return "\n".join(lines)


# -----------------------------
# Main TXT generator
# -----------------------------

def generate_txt_for_lang(pokemon_list, species_map, evo_map, lang, folders, logger):
    """
    Generates TXT files for a specific language.
    Handles validation, backup, and writing.
    """

    # Determine output + backup folders based on language
    if lang == "en":
        out_dir = folders["text_en"]
        backup_dir = folders["backups_text_en"]
    elif lang == "ja":
        out_dir = folders["text_ja"]
        backup_dir = folders["backups_text_ja"]
    elif lang == "ja-Hrkt":
        out_dir = folders["text_ja_hrkt"]
        backup_dir = folders["backups_text_ja_hrkt"]
    else:
        logger.error(f"Unsupported language: {lang}")
        return

    # Process each Pokémon
    for p in pokemon_list:
        pid = p["id"]
        name = p["name"].capitalize()
        id_str = f"{pid:04d}"

        species = species_map[pid]
        evo_json = evo_map[pid]
        evo_chain = extract_evolution_chain(evo_json)

        # Extract flavor text for each language
        flavor_en = extract_flavor_texts(species, "en")
        flavor_ja = extract_flavor_texts(species, "ja")
        flavor_ja_hrkt = extract_flavor_texts(species, "ja-Hrkt")

        # Build summary based on language
        if lang == "en":
            summary = build_summary_en(p, species, evo_chain, flavor_en)
            filename = f"{id_str}_{name}_en.txt"
        elif lang == "ja":
            summary = build_summary_ja(p, species, evo_chain, flavor_ja, "Japanese (ja)", "ja")
            filename = f"{id_str}_{name}_ja.txt"
        else:
            summary = build_summary_ja(p, species, evo_chain, flavor_ja_hrkt, "Japanese (ja-Hrkt)", "ja-Hrkt")
            filename = f"{id_str}_{name}_ja-Hrkt.txt"

        path = os.path.join(out_dir, filename)
        new_norm = normalize_text(summary)

        # Validation: compare old vs new
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                old = f.read()
            old_norm = normalize_text(old)

            if old_norm != new_norm:
                backup_file_if_exists(path, backup_dir, logger)
                with open(path, "w", encoding="utf-8") as f:
                    f.write(summary)
                logger.info(f"Updated TXT ({lang}): {path}")
            else:
                logger.info(f"No changes in TXT ({lang}): {path}")

        else:
            # First-time creation
            with open(path, "w", encoding="utf-8") as f:
                f.write(summary)
            logger.info(f"Created TXT ({lang}): {path}")
