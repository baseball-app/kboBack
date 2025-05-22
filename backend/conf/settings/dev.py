from conf.settings.base import *  # noqa: F403

DEBUG = False
ALLOWED_HOSTS = ["dev.kboapp.xyz", "kboapp.xyz", "www.kboapp.xyz", "localhost", "127.0.0.1"]
CSRF_TRUSTED_ORIGINS = [
    "https://dev.kboapp.xyz",
    "https://kboapp.xyz",
]
DEFAULT_HOST = "https://dev.kboapp.xyz"

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")  # noqa: F405
