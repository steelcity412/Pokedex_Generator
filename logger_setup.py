import os
import logging
from logging.handlers import RotatingFileHandler

def get_logger(base_output: str):
    """
    Creates a logger that writes to BOTH console and a rotating log file.
    This keeps runtime output readable while also preserving detailed logs.
    """

    # Ensure logs directory exists
    logs_dir = os.path.join(base_output, "logs")
    os.makedirs(logs_dir, exist_ok=True)

    log_file = os.path.join(logs_dir, "pokedex.log")

    # Create main logger
    logger = logging.getLogger("pokedex")
    logger.setLevel(logging.DEBUG)

    # Prevent duplicate handlers if logger is reused
    if logger.handlers:
        return logger

    # Console handler (INFO level)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))

    # File handler (DEBUG level, rotating)
    fh = RotatingFileHandler(
        log_file,
        maxBytes=2_000_000,   # 2 MB per file
        backupCount=5,        # Keep 5 old logs
        encoding="utf-8"
    )
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

    # Attach handlers
    logger.addHandler(ch)
    logger.addHandler(fh)

    return logger
