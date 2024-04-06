# CHANGELOG

## 1.3

* Allow media routes when using the file system storage (i.e., MEDIA_URL and MEDIA_ROOT)
* Drop support for Python 3.7
* Add support for Python 3.11
* Add support for Python 3.12

## 1.2

* Use `PermissionDenied` in the middleware
  instead of `HttpResponseForbidden`.
  This lets Django use the `permission_denied` handler
  if users have defined a custom 403 error page.

## 1.1

* The login URLs do not need to be explicitly allowed.

## 1.0

* Validated the package against a production site.
  Declaring 1.0 to show API stability.

## 0.2

* Inclusion of all the features ported from the homeschool app
  where this library came from originally.

## 0.1

* Initial release with skeleton of application
