import logging
import sys
from pathlib import Path
from datetime import datetime

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)
log_file = LOG_DIR / f"novel_app_{datetime.now().strftime('%Y%m%d')}.log"

LOG_FORMAT = (
    "%(asctime)s | %(levelname)-8s | "
    "%(filename)s:%(lineno)d (%(funcName)s) | %(message)s"
)

def setup_logger():
    logger = logging.getLogger("novel_app")
    
    if logger.hasHandlers():
        return logger

    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(LOG_FORMAT, datefmt='%Y-%m-%d %H:%M:%S')

    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

logger = setup_logger()