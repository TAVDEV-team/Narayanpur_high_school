import os
from pathlib import Path
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent
LOGS_DIR = BASE_DIR / "logs"
os.makedirs(LOGS_DIR, exist_ok=True)

LOG_LEVEL = config("LOG_LEVEL", default="INFO")


def get_logging_config(debug: bool) -> dict:
    return {
        "version": 1,
        "disable_existing_loggers": False,

        "formatters": {
            "verbose": {
                "format": "[{asctime}] {levelname} {name} - {message}",
                "style": "{",
            },
            "simple": {
                "format": "{levelname} {message}",
                "style": "{",
            },
        },

        "handlers": {
            "console": {
                "level": "DEBUG" if debug else "INFO",
                "class": "logging.StreamHandler",
                "formatter": "simple",
            },
            "file": {
                "level": "INFO",
                "class": "logging.handlers.RotatingFileHandler",
                "filename": LOGS_DIR / "django.log",
                "maxBytes": 5 * 1024 * 1024,
                "backupCount": 5,
                "formatter": "verbose",
            },
            "error_file": {
                "level": "ERROR",
                "class": "logging.handlers.RotatingFileHandler",
                "filename": LOGS_DIR / "errors.log",
                "maxBytes": 5 * 1024 * 1024,
                "backupCount": 5,
                "formatter": "verbose",
            },
        },

        "root": {
            "handlers": ["console"],
            "level": "WARNING",
        },

        "loggers": {
            "django": {
                "handlers": ["console", "file"],
                "level": "INFO",
                "propagate": False,
            },
            "django.request": {
                "handlers": ["console", "error_file"],
                "level": "ERROR",
                "propagate": False,
            },
            "django.db.backends": {
                "handlers": ["console"],
                "level": "WARNING",
                "propagate": False,
            },
            "accounts": {
                "handlers": ["console", "file"],
                "level": LOG_LEVEL,
                "propagate": False,
            },
            "fund": {
                "handlers": ["console", "file"],
                "level": LOG_LEVEL,
                "propagate": False,
            },
            "nphs_school": {
                "handlers": ["console", "file"],
                "level": LOG_LEVEL,
                "propagate": False,
            },
            "results": {
                "handlers": ["console", "file"],
                "level": LOG_LEVEL,
                "propagate": False,
            },
            "gallery": {
                "handlers": ["console", "file"],
                "level": LOG_LEVEL,
                "propagate": False,
            },
        },
    }
