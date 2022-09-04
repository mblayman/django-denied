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

If you set `LOGIN_URL`,
django-denied expects the path form
of the setting
(e.g., `/accounts/login/`)
rather than the `url` name
(e.g., `accounts:login`).

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
# project/urls.py
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

With django-denied,
a Django view is authorized with the `authorize` decorator
and an *authorizer* function.
An authorizer has a function signature of

```python
from django.http import HttpRequest


def example_authorizer(request: HttpRequest, **view_kwargs: dict) -> bool:
    ...
```

The authorizer evaluates the incoming request and view information
and should return `True` if the request is authorized
or `False` is the request is not authorized.
The `view_kwargs` include any data that was parsed out of the URL route.

The authorizer acts as a declarative way
of showing what is authorized
for the view.

```python
from denied.decorators import authorize

from .authorizers import example_authorizer


@authorize(example_authorizer)
def example_view(request):
    ...
```

To use `authorize` on a class-based view,
you must attach the decorator to the `dispatch` method.

```python
from denied.decorators import authorize
from django.utils.decorators import method_decorator
from django.views.generic import DetailView

from .authorizers import example_authorizer
from .models import Example


@method_decorator(authorize(example_authorizer), "dispatch")
class ExampleDetail(DetailView):
    queryset = Example.objects.all()
```
### Built-in authorizers

The library includes built-in authorizers
for common cases.

#### `denied.authorizers.any_authorized`

This authorizer always evaluates to `True` and is the logical equivalent
to `login_required` since django-denied always enforces authentication checking.

#### `denied.authorizers.staff_authorized`

This authorizer only permits access when `user.is_staff == True`.
`staff_authorized` is equivalent to `staff_member_required`
from the Django `admin` app.

#### Authorizer example

This section shows a more complete example
of an authorizer
to give you a sense
of how django-denied works in practice.

For our example,
we'll consider a project tracking application.
This is little more than a TODO list
that groups the tasks into projects.

Here are the models.

```python
# application/models.py
from django.contrib.auth.models import User
from django.db import models


class Project(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)


class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    description = models.TextField()
    completed = models.BooleanField(default=False)
```

For this simple system,
only project owners can do anything
with a task.
Let's create the authorizer for that.

```python
# application/authorizers.py


def task_authorized(request, **view_kwargs):
    return Task.objects.filter(
        project__owner=request.user,
        pk=view_kwargs["pk"],
    ).exists()
```

These are the URLs we want to support
with this authorizer.

```python
# application/urls.py

from django.urls import path

from .views import task_detail, task_edit

urlpatterns = [
    path("tasks/<int:pk>/", task_detail, name="task_detail"),
    path("tasks/<int:pk>/edit/", task_detail, name="task_edit"),
]
```

Now we can set our views
and set their authorization.

```python
# application/views.py
from denied.decorators import authorize
from django.shortcuts import render

from .authorizers import task_authorized
from .models import Task


@authorize(task_authorized)
def task_detail(request, pk):
    task = Task.objects.get(pk=pk)
    return render(request, "task_detail.html", {"task": task})


@authorize(task_authorized)
def task_edit(request, pk):
    task = Task.objects.get(pk=pk)
    return render(request, "task_edit.html", {"task": task})
```

Since the authorizer handles the access control,
we can be confident that the task is safe to fetch
by its key alone.
Access control is pushed to the boundary of the view
so that the view's internal logic is about as simple
as you can make it.
