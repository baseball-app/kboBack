#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""

import sys
import logging


from conf.utils import set_environment


def main():
    """Run administrative tasks."""
    set_environment()

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
