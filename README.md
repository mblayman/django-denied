# django-denied

> None shall pass.
>
> The Black Knight

django-denied is an authorization system
for the Django web framework.
With django-denied,
every Django view *must be explicitly allowed*.
This design choice means
that developers have to make a design decision
about authorization
for a view to work.

In other words,
django-denied makes authorization controls a requirement
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

* TODO: document api
