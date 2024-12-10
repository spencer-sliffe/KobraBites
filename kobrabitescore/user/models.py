from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField("email address", unique=True)
    reset_token = models.CharField(max_length=255, null=True, blank=True)
    reset_token_expires = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    @classmethod
    def get_user_by_uidb64(cls, uidb64):
        # Decode the user's ID from base64
        user_id_bytes = urlsafe_base64_decode(uidb64)
        # Decode the user's ID from bytes to string
        user_id = user_id_bytes.decode()
        # Get the user by ID
        user = CustomUser.objects.get(pk=user_id)
        return user

    def get_uid(self):
        # Get the user's ID as bytes
        user_id_bytes = force_bytes(self.pk)
        # Encode the user's ID as base64
        return urlsafe_base64_encode(user_id_bytes)
