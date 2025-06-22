from .models import User
from django.utils import timezone
import six
from django.contrib.auth.tokens import PasswordResetTokenGenerator

class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user:User, timestamp):
        login_time = timezone.datetime.timestamp(user.date_joined)
        return six.text_type(user.pk) + six.text_type(timestamp) + six.text_type(user.is_active) + six.text_type(login_time)

