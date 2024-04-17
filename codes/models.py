import random
import string
from django.db import models
from users.models import User


class Code(models.Model):

    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    verify_code = models.CharField(verbose_name='Код подтверждения', max_length=4)
    invite_code = models.CharField(verbose_name='Инвайт-код', max_length=6, blank=True, null=True)

    def __str__(self):
        return str(self.verify)

    def save(self, *args, **kwargs):
        self.verify_code = ''.join(random.choices(string.digits, k=4))
        super().save(*args, **kwargs)
