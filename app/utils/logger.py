import logging
import sys
from typing import Any

from app.core.config import settings


def get_logger(name: str) -> logging.Logger:
    """Get a configured logger instance."""
    logger = logging.getLogger(name)
    
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(
            logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
        )
        logger.addHandler(handler)
    
    logger.setLevel(
        logging.DEBUG if settings.DEBUG else logging.INFO
    )
    
    return logger


# Application logger
logger = get_logger("mealsight")
