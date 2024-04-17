import random
import string
from users.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=User)
def generate_invite_code(sender, instance, created, **kwargs):
    """ Invite-code generation after user creation """
    if created and not instance.invite_code:
        while True:
            invite_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            if not User.objects.filter(invite_code=invite_code).exists():
                instance.invite_code = invite_code
                instance.save()
                break
