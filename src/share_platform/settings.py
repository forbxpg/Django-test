"""Модуль для настроек проекта."""

import os
from datetime import timedelta
from pathlib import Path

from django.core.management.utils import get_random_secret_key
from dotenv import load_dotenv


load_dotenv()


AUTH_USER_MODEL = "users.User"

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get("SECRET_KEY", default=get_random_secret_key)

DEBUG = os.environ.get("DEBUG", default="false").lower() == "true"

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", default="*").split(",")

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # third party apps
    "django_filters",
    "djoser",
    "rest_framework",
    "rest_framework_simplejwt",
    "tailwind",
    "theme",
    "unfold",
    "unfold.contrib.filters",
    "unfold.contrib.forms",
    "unfold.contrib.inlines",
    "unfold.contrib.import_export",
    "unfold.contrib.guardian",
    "unfold.contrib.simple_history",
    "django.contrib.admin",
    # local apps
    "ads.apps.AdsConfig",
    "api.apps.ApiConfig",
    "exchanges.apps.ExchangesConfig",
    "users.apps.UsersConfig",
]

TAILWIND_APP_NAME = "theme"
INTERNAL_IPS = os.environ.get(
    "INTERNAL_IPS", default="127.0.0.1,0.0.0.0"
).split(",")

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

BROWSER_RELOAD = (
    os.environ.get("BROWSER_RELOAD", default="false").lower() == "true"
)

if BROWSER_RELOAD:
    INSTALLED_APPS.append("django_browser_reload")
    MIDDLEWARE.append(
        "django_browser_reload.middleware.BrowserReloadMiddleware",
    )

ROOT_URLCONF = "share_platform.urls"

TEMPLATES_DIRS = BASE_DIR / "templates"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            TEMPLATES_DIRS,
        ],
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

WSGI_APPLICATION = "share_platform.wsgi.application"


if os.environ.get("USE_SQLITE", default="true").lower() == "true":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

if os.environ.get("USE_POSTGRES", default="false").lower() == "true":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.environ.get("POSTGRES_DB", default="share_platform"),
            "USER": os.environ.get("POSTGRES_USER", default="postgres"),
            "PASSWORD": os.environ.get(
                "POSTGRES_PASSWORD", default="password"
            ),
            "HOST": os.environ.get("POSTGRES_HOST", default="localhost"),
            "PORT": os.environ.get("POSTGRES_PORT", default="5432"),
        }
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

LANGUAGE_CODE = "ru-RU"

TIME_ZONE = "Europe/Moscow"

USE_I18N = True

USE_TZ = True

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "static"

# Номера телефонов
PHONENUMBER_DEFAULT_REGION = "RU"
PHONENUMBER_DB_FORMAT = "INTERNATIONAL"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGIN_REDIRECT_URL = "/ads/"

LOGIN_URL = "users:login"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ],
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=30),
    "AUTH_HEADER_TYPES": ("Bearer",),
}

DJOSER = {
    "SERIALIZERS": {
        "user": "api.v1.serializers.user.UserSerializer",
        "current_user": "api.v1.serializers.user.UserSerializer",
    },
}

NPM_BIN_PATH = os.environ.get("NPM_BIN_PATH", default="/usr/bin/npm")
