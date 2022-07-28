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
