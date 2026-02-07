"""Django settings for analytics service."""
import os

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "dev-secret-key-for-testing-only")

DEBUG = True
ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.auth",
    "rest_framework",
    "analytics_app",
]

ROOT_URLCONF = "analytics.urls"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

