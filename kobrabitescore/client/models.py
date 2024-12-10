from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class SoftDeleteModel(models.Model):
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        self.deleted_at = timezone.now()
        self.save(update_fields=['deleted_at'])


class PersonFields(models.Model):
    first_name = models.CharField(max_length=150, null=False, blank=False)
    last_name = models.CharField(max_length=150, null=False, blank=False)
    birthdate = models.DateField(auto_now=False, null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    pronouns = models.CharField(max_length=32, blank=True, null=True)
    gender = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        abstract = True


class Client(PersonFields, SoftDeleteModel):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="clients")
    email_opt_in = models.BooleanField(default=False)
    phone_opt_in = models.BooleanField(default=False)
    client_since = models.DateField(null=True, blank=True)
    profile_image = models.CharField(max_length=128, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_active = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Client<{self.first_name} {self.last_name} ({self.id})>"

    def get_name(self):
        try:
            full_name = "%s %s" % (self.first_name, self.last_name)
            return full_name.strip()
        except AttributeError:
            return None
