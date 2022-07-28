from __future__ import annotations

from django.contrib import admin
from django.http import HttpResponse
from django.urls import include, path


def a_root_view(request):
    return HttpResponse()  # pragma: no cover


urlpatterns = [
    path("admin/", admin.site.urls),
    path("root-view/", a_root_view, name="test-root-view"),
    path("nested/", include("tests.nested_urls")),
]
