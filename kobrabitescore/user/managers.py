from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)

        if 'username' not in extra_fields or not extra_fields['username']:
            raise ValueError(_("The Username must be set"))

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user
