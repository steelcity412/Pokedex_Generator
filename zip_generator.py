import os
import zipfile

def zip_folder(folder_path, zip_path, logger):
    """
    Zips a single folder into a .zip archive.
    Used at the end of the pipeline to compress output folders.
    """

    if not os.path.exists(folder_path):
        logger.warning(f"Cannot zip missing folder: {folder_path}")
        return

    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, _, files in os.walk(folder_path):
            for f in files:
                full_path = os.path.join(root, f)
                rel_path = os.path.relpath(full_path, folder_path)
                zf.write(full_path, rel_path)

    logger.info(f"Created ZIP: {zip_path}")


def zip_all(base_output: str, folders: dict, logger):
    """
    Zips ALL output folders (sprites, TXT, DOCX).
    Called once at the end of the main script.
    """

    zip_folder(folders["sprites"], os.path.join(base_output, "Pokemon_Sprites.zip"), logger)
    zip_folder(folders["text_en"], os.path.join(base_output, "Pokemon_Text_en.zip"), logger)
    zip_folder(folders["text_ja"], os.path.join(base_output, "Pokemon_Text_ja.zip"), logger)
    zip_folder(folders["text_ja_hrkt"], os.path.join(base_output, "Pokemon_Text_ja-Hrkt.zip"), logger)
    zip_folder(folders["docx_en"], os.path.join(base_output, "Pokemon_Docx_en.zip"), logger)
    zip_folder(folders["docx_ja"], os.path.join(base_output, "Pokemon_Docx_ja.zip"), logger)
    zip_folder(folders["docx_ja_hrkt"], os.path.join(base_output, "Pokemon_Docx_ja-Hrkt.zip"), logger)
