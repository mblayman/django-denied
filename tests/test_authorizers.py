from __future__ import annotations

from denied.authorizers import any_authorized, staff_authorized


class TestAnyAuthorized:
    def test_authorized(self, rf):
        """Any authorized use is permitted."""
        request = rf.get("/")

        assert any_authorized(request)


class TestStaffAuthorized:
    def test_non_staff(self, authenticated_request):
        """Non-staff access is not permitted."""
        assert not staff_authorized(authenticated_request)

    def test_staff(self, rf, user):
        """Staff access is permitted."""
        request = rf.get("/")
        user.is_staff = True
        request.user = user

        assert staff_authorized(request)
