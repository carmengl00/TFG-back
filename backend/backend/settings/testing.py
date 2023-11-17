import os

from .local import *  # NOQA

# Database is changed because we do use circleCI to save time in processing we do use
# sqlite for this tests
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("DB_NAME", "backend"),
        "USER": os.environ.get("DB_USER", "backend"),
        "PASSWORD": os.environ.get("DB_PASSWORD", "backend!"),
        "HOST": os.environ.get("DB_HOST", "database"),
        "PORT": os.environ.get("DB_PORT", ""),
    }
}

# FAKE SECRET KEY FOR TESTING (https://djecrety.ir/)
SECRET_KEY = "3!j6t410mf*v)z1@o1w&xymv3e&$uoc4g0n%w&zjqc1bseidb0"
