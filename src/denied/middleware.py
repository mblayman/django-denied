from __future__ import annotations

from typing import Callable

from django.conf import settings
from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import PermissionDenied
from django.http import HttpRequest, HttpResponse
from django.urls import reverse_lazy

LOGIN_URLS = {
    settings.LOGIN_URL,
    reverse_lazy("admin:login"),
}


class DeniedMiddleware:
    """This middleware will deny all calls by default.

    A view must provide an authorizer that will return a boolean status
    to indicate whether to proceed or not.
    """

    def __init__(self, get_response: Callable) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        return self.get_response(request)

    def process_view(
        self,
        request: HttpRequest,
        view_func: Callable,
        view_args: list,
        view_kwargs: dict,
    ) -> HttpResponse | None:
        """Process the view by checking against an authorizer."""
        if (
            getattr(view_func, "__denied_exempt__", False)
            # Or check on a bound method
            or getattr(getattr(view_func, "__func__", None), "__denied_exempt__", False)
        ):
            return None

        if not request.user.is_authenticated and request.path not in LOGIN_URLS:
            return redirect_to_login(request.get_full_path())

        if not hasattr(view_func, "__denied_authorizer__"):
            # Permit the login URLs always.
            if request.path in LOGIN_URLS:
                return None

            raise PermissionDenied()

        # __denied_authorizer__ is set by the various decorators.
        if not view_func.__denied_authorizer__(request, **view_kwargs):  # type: ignore
            raise PermissionDenied()

        return None
