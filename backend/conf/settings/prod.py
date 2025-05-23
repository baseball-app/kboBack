from conf.settings.base import *  # noqa: F403

DEBUG = False
ALLOWED_HOSTS = ["kboapp.xyz", "www.kboapp.xyz", "localhost", "127.0.0.1"]
CSRF_TRUSTED_ORIGINS = [
    "https://kboapp.xyz",
]
DEFAULT_HOST = "https://kboapp.xyz"

# Sentry 설정
sentry_sdk.init(
    dsn=config["sentry"].get("dsn_url", ""),
    integrations=[
        DjangoIntegration(),
    ],
    traces_sample_rate=1.0,
    send_default_pii=True
)

# Environment
ENVIRONMENT = "prod"
