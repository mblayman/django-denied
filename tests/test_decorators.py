from django.http import HttpResponse
from django.urls import include

from denied.decorators import allow, authorize
from denied.middleware import DeniedMiddleware


def false_authorizer(request, **view_kwargs):
    return False


def true_authorizer(request, **view_kwargs):
    return True


def data_authorizer(request, **view_kwargs):
    return view_kwargs.get("id") == 42


class TestAllowDecorator:
    def test_allow(self, authenticated_request):
        """An allowed view permits access."""

        @allow
        def allowed_view(request):
            return HttpResponse()  # pragma: no cover

        middleware = DeniedMiddleware(allowed_view)

        ret = middleware.process_view(authenticated_request, allowed_view, [], {})

        # The contract of the middleware is that None permits the middleware
        # chain to continue.
        assert ret is None

    def test_allow_unauthenticated(self, unauthenticated_request):
        """An allowed view does not need authentication."""

        @allow
        def allowed_view(request):
            return HttpResponse()  # pragma: no cover

        middleware = DeniedMiddleware(allowed_view)

        ret = middleware.process_view(unauthenticated_request, allowed_view, [], {})

        # The contract of the middleware is that None permits the middleware
        # chain to continue.
        assert ret is None

    def test_allow_include(self):
        """All included views are exempt.

        This test has the side effect of modifying the test views,
        but they are only used for this test.
        """
        from tests import nested_urls, urls

        urlconf_module, _, _ = allow(include("tests.urls"))

        assert urlconf_module == urls
        assert urls.a_root_view.__denied_exempt__  # type: ignore
        assert nested_urls.a_nested_view.__denied_exempt__  # type: ignore


class TestAuthorizeDecorator:
    def test_unauthorized(self, authenticated_request):
        """An unauthorized request is forbidden."""

        @authorize(false_authorizer)
        def allowed_view(request):
            return HttpResponse()  # pragma: no cover

        middleware = DeniedMiddleware(allowed_view)

        response = middleware.process_view(authenticated_request, allowed_view, [], {})

        assert response.status_code == 403

    def test_authorized(self, authenticated_request):
        """An authorized request is permitted."""

        @authorize(true_authorizer)
        def allowed_view(request):
            return HttpResponse()  # pragma: no cover

        middleware = DeniedMiddleware(allowed_view)

        ret = middleware.process_view(authenticated_request, allowed_view, [], {})

        # The contract of the middleware is that None permits the middleware
        # chain to continue.
        assert ret is None

    def test_authorized_against_data(self, authenticated_request):
        """A request is authorized against data."""

        @authorize(data_authorizer)
        def allowed_view(request):
            return HttpResponse()  # pragma: no cover

        middleware = DeniedMiddleware(allowed_view)

        ret = middleware.process_view(
            authenticated_request, allowed_view, [], {"id": 42}
        )

        # The contract of the middleware is that None permits the middleware
        # chain to continue.
        assert ret is None
