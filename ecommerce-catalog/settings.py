# settings.py
import os
from datetime import timedelta
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

INSTALLED_APPS = [
    # django defaults...
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # third-party
    'rest_framework',
    'rest_framework.authtoken',
    'django_filters',
    'drf_yasg',            # swagger ui

    # local apps
    'store',
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("POSTGRES_DB", "ecommerce_db"),
        "USER": os.environ.get("POSTGRES_USER", "ecommerce_user"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD", "changeme"),
        "HOST": os.environ.get("POSTGRES_HOST", "localhost"),
        "PORT": os.environ.get("POSTGRES_PORT", "5432"),
    }
}

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
REST_FRAMEWORK['DEFAULT_PAGINATION_CLASS'] = 'rest_framework.pagination.CursorPagination'
REST_FRAMEWORK['PAGE_SIZE'] = 20
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ),
    "DEFAULT_PAGINATION_CLASS": "store.pagination.StandardResultsSetPagination",
    "PAGE_SIZE": 12,
    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.OrderingFilter",
        "rest_framework.filters.SearchFilter",
    ),
}

# Simple JWT config
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "AUTH_HEADER_TYPES": ("Bearer",),
}

# CORS
# pip install django-cors-headers if using
# INSTALLED_APPS += ['corsheaders']
# MIDDLEWARE = ['corsheaders.middleware.CorsMiddleware', ...]
# CORS_ALLOWED_ORIGINS = ["http://localhost:3000"]

# Static and media
STATIC_URL = "/static/"
MEDIA_URL = "/media/"
