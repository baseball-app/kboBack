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
]

THIRD_PARTY_APPS = [
    "rest_framework",
    "oauth2_provider",
    "django_extensions",
    "drf_spectacular",
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
        "oauth2_provider.contrib.rest_framework.OAuth2Authentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

AUTHENTICATION_BACKENDS = ("django.contrib.auth.backends.ModelBackend",)

SESSION_COOKIE_AGE = 1209600

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
            "Bearer": {
                "type": "apiKey",
                "name": "Authorization",
                "in": "header",
            }
        }
    },
    "SECURITY": [{"Bearer": []}],
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
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

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

STATIC_URL = "static/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
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
