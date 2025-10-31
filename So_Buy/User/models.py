from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError


# Create your models here.
class CustomUser(AbstractUser):
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='customuser_set',  # Уникальное имя
        related_query_name='customuser',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='customuser_set',  # Уникальное имя
        related_query_name='customuser',
    )
    email = models.EmailField(unique=True, verbose_name="email", error_messages={"unique": "Пользователь с данной электронной почтой уже был зарегистрирован"}, blank=False)
    phone = models.CharField(max_length=12, unique=True, verbose_name='phone', blank=False)
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)

    def clean(self):
        super().clean()

        if self.phone:
            if not self.phone.startswith('+79') or len(self.phone) != 12:
                raise ValidationError({'phone': 'Ошибка, введите номер телефона в формате +79ХХХХХХХХХ'})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)



