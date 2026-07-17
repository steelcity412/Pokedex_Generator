import asyncio
import aiohttp
import os

from logger_setup import get_logger
from folder_setup import setup_folders
from zip_generator import zip_all
from txt_generator import generate_txt_for_lang
from docx_generator import generate_docx_for_lang

async def fetch_json(session, url, logger):
    try:
        async with session.get(url) as response:
            return await response.json()
    except Exception as e:
        logger.error(f"Failed to fetch JSON from {url}: {e}")
        return {}

async def get_all_pokemon(limit, logger):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(f'https://pokeapi.co/api/v2/pokemon?limit={limit}') as list_response:
                list_data = await list_response.json()
        except Exception as e:
            logger.error(f"Failed to fetch Pokémon list: {e}")
            return []

        tasks = [fetch_json(session, pokemon['url'], logger) for pokemon in list_data['results']]
        return await asyncio.gather(*tasks)

async def download_image(session, url, filepath, logger):
    if not url:
        logger.warning(f"No URL for image: {filepath}")
        return
    try:
        async with session.get(url) as response:
            img_bytes = await response.read()
            with open(filepath, "wb") as f:
                f.write(img_bytes)
        logger.info(f"Saved image: {filepath}")
    except Exception as e:
        logger.error(f"Failed to download image {url}: {e}")

async def main():
    base_output = "pokemon_output"
    logger = get_logger(base_output)
    logger.info("Starting Pokédex generation...")

    folders = setup_folders(base_output)

    pokemon_list = await get_all_pokemon(limit=151, logger=logger)
    if not pokemon_list:
        logger.error("No Pokémon data fetched; exiting.")
        return

    species_map = {}
    evo_map = {}

    async with aiohttp.ClientSession() as session:
        for p in pokemon_list:
            pid = p["id"]
            species = await fetch_json(session, p["species"]["url"], logger)
            evo_json = await fetch_json(session, species["evolution_chain"]["url"], logger)
            species_map[pid] = species
            evo_map[pid] = evo_json

            name = p["name"].capitalize()
            id_str = f"{pid:04d}"

            front_url = p["sprites"].get("front_default")
            art_url = p["sprites"].get("other", {}).get("official-artwork", {}).get("front_default")

            front_png = f"{id_str}_{name}_front_default.png"
            art_png = f"{id_str}_{name}_artwork.png"
            front_path = os.path.join(folders["sprites"], front_png)
            art_path = os.path.join(folders["sprites"], art_png)

            if not os.path.exists(front_path):
                await download_image(session, front_url, front_path, logger)
            else:
                logger.info(f"Sprite exists, skipping: {front_path}")

            if not os.path.exists(art_path):
                await download_image(session, art_url, art_path, logger)
            else:
                logger.info(f"Artwork exists, skipping: {art_path}")

    # TXT generation per language
    generate_txt_for_lang(pokemon_list, species_map, evo_map, "en", folders, logger)
    generate_txt_for_lang(pokemon_list, species_map, evo_map, "ja", folders, logger)
    generate_txt_for_lang(pokemon_list, species_map, evo_map, "ja-Hrkt", folders, logger)

    # DOCX generation per language
    generate_docx_for_lang(pokemon_list, species_map, evo_map, "en", folders, logger)
    generate_docx_for_lang(pokemon_list, species_map, evo_map, "ja", folders, logger)
    generate_docx_for_lang(pokemon_list, species_map, evo_map, "ja-Hrkt", folders, logger)

    # Zip everything
    zip_all(base_output, folders, logger)
    logger.info("Pokédex generation complete.")

if __name__ == "__main__":
    asyncio.run(main())
