from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from .managers import CustomUserManager


class CustomUser(AbstractUser):
    email = models.EmailField("email address", unique=True)
    reset_token = models.CharField(max_length=255, null=True, blank=True)
    reset_token_expires = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    @classmethod
    def get_user_by_uidb64(cls, uidb64):
        user_id_bytes = urlsafe_base64_decode(uidb64)
        user_id = user_id_bytes.decode()
        return cls.objects.get(pk=user_id)

    def get_uid(self):
        return urlsafe_base64_encode(force_bytes(self.pk))
