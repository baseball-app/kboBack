from conf.settings.base import *  # noqa: F403

DEBUG = False
ALLOWED_HOSTS = ['kboapp.xyz', 'www.kboapp.xyz', 'localhost', '127.0.0.1']
CSRF_TRUSTED_ORIGINS = [
    'https://kboapp.xyz',
]
DEFAULT_HOST = "https://kboapp.xyz"
