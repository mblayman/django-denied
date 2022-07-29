# django-denied

> None shall pass.
>
> The Black Knight

django-denied is an authorization system
for the Django web framework.
With django-denied,
every Django view *must be explicitly allowed*.
This design means
that developers have to make a choice
about authorization
for a view to work.

In other words,
django-denied makes authorization a requirement
for every view in a Django project.

## Who should use this?

This package is well suited for Django projects
that need to protect pages against unauthorized access normally.
If you are making a service
that requires user's to login
and restricts which data a user sees,
then django-denied may be a good fit for you.

If your web application is meant to be open
for a large audience,
especially with lots of anonymous users,
then this package may be overkill for your needs.
A blog or content management system may not be a good candidate.

## Install

Get the package.

```
pip install django-denied
```

django-denied uses Django's built-in `auth` and `admin` apps.
These apps also depend on the `contenttypes` app.
Ensure that these apps are in your `INSTALL_APPS`
in your Django settings file.

```python
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    ...,
]
```

Add the `DeniedMiddleware`.
This middleware does all the authorization checking.
The middleware depends on the `request.user`,
so be sure to include it *after* the `AuthenticationMiddleware`.

```python
MIDDLEWARE = [
    ...,
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "denied.middleware.DeniedMiddleware",
    ...,
]
```

Now you're ready to start.

## Usage

django-denied has two primary modes
for handling views.

1. `allow`
2. `authorize`

These decorators are the main interface
of the package
and are described in the sections below.

By default,
django-denied assumes that all users should be authenticated,
with the exception of allowed views or login pages.

The login pages are

* The page defined by `settings.LOGIN_URL` and
* The Django admin login defined at the `admin:login` route.

### Allowing views

Every app is likely to have views
that should be made accessible to unauthenticated users.
A company's about page, terms of service, and privacy policy are all good examples.

The `allow` decorator is for marking a Django view as exempt
from the authorization checking done
by the `DeniedMiddleware`.

This is an example of how you might create a terms of service view.

```python
# application/views.py
from denied.decorators import allow
from django.shortcuts import render


@allow
def terms_of_service(request):
    return render(request, "tos.html", {})
```

The `allow` decorator has a secondary function.
Aside from allowing a single view,
the decorator can allow a set of views
that you would use with `django.urls.path`.

This is necessary to permit third party apps
that have other views,
but are unaware of the django-denied system.

This is an example of using `allow`
to permit the Django admin views
as well as the popular app,
[django-allauth](https://django-allauth.readthedocs.io/en/latest/).

```python
from denied.decorators import allow
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("accounts/", allow(include("allauth.urls"))),
    path("admin/", allow(admin.site.urls)),
]
```

Note:
Even if you include `allow` on a view or a set of views,
that does not mean that what you've allowed will suddenly
bypass any existing authentication or authorization checking.
***This is a feature, not a bug!***

`login_required`, `permission_required`,
and any other authentication or authorization checking
that pre-exist on views will remain.
*django-denied does not disable the security features
of other third party libraries.*

## Authorizing views

* TODO: document api
