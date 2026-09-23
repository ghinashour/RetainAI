import logging
import sys
from typing import Any

from app.core.config import get_settings


def setup_logging() -> logging.Logger:
    settings = get_settings()
    logger = logging.getLogger("retainai")
    logger.setLevel(getattr(logging, settings.log_level.upper(), logging.INFO))
    logger.propagate = False

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(
            logging.Formatter(
                "%(asctime)s %(levelname)s %(name)s %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )
        )
        logger.addHandler(handler)

    return logger


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(f"retainai.{name}")
    if not logger.handlers:
        logger.handlers = logging.getLogger("retainai").handlers
    return logger


def log_context(**context: Any) -> dict[str, Any]:
    return {"service": "retainai-api", "environment": get_settings().app_env, **context}
