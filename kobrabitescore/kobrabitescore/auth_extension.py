from django.conf import settings
from rest_framework.authentication import SessionAuthentication
from drf_spectacular.authentication import SessionScheme


class CustomSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        """
        Enforce CSRF validation for session based authentication.
        """
        if settings.DISABLE_CSRF:
            return False
        return super().enforce_csrf(request)


class CustomSessionScheme(SessionScheme):
    target_class = 'kobrabitescore.auth_extension.CustomSessionAuthentication'
    name = 'cookieAuth'
    priority = -1
