import os
from pathlib import Path

import toml


def set_environment():
    config = toml.load(Path(__file__).resolve().parent.parent / "config.toml")
    env = config["django"]["env"]
    if env == "prod":
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "conf.settings.prod")
    elif env == "dev":
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "conf.settings.dev")
    else:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "conf.settings.local")
