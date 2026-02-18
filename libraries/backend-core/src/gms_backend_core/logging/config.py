import logging
import sys

from pythonjsonlogger import json

from ..config import GmsBackendSettings


def setup_logging(settings: GmsBackendSettings):
    log_level_str = settings.log_level.upper()
    log_level = getattr(logging, log_level_str, logging.INFO)

    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    handler = logging.StreamHandler(sys.stdout)
    formatter = json.JsonFormatter(
        "%(asctime)s %(levelname)s %(name)s %(message)s", datefmt="%Y-%m-%dT%H:%M:%SZ"
    )

    handler.setFormatter(formatter)
    root_logger.addHandler(handler)

    loggers_to_propagate = (
        "uvicorn",
        "uvicorn.error",
        "uvicorn.access",
        "fastapi",
        "httpx",
        "httpcore",
    )
    for logger_name in loggers_to_propagate:
        child_logger = logging.getLogger(logger_name)
        child_logger.handlers = []
        child_logger.propagate = True

        if log_level == logging.INFO and logger_name in ("httpx", "httpcore"):
            child_logger.setLevel(logging.WARNING)

    logging.info(f"Logging initialized in {settings.environment} mode with level {log_level_str}")
