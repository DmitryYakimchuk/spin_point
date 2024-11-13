"""Here is the functions for common use"""

from django.conf import settings
from django.contrib.auth.decorators import user_passes_test


def logout_required(function=None, logout_url=settings.LOGOUT_REDIRECT_URL):
    """
    Similar decorator for @logout_required,
    such that the view is only rendered if the user is not authenticated,
    otherwise redirected to settings.LOGOUT_REDIRECT_URL
    """

    actual_decorator = user_passes_test(
        lambda u: not u.is_authenticated,
        login_url=logout_url
    )
    if function:
        return actual_decorator(function)
    return actual_decorator
