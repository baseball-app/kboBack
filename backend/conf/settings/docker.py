from conf.settings.base import *  # noqa: F403

DEBUG = True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config["database"]["docker"]["name"],
        "USER": config["database"]["docker"]["user"],
        "PASSWORD": config["database"]["docker"]["password"],
        "HOST": config["database"]["docker"]["host"],
        "PORT": config["database"]["docker"]["port"],
    }
}