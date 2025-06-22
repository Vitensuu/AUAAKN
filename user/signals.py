from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from wallet.models import Wallet
from .models import User
@receiver(post_save, sender=User)
def create_wallet_for_regular_user(sender, instance, created, **kwargs):
    if created and not instance.is_staff and not instance.is_superuser:
        Wallet.objects.get_or_create(user=instance)
