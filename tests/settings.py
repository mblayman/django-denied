# Heavily inspired by the test settings in django_htmx.
from __future__ import annotations

from typing import Any

SECRET_KEY = "NOTASECRET"

ALLOWED_HOSTS: list[str] = []

DATABASES: dict[str, dict[str, Any]] = {}

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
]

MIDDLEWARE: list[str] = []

ROOT_URLCONF = "tests.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "OPTIONS": {"context_processors": []},
    }
]

USE_TZ = True

# The default for MEDIA_URL is an empty string, but something is the test setup
# is setting it to "/". This is super annoying because it messes up the middleware
# processing. Since there are explicit tests to check when MEDIA_URL is an empty string
# or has a value, this is set to something that won't conflict.
MEDIA_URL = "/not-a-path-that-the-suite-tests-against/"
