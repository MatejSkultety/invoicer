"""
Logging configuration for the BFF application.
"""

import logging
import logging.config
from .config import settings

LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_DEFAULT_HANDLERS = ["console"]

# Use settings from our config instead of direct env access
IS_DEBUG_MODE = settings.DEBUG_MODE

# Determine log level from settings or debug mode
if IS_DEBUG_MODE:
    ROOT_LOG_LEVEL = logging.DEBUG
else:
    ROOT_LOG_LEVEL = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)

# Libraries that can be noisy in production
NOISY_LIBS = [
    "httpx", "uvicorn",
    "urllib3", "asyncio"
]

# Base loggers configuration
loggers_config = {
    "root": {
        "level": ROOT_LOG_LEVEL,
        "handlers": LOG_DEFAULT_HANDLERS,
    },
    "backend": {  # Our application logger
        "level": ROOT_LOG_LEVEL,
        "handlers": LOG_DEFAULT_HANDLERS,
        "propagate": False,
    },
}

# Main logging configuration
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": LOG_FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "detailed": {
            "format": (
                "%(asctime)s - %(name)s - %(levelname)s - "
                "%(filename)s:%(lineno)d - %(funcName)s - %(message)s"
            ),
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "detailed" if IS_DEBUG_MODE else "default",
            "stream": "ext://sys.stdout",
        },
    },
    "loggers": loggers_config,
}

# Configure uvicorn loggers
LOGGING_CONFIG["loggers"]["uvicorn.error"] = {
    "level": logging.INFO,
    "propagate": True,
}
LOGGING_CONFIG["loggers"]["uvicorn.access"] = {
    "handlers": LOG_DEFAULT_HANDLERS,
    "level": logging.INFO,
    "propagate": False,
}

# Reduce noise from third-party libraries in production
if not IS_DEBUG_MODE:
    for lib in NOISY_LIBS:
        LOGGING_CONFIG["loggers"][lib] = {
            "level": logging.WARNING, 
            "propagate": True
        }


def configure_logging() -> None:
    """Configure logging for the application."""
    logging.config.dictConfig(LOGGING_CONFIG)
    
    # Log the configuration
    logger = logging.getLogger("bff")
    logger.info("Logging configured successfully")
    logger.info(f"Debug mode: {IS_DEBUG_MODE}")
    logger.info(f"Log level: {logging.getLevelName(ROOT_LOG_LEVEL)}")


# Configure logging when module is imported
configure_logging()
