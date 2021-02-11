from functools import wraps

from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.core.exceptions import ImproperlyConfigured, PermissionDenied
from django.shortcuts import resolve_url, redirect


def user_passes_test(test_func, redirect_url=None):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if test_func(request.user):
                return view_func(request, *args, **kwargs)
            path = request.build_absolute_uri()
            resolved_redirect_url = resolve_url(redirect_url or settings.PERMISSION_REDIRECT_URL)

            return redirect(resolved_redirect_url)
        return _wrapped_view
    return decorator


def admin_required(function=None, redirect_url=None):
    actual_decorator = user_passes_test(
        lambda u: u.user_type == 'AD',
        redirect_url=redirect_url
    )

    if function:
        return actual_decorator(function)
    return actual_decorator


def system_admin_required(function=None, redirect_url=None):
    actual_decorator = user_passes_test(
        lambda u: u.user_type == 'SAD',
        redirect_url=redirect_url
    )

    if function:
        return actual_decorator(function)
    return actual_decorator


def school_head_required(function=None, redirect_url=None):
    actual_decorator = user_passes_test(
        lambda u: u.user_type == 'SH',
        redirect_url=redirect_url
    )

    if function:
        return actual_decorator(function)
    return actual_decorator


def school_admin_required(function=None, redirect_url=None):
    actual_decorator = user_passes_test(
        lambda u: u.user_type == 'SH' or u.user_type == 'SAD',
        redirect_url=redirect_url
    )

    if function:
        return actual_decorator(function)
    return actual_decorator


def pupil_required(function=None, redirect_url=None):
    actual_decorator = user_passes_test(
        lambda u: u.user_type == 'PU',
        redirect_url=redirect_url
    )

    if function:
        return actual_decorator(function)
    return actual_decorator


def teacher_required(function=None, redirect_url=None):
    actual_decorator = user_passes_test(
        lambda u: u.user_type == 'TU' or u.user_type == 'CT',
        redirect_url=redirect_url
    )

    if function:
        return actual_decorator(function)
    return actual_decorator


def class_teacher_required(function=None, redirect_url=None):
    actual_decorator = user_passes_test(
        lambda u: u.user_type == 'CT',
        redirect_url=redirect_url
    )

    if function:
        return actual_decorator(function)
    return actual_decorator


def finance_required(function=None, redirect_url=None):
    actual_decorator = user_passes_test(
        lambda u: u.user_type == 'FO',
        redirect_url=redirect_url
    )

    if function:
        return actual_decorator(function)
    return actual_decorator

