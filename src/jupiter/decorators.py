from django.core.exceptions import PermissionDenied
from functools import wraps

def allow(roles):
    def decorated(func):
        @wraps(func)
        def func_wrapper(request, *args, **kwargs):
            if request.user.is_authenticated:
                if request.user.role in roles:
                    return func(request, *args, **kwargs)
            raise PermissionDenied
        return func_wrapper
    return decorated