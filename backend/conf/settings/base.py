import os
from pathlib import Path

import toml

BASE_DIR = Path(__file__).resolve().parent.parent.parent

config = toml.load(BASE_DIR / "config.toml")

SECRET_KEY = config["django"]["secret_key"]

ALLOWED_HOSTS = ["*"]

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

PROJECT_APPS = [
    "apps.users",
    "apps.tickets",
    "apps.games",
    "apps.alerts",
    "apps.auths",
    "apps.notifications",
    "apps.teams",
]

THIRD_PARTY_APPS = [
    "rest_framework",
    "oauth2_provider",
    "django_extensions",
    "drf_spectacular",
    "django_celery_beat",
    "django_celery_results",
]

INSTALLED_APPS = DJANGO_APPS + PROJECT_APPS + THIRD_PARTY_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "corsheaders.middleware.CorsMiddleware",
]

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "base.authentication.CustomHeaderAuthentication",
        "oauth2_provider.contrib.rest_framework.OAuth2Authentication",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

AUTHENTICATION_BACKENDS = ("django.contrib.auth.backends.ModelBackend",)

CUSTOM_HEADER_NAME = "HTTP_X_KBOAPP_TOKEN"

OAUTH2_PROVIDER = {
    "SCOPES": {"read": "Read scope", "write": "Write scope"},
}

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

SITE_NAME = "KBO Backend"
SPECTACULAR_SETTINGS = {
    "TITLE": f"{SITE_NAME} API",
    "DESCRIPTION": f"{SITE_NAME}의 API입니다.",
    "APPEND_COMPONENTS": {
        "securitySchemes": {
            "X-KBOAPP-TOKEN": {
                "type": "apiKey",
                "name": "X-KBOAPP-TOKEN",
                "in": "header",
                "description": "Custom authentication token for KBO App",
            }
        }
    },
    "SECURITY": [{"X-KBOAPP-TOKEN": []}],
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": True,
    "SERVE_AUTHENTICATION": [],
}

ROOT_URLCONF = "conf.urls"

WSGI_APPLICATION = "conf.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config["database"]["name"],
        "USER": config["database"]["user"],
        "PASSWORD": config["database"]["password"],
        "HOST": config["database"]["host"],
        "PORT": config["database"]["port"],
    }
}

AUTH_USER_MODEL = "users.User"

DEFAULT_EXIRES_IN = 3600

SOCIAL_LOGIN = {
    "NAVER": {
        "CLIENT_ID": config["api_keys"]["naver"]["client_id"],
        "CLIENT_SECRET": config["api_keys"]["naver"]["client_secret"],
    },
    "KAKAO": {
        "CLIENT_ID": config["api_keys"]["kakao"]["client_id"],
        "CLIENT_SECRET": config["api_keys"]["kakao"]["client_secret"],
    },
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Seoul"

USE_I18N = True

USE_TZ = True

STATIC_URL = "static/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "[{levelname}] {asctime} {module} {message}",
            "style": "{",
        },
        "simple": {
            "format": "[{levelname}] {message}",
            "style": "{",
        },
    },
    "handlers": {
        "file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "django.log"),
            "formatter": "verbose",
        },
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": True,
        },
    },
}

# Celery
CELERY_BROKER_URL = config["celery"]["broker_url"]
CELERY_RESULT_BACKEND = config["celery"]["result_backend"]
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = "Asia/Seoul"

# AWS
AWS_S3_ACCESS_KEY = config["aws"].get("AWS_S3_ACCESS_KEY", "")
AWS_S3_SECRET_KEY = config["aws"].get("AWS_S3_SECRET_KEY", "")
AWS_S3_STORAGE_BUCKET_NAME = config["aws"].get("AWS_S3_STORAGE_BUCKET_NAME", "")
AWS_S3_REGION_NAME = config["aws"].get("AWS_S3_REGION_NAME", "ap-northeast-2")
AWS_S3_CUSTOM_DOMAIN = config["aws"].get("AWS_S3_CUSTOM_DOMAIN", "")

DEFAULT_HOST = "http://localhost:8000"
