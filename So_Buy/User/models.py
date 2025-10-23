from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.db import models

from decimal import Decimal


# Create your models here.
class Users(AbstractUser):
    """
        Кастомная модель пользователя, расширяющая стандартную AbstractUser
        Добавлены поля для ролевой системы, баланса и телефона
        """

    # Переопределение полей groups и user_permissions для избежания конфликтов
    # со стандартной моделью User из django.contrib.auth
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='custom_users_groups', # Уникальное имя для обратной связи
        related_query_name='custom_user', # Уникальное имя для запросов
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='custom_users_permissions', # Уникальное имя для обратной связи
        related_query_name='custom_user' # Уникальное имя для запросов
    )

    email = models.EmailField(max_length=128, unique=True)

    class Role(models.TextChoices):
        """Возможные роли пользователя в системе"""
        BUYER = 'Buyer', 'Покупатель'
        SELLER = 'Seller', 'Продавец'

    role = models.CharField(
        max_length=6,
        choices=Role.choices,
        default=Role.BUYER,
    )

    balance = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(0)])


    phone = models.CharField(
        max_length=11,
        unique=True,
    )


    def error_password(self):
        """ Валидация пароля на минимальную длину """
        if len(self.password) < 8:
            return 'Длина пароля должна быть не меньше 8 символов'
        return None

    def checking_the_correctness_of_the_phone_number(self):
        """
                Валидация номера телефона

                Проверяет:
                - Состоит ли номер только из цифр
                - Соответствует ли длина 11 символам
                - Начинается ли номер с '89' (российский формат)
        """
        if not self.phone.isdigit():
            raise ValidationError('Номер должен состоять исключительно из цифр')
        if len(self.phone) != 11:
            raise ValidationError('Номер должен состоять из 11 цифр')
        if not self.phone.startswith('89'):
            raise ValidationError('Номер должен начинаться с 89')

    def save(self, *args, **kwargs):
        """
                Переопределенный метод сохранения с автоматической валидацией

                Вызывает full_clean() перед сохранением для проверки всех валидаторов
                """
        self.full_clean()
        super().save(*args, **kwargs)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Строковое представление пользователя"""
        return f"{self.username}"

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'