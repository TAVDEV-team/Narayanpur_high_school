import os
from pathlib import Path
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent
LOG_LEVEL = config("LOG_LEVEL", default="INFO")

# Only used locally — Render's filesystem is ephemeral, so file logs
# there would just disappear on every restart/redeploy anyway.
IS_PRODUCTION = config("RENDER", default=False, cast=bool)


def get_logger(debug: bool) -> dict:
    handlers = {
        "console": {
            "level": "DEBUG" if debug else "INFO",
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
    }

    app_handlers = ["console"]
    django_handlers = ["console"]
    error_handlers = ["console"]

    if not IS_PRODUCTION:
        logs_dir = BASE_DIR / "logs"
        os.makedirs(logs_dir, exist_ok=True)

        handlers["file"] = {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": logs_dir / "django.log",
            "maxBytes": 5 * 1024 * 1024,
            "backupCount": 5,
            "formatter": "verbose",
        }
        handlers["error_file"] = {
            "level": "ERROR",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": logs_dir / "errors.log",
            "maxBytes": 5 * 1024 * 1024,
            "backupCount": 5,
            "formatter": "verbose",
        }
        app_handlers.append("file")
        django_handlers.append("file")
        error_handlers.append("error_file")

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
        "handlers": handlers,
        "root": {
            "handlers": ["console"],
            "level": "WARNING",
        },
        "loggers": {
            "django": {
                "handlers": django_handlers,
                "level": "INFO",
                "propagate": False,
            },
            "django.request": {
                "handlers": error_handlers,
                "level": "ERROR",
                "propagate": False,
            },
            "django.db.backends": {
                "handlers": ["console"],
                "level": "WARNING",
                "propagate": False,
            },
            "accounts": {
                "handlers": app_handlers,
                "level": LOG_LEVEL,
                "propagate": False,
            },
            "fund": {
                "handlers": app_handlers,
                "level": LOG_LEVEL,
                "propagate": False,
            },
            "nphs_school": {
                "handlers": app_handlers,
                "level": LOG_LEVEL,
                "propagate": False,
            },
            "results": {
                "handlers": app_handlers,
                "level": LOG_LEVEL,
                "propagate": False,
            },
            "gallery": {
                "handlers": app_handlers,
                "level": LOG_LEVEL,
                "propagate": False,
            },
        },
    }
