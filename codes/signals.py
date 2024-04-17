import random
import string
from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import User


@receiver(post_save, sender=User)
def generate_verify_code(sender, instance, created, *args, **kwargs):
    if created:
        verification_code = ''.join(random.choices(string.digits, k=4))
        instance.verification_code = verification_code
        instance.save()
