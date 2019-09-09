from django.core.exceptions import PermissionDenied
from .models import Client


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