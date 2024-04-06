from __future__ import annotations

import pytest
from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.test import RequestFactory

from denied.authorizers import any_authorized
from denied.decorators import authorize
from denied.middleware import DeniedMiddleware


def get_response(request):
    return HttpResponse()


def false_authorizer(request, **view_kwargs):
    return False


def true_authorizer(request, **view_kwargs):
    return True


class TestDeniedMiddleware:
    rf = RequestFactory()

    def test_unbroken_chain(self):
        """The middleware continues the chain."""
        request = self.rf.get("/")
        middleware = DeniedMiddleware(get_response)

        response = middleware(request)

        assert response.status_code == 200

    def test_authentication_required(self):
        """Authentication is required by default."""
        request = self.rf.get("/")
        request.user = AnonymousUser()
        middleware = DeniedMiddleware(get_response)

        response = middleware.process_view(request, get_response, [], {})

        assert response
        assert response.status_code == 302
        assert "login" in response["Location"]

    def test_authentication_not_required_for_login(self, settings):
        """A login URL is exempt from the authentication checking."""

        @authorize(any_authorized)
        def allowed_view(request):
            return HttpResponse()  # pragma: no cover

        request = self.rf.get(settings.LOGIN_URL)
        request.user = AnonymousUser()
        middleware = DeniedMiddleware(allowed_view)

        ret = middleware.process_view(request, allowed_view, [], {})

        # The contract of the middleware is that None permits the middleware
        # chain to continue.
        assert ret is None

    def test_login_allowed(self, settings):
        """The login page does not need to be allowed explicitly."""

        request = self.rf.get(settings.LOGIN_URL)
        request.user = AnonymousUser()
        middleware = DeniedMiddleware(get_response)

        ret = middleware.process_view(request, get_response, [], {})

        # The contract of the middleware is that None permits the middleware
        # chain to continue.
        assert ret is None

    def test_authentication_exempt(self):
        """A view is exempt from authentication checking."""

        def authorized_view(request):
            return HttpResponse()  # pragma: no cover

        authorized_view.__denied_exempt__ = True  # type: ignore
        request = self.rf.get("/")
        request.user = AnonymousUser()
        middleware = DeniedMiddleware(authorized_view)

        ret = middleware.process_view(request, authorized_view, [], {})

        # The contract of the middleware is that None permits the middleware
        # chain to continue.
        assert ret is None

    def test_default_forbidden(self, authenticated_request):
        """A view is denied by default."""
        middleware = DeniedMiddleware(get_response)

        with pytest.raises(PermissionDenied):
            middleware.process_view(authenticated_request, get_response, [], {})

    def test_authorized(self, authenticated_request):
        """An authorizer permits access."""

        def authorized_view(request):
            return HttpResponse()  # pragma: no cover

        authorized_view.__denied_authorizer__ = true_authorizer  # type: ignore
        middleware = DeniedMiddleware(authorized_view)

        ret = middleware.process_view(authenticated_request, authorized_view, [], {})

        # The contract of the middleware is that None permits the middleware
        # chain to continue.
        assert ret is None

    def test_not_authorized(self, authenticated_request):
        """An authorizer rejects an unauthorized attempt."""

        def denied_view(request):
            return HttpResponse()  # pragma: no cover

        denied_view.__denied_authorizer__ = false_authorizer  # type: ignore
        middleware = DeniedMiddleware(denied_view)

        with pytest.raises(PermissionDenied):
            middleware.process_view(authenticated_request, denied_view, [], {})

    def test_media_allowed(self, settings):
        """All media is allowed when a MEDIA_URL is present."""
        settings.MEDIA_URL = "/media/"
        request = self.rf.get("/media/some-user-file.jpg")
        request.user = AnonymousUser()
        middleware = DeniedMiddleware(get_response)

        ret = middleware.process_view(request, get_response, [], {})

        # The contract of the middleware is that None permits the middleware
        # chain to continue.
        assert ret is None

    def test_media_disallowed(self, settings):
        """Media URLs are handled like all other routes when MEDIA_URL is not set."""
        settings.MEDIA_URL = ""
        request = self.rf.get("/media/some-user-file.jpg")
        request.user = AnonymousUser()
        middleware = DeniedMiddleware(get_response)

        ret = middleware.process_view(request, get_response, [], {})

        # The contract of the middleware is that None permits the middleware
        # chain to continue.
        assert ret is None
