from django.core.exceptions import PermissionDenied
from django.http import HttpResponseBadRequest


def company_required(function):
    def wrap(request, *args, **kwargs):
        if request.user.is_organisation():
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


def normal_user_required(function):
    def wrap(request, *args, **kwargs):
        if request.user.is_individual():
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


def ajax_required(f):
    def wrap(request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseBadRequest()
        return f(request, *args, **kwargs)

    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap


