from django.utils import timezone
from datetime import timedelta
import uuid


# WILL USE LATER
def user_set_reset_token(user, days=1):
    user.reset_token = str(uuid.uuid4())
    user.reset_token_expires = timezone.now() + timedelta(days=days)
    user.save(update_fields=['reset_token', 'reset_token_expires'])
