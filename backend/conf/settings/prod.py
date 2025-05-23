from conf.settings.base import *  # noqa: F403

DEBUG = False
ALLOWED_HOSTS = ["kboapp.xyz", "www.kboapp.xyz", "localhost", "127.0.0.1"]
CSRF_TRUSTED_ORIGINS = [
    "https://kboapp.xyz",
]
DEFAULT_HOST = "https://kboapp.xyz"

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")  # noqa: F405

# Environment
ENVIRONMENT = "prod"
