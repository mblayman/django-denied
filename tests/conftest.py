import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser

User = get_user_model()


@pytest.fixture
def user():
    """Make a user."""
    return User()


@pytest.fixture
def authenticated_request(user, rf):
    """Make a request with an authenticated user."""
    request = rf.get("/")
    request.user = user
    return request


@pytest.fixture
def unauthenticated_request(user, rf):
    """Make a request with an unauthenticated user."""
    request = rf.get("/")
    request.user = AnonymousUser()
    return request
