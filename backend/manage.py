#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""

import os
import sys
import logging
from pathlib import Path

import toml


def main():
    """Run administrative tasks."""
    config = toml.load(Path(__file__).resolve().parent / "config.toml")

    env = config["django"]["env"]
    if env == "prod":
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "conf.settings.prod")
    elif env == "dev":
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "conf.settings.dev")
    else:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "conf.settings.local")

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    logging.basicConfig(
        stream=sys.stdout,
        level=logging.DEBUG,
        format="%(asctime)s %(levelname)s %(message)s",
    )

    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
