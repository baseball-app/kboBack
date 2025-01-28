from conf.settings.base import *  # noqa: F403

DEBUG = True
CORS_ORIGIN_ALLOW_ALL = True

LOGGING["loggers"]["django.db.backends"] = {
    "handlers": ["console"],
    "level": "DEBUG",
    "propagate": False,
}
