import logging
import os
from logging.config import dictConfig
from common.settings import LOG_LEVEL

from pydantic import BaseModel


class LastPartFilter(logging.Filter):
    def filter(self, record):
        cwd = os.getcwd()
        module_path = []
        split_path = record.pathname[len(cwd)::].rsplit('\\')
        for split in split_path:
            module_path.append(split.lower())
        module_path[-1] = module_path[-1].split(".")[0]
        module_path = module_path[1:]
        record.module_path = ".".join(module_path)
        return True


class LogConfig(BaseModel):
    """Logging configuration to be set for the server"""

    LOGGER_NAME: str = "logger"
    LOG_LEVEL: str = LOG_LEVEL

    # Logging config
    version: int = 1
    disable_existing_loggers: bool = False
    formatters: dict = {
        "default": {
            "()": "common.logging_config.formatter.CustomFormatter",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    }
    handlers: dict = {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
            "filters": [LastPartFilter()],
        },
    }
    loggers: dict = {
        "": {"handlers": ["default"], "level": LOG_LEVEL},
    }


logging.config.dictConfig(LogConfig().dict())
