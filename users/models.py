from users.utils import generate_invite_code, generate_confirmation_code
from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from users.managers import CustomUserManager

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):

    username = None
    name = models.CharField(max_length=32, **NULLABLE, verbose_name='имя')
    phone_number = PhoneNumberField(unique=True)
    avatar = models.ImageField(upload_to='users/', **NULLABLE, verbose_name='аватар')
    is_active = models.BooleanField(default=True, verbose_name='активен')
    confirmation_code = models.CharField(max_length=4, verbose_name='код подтверждения')
    invite_code = models.CharField(max_length=6, unique=True, verbose_name='инвайт-код')
    referrer = models.CharField(max_length=6, **NULLABLE, verbose_name='пригласивший пользователь')

    objects = CustomUserManager()

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.phone_number}'

    def save(self, *args, **kwargs):
        self.verification_code = generate_confirmation_code()
        self.invite_code = generate_invite_code()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

