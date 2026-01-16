"""
Central logging utility for Physician Notetaker

Provides:
- Console logging
- File-based logging
- Standard log formatting

Python version: 3.13.5
"""

import logging
import os
from datetime import datetime


# -------------------------------------------------------------------
# Logger Configuration
# -------------------------------------------------------------------

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(
    LOG_DIR,
    f"physician_notetaker_{datetime.utcnow().strftime('%Y%m%d')}.log"
)


def get_logger(name: str) -> logging.Logger:
    """
    Create and return a configured logger.

    Args:
        name (str): Logger name (usually __name__)

    Returns:
        logging.Logger
    """

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Prevent duplicate handlers
    if logger.handlers:
        return logger

    # Formatter
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # File handler
    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    # Attach handlers
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger