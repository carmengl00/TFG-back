import json
import os

from base.secretsmanager import SecretManager

from ..settings.base import *  # NOQA

secrets = SecretManager(secret_name=os.environ.get("SECRETS_NAME_ENV"))

DEBUG = secrets.get_secret("DEBUG") == "True"
SECRET_KEY = secrets.get_secret("DJANGO_SECRET_KEY")

VERSION = secrets.get_secret("VERSION")

URL_API = secrets.get_secret("URL_API")
URL_FRONT = secrets.get_secret("URL_FRONT")

ALLOWED_HOSTS = json.loads(secrets.get_secret("ALLOWED_HOSTS"))
CORS_ALLOW_ALL_ORIGINS = secrets.get_secret("CORS_ALLOW_ALL_ORIGINS") == "True"

CORS_ORIGIN_REGEX_WHITELIST = [r"^https://\w+\.ngrok\.io$"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": secrets.get_secret("DB_NAME"),
        "USER": secrets.get_secret("DB_USER"),
        "PASSWORD": secrets.get_secret("DB_PASSWORD"),
        "HOST": secrets.get_secret("DB_HOST"),
        "PORT": secrets.get_secret("DB_PORT"),
        "OPTIONS": {"sslmode": "require"},
    }
}

AWS_ACCESS_KEY_ID = secrets.get_secret("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = secrets.get_secret("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = secrets.get_secret("AWS_STORAGE_BUCKET_NAME")
AWS_S3_REGION_NAME = secrets.get_secret("AWS_S3_REGION_NAME")
AWS_S3_CUSTOM_DOMAIN = "%s.s3.amazonaws.com" % AWS_STORAGE_BUCKET_NAME
AWS_DEFAULT_ACL = "public-read"

# Redis
_redis_host = secrets.get_secret("REDIS_HOST")
CELERY_BROKER_URL = f"redis://{_redis_host}:6379/0"
BROKER_TRANSPORT = "redis"
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_RESULT_SERIALIZER = "json"
CELERY_TASK_SERIALIZER = "json"

SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": f"{CELERY_BROKER_URL}/1",
    }
}
# s3 static settings
AWS_LOCATION = "static"
STATIC_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_LOCATION}/"
STATICFILES_STORAGE = "base.storage.StaticStorage"

# s3 public media settings
PUBLIC_MEDIA_LOCATION = "media"
MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{PUBLIC_MEDIA_LOCATION}/"
DEFAULT_FILE_STORAGE = "base.storage.PublicMediaStorage"

# s3 private media settings
PRIVATE_MEDIA_LOCATION = "private"
PRIVATE_MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{PRIVATE_MEDIA_LOCATION}/"
PRIVATE_FILE_STORAGE = "base.storage.PrivateMediaStorage"

MEDIA_UPLOAD_BACKEND = os.getenv(
    "MEDIA_UPLOAD_BACKEND", "media_upload.backends.s3.S3MediaUploadBackend"
)

MEDIA_UPLOAD_TOKEN_EXPIRATION = 300
MEDIA_DOWNLOAD_TOKEN_EXPIRATION = 9000

# Email
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = secrets.get_secret("EMAIL_HOST")
EMAIL_PORT = secrets.get_secret("EMAIL_PORT")
EMAIL_HOST_USER = secrets.get_secret("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = secrets.get_secret("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = secrets.get_secret("EMAIL_USE_TLS") == "True"
DEFAULT_FROM_EMAIL = secrets.get_secret("DEFAULT_FROM_EMAIL")
SUPPORT_EMAIL = secrets.get_secret("SUPPORT_EMAIL")
