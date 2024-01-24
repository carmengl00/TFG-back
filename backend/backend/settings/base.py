import os
from datetime import timedelta

import dj_email_url
from pytimeparse import parse

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "3!j6t410mf*v)z1@o1w&xymv3e&$uoc4g0n%w&zjqc1bseidb0"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

INTERNAL_IPS = ["localhost"]

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "strawberry_django_jwt.refresh_token",
    "rest_framework",
    "rest_framework.authtoken",
    "base",
    "media_upload",
    "users",
    "resources",
    "slots",
    "corsheaders",
    "health_check",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "backend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "backend.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("DB_NAME", "backend"),
        "USER": os.environ.get("DB_USER", "backend"),
        "PASSWORD": os.environ.get("DB_PASSWORD", "backend!"),
        "HOST": os.environ.get("DB_HOST", "database"),
        "PORT": os.environ.get("DB_PORT", ""),
        # http://www.revsys.com/blog/2015/may/06/django-performance-simple-things
        # persistent DB connection
        "CONN_MAX_AGE": 60 * 5,  # 5 minutes
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
        ),
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 100,
}


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static_root")

# Auth User Model
AUTH_USER_MODEL = "users.User"

AUTHENTICATION_BACKENDS = [
    "users.backends.JSONWebTokenBackend",
    "django.contrib.auth.backends.ModelBackend",
]

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media_root")

MEDIA_UPLOAD_BACKEND = os.getenv(
    "MEDIA_UPLOAD_BACKEND", "media_upload.backends.local.LocalMediaUploadBackend"
)
URL_FRONT = os.getenv("URL_FRONT", "backend:/")
URL_API = os.getenv("URL_API", "localhost")

# EMAIL
EMAIL_URL = os.environ.get("EMAIL_URL")

# Documentation: https://github.com/migonzalvar/dj-email-url
email_config = dj_email_url.parse(EMAIL_URL or "smtp://mailhog:1025")

EMAIL_BACKEND = email_config["EMAIL_BACKEND"]
EMAIL_FILE_PATH = email_config["EMAIL_FILE_PATH"]
EMAIL_HOST_USER = email_config["EMAIL_HOST_USER"]
EMAIL_HOST_PASSWORD = email_config["EMAIL_HOST_PASSWORD"]
EMAIL_HOST = email_config["EMAIL_HOST"]
EMAIL_PORT = email_config["EMAIL_PORT"]
EMAIL_USE_TLS = email_config["EMAIL_USE_TLS"]
EMAIL_USE_SSL = email_config["EMAIL_USE_SSL"]
EMAIL_TIMEOUT = email_config["EMAIL_TIMEOUT"]

CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL")
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_RESULT_SERIALIZER = "json"
CELERY_TASK_SERIALIZER = "json"
CORS_ALLOW_ALL_ORIGINS = True
# CORS_ALLOWED_ORIGINS = [""] # TODO set this VAR on PRODUCTION
CORS_ALLOW_CREDENTIALS = True


# Redis

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": f"{CELERY_BROKER_URL}/1",
    }
}
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

CELERY_BEAT_SCHEDULE = {}

# Form uploads
DATA_UPLOAD_MAX_NUMBER_FIELDS = 5000  # default 1000
DATA_UPLOAD_MAX_MEMORY_SIZE = 1024 * 1024 * 5  # default 2.5 MB (2621440)

APP_CONFIG = None

GRAPHQL_JWT = {"JWT_AUTHENTICATE_INTROSPECTION": False}


# JWT
JWT_EXPIRE = bool(os.environ.get("JWT_EXPIRE") or 1)
JWT_TTL_ACCESS = os.environ.get("JWT_TTL_ACCESS") or "1 day"
JWT_TTL_ACCESS_TIMEDELTA = timedelta(seconds=parse(JWT_TTL_ACCESS))
JWT_TTL_REFRESH = os.environ.get("JWT_TTL_REFRESH") or "30 days"
JWT_TTL_REFRESH_TIMEDELTA = timedelta(seconds=parse(JWT_TTL_REFRESH))
