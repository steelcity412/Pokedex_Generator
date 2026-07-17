import os

def setup_folders(base_output: str):
    """
    Creates all required output folders and backup folders.
    Returns a dictionary containing paths for easy access.
    """

    # Main output folders
    sprites_dir = os.path.join(base_output, "Pokemon_Sprites")
    text_en_dir = os.path.join(base_output, "Pokemon_Text_en")
    text_ja_dir = os.path.join(base_output, "Pokemon_Text_ja")
    text_ja_hrkt_dir = os.path.join(base_output, "Pokemon_Text_ja-Hrkt")
    docx_en_dir = os.path.join(base_output, "Pokemon_Docx_en")
    docx_ja_dir = os.path.join(base_output, "Pokemon_Docx_ja")
    docx_ja_hrkt_dir = os.path.join(base_output, "Pokemon_Docx_ja-Hrkt")

    # Backup folders
    backups_base = os.path.join(base_output, "backups")
    backups_text_en = os.path.join(backups_base, "Text_en")
    backups_text_ja = os.path.join(backups_base, "Text_ja")
    backups_text_ja_hrkt = os.path.join(backups_base, "Text_ja-Hrkt")
    backups_docx_en = os.path.join(backups_base, "Docx_en")
    backups_docx_ja = os.path.join(backups_base, "Docx_ja")
    backups_docx_ja_hrkt = os.path.join(backups_base, "Docx_ja-Hrkt")

    # Create all folders
    for d in [
        base_output, sprites_dir, text_en_dir, text_ja_dir, text_ja_hrkt_dir,
        docx_en_dir, docx_ja_dir, docx_ja_hrkt_dir,
        backups_text_en, backups_text_ja, backups_text_ja_hrkt,
        backups_docx_en, backups_docx_ja, backups_docx_ja_hrkt
    ]:
        os.makedirs(d, exist_ok=True)

    # Return dictionary for easy access
    return {
        "sprites": sprites_dir,
        "text_en": text_en_dir,
        "text_ja": text_ja_dir,
        "text_ja_hrkt": text_ja_hrkt_dir,
        "docx_en": docx_en_dir,
        "docx_ja": docx_ja_dir,
        "docx_ja_hrkt": docx_ja_hrkt_dir,
        "backups_text_en": backups_text_en,
        "backups_text_ja": backups_text_ja,
        "backups_text_ja_hrkt": backups_text_ja_hrkt,
        "backups_docx_en": backups_docx_en,
        "backups_docx_ja": backups_docx_ja,
        "backups_docx_ja_hrkt": backups_docx_ja_hrkt,
    }
