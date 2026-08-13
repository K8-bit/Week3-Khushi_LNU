from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Union

DEFAULT_LOG_FILE = Path("app.log")
DEFAULT_LOG_LEVEL = logging.INFO
APP_LOGGER_NAME = "product"

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

MAX_LOG_SIZE = 5 * 1024 * 1024
BACKUP_COUNT = 3
HANDLER_MARKER = "_product_file_handler"

logger = logging.getLogger(__name__)


def configure_logging(
    log_file: Union[str, Path] = DEFAULT_LOG_FILE,
    level: int = DEFAULT_LOG_LEVEL,
) -> logging.Logger:
    """Configure file logging for the application."""

    log_path = Path(log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    application_logger = logging.getLogger(APP_LOGGER_NAME)
    application_logger.setLevel(level)
    application_logger.propagate = False

    for handler in application_logger.handlers[:]:
        if getattr(handler, HANDLER_MARKER, False):
            application_logger.removeHandler(handler)
            handler.close()

    file_handler = RotatingFileHandler(
        filename=log_path,
        maxBytes=MAX_LOG_SIZE,
        backupCount=BACKUP_COUNT,
        encoding="utf-8",
    )

    file_handler.setLevel(level)
    file_handler.setFormatter(
        logging.Formatter(
            fmt=LOG_FORMAT,
            datefmt=DATE_FORMAT,
        )
    )

    setattr(file_handler, HANDLER_MARKER, True)
    application_logger.addHandler(file_handler)

    return application_logger
