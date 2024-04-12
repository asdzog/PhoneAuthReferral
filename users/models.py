import random
import string
from datetime import timedelta, timezone

from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ObjectDoesNotExist
from django.db import models


from django.db.models.signals import post_save
from django.dispatch import receiver

NULLABLE = {'blank': True, 'null': True}


class UserManager(BaseUserManager):

    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError('The phone number is required')
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def superuser(self, phone_number, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self.create(phone_number, password, **extra_fields)

    def generate_confirmation_code(self):
        # Генерируем случайный код подтверждения
        return ''.join([str(random.randint(0, 9)) for _ in range(4)])

    def create_user_with_confirmation_code(self, phone_number):
        """
        Создает пользователя и генерирует код подтверждения.
        """
        if not phone_number:
            raise ValueError('The Phone Number must be set')

        # Генерируем случайный код подтверждения
        confirmation_code = ''.join([str(random.randint(0, 9)) for _ in range(4)])

        # Создаем пользователя с кодом подтверждения
        user = self.model(phone_number=phone_number, confirmation_code=confirmation_code)
        user.set_unusable_password()
        user.save(using=self._db)
        print(user.confirmation_code)

        return user

    def check_confirmation_code_and_login(self, phone_number, entered_code):
        try:
            user = self.get(phone_number=phone_number)
        except self.model.DoesNotExist:
            # Если пользователь не найден, создаем нового
            user = self.create_user_with_confirmation_code(phone_number)
            # В этом случае, код подтверждения уже установлен при создании пользователя

        if user.confirmation_code and user.confirmation_code == entered_code:
            # Проверяем срок действия кода подтверждения
            if user.created_at + timedelta(minutes=15) >= timezone.now():
                return user, None
            else:
                return None, "Время действия кода подтверждения истекло."
        else:
            return None, "Неверный код подтверждения."


class User(AbstractUser):

    username = None

    name = models.CharField(max_length=32, **NULLABLE, verbose_name='имя')
    phone_number = models.CharField(max_length=20, unique=True, verbose_name='телефон')
    avatar = models.ImageField(upload_to='users/', **NULLABLE, verbose_name='аватар')
    is_active = models.BooleanField(default=True, verbose_name='активен')
    confirmation_code = models.CharField(max_length=4, blank=True, null=True)
    invite_code = models.CharField(max_length=6, unique=True, verbose_name='инвайт-код')
    invited_users = models.ManyToManyField(
        'self', blank=True, symmetrical=False, verbose_name='рефералы'
    )

    objects = UserManager()

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.phone_number}'

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'


@receiver(post_save, sender=User)
def generate_invite_code(sender, instance, created, **kwargs):
    if created and not instance.invite_code:
        while True:
            invite_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            if not User.objects.filter(invite_code=invite_code).exists():
                instance.invite_code = invite_code
                instance.save()
                break
