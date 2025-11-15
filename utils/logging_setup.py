# logging_setup.py (możesz też wkleić bezpośrednio do komórki)
import logging
from pathlib import Path
from logging.handlers import RotatingFileHandler

def setup_logging(log_dir: Path = Path("logs"), log_name: str = "pipeline.log",
                  level=logging.INFO, max_bytes=10_000_000, backup_count=3):
    """
    Konfiguruje logger:
    - plik logs/pipeline.log (rotacja),
    - wypis na stdout (StreamHandler).
    - bez duplikowania handlerów (ważne w notebooku).
    """
    log_dir = Path(log_dir)
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / log_name

    logger = logging.getLogger()  # root logger
    logger.setLevel(level)

    # Usuń stare handlery (przy wielokrotnym uruchamianiu w notebooku)
    if logger.handlers:
        logger.handlers = []

    # File handler z rotacją
    fh = RotatingFileHandler(log_file, maxBytes=max_bytes, backupCount=backup_count, encoding="utf-8")
    fh.setLevel(level)
    fh.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(message)s"))

    # Console handler
    ch = logging.StreamHandler()
    ch.setLevel(level)
    ch.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

    logger.addHandler(fh)
    logger.addHandler(ch)

    logger.info(f"Logging uruchomiony. Logi -> {log_file.resolve()}")
    return logger, log_file