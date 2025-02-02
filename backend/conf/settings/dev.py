from conf.settings.base import *  # noqa: F403

DEBUG = False

LOGGING["loggers"]["django.db.backends"] = {
    "handlers": ["file"],
    "level": "DEBUG",
    "propagate": False,
}

DEFAULT_HOST = "https://kboapp.xyz"
