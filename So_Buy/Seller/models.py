from django.core.validators import MinLengthValidator
from django.db import models
from User.models import Users
from django.core.exceptions import ValidationError

# Create your models here.
class Sellers(models.Model):
    user_id = models.OneToOneField(Users,on_delete=models.CASCADE, related_name='seller_profile')

    shop_name = models.CharField(
        max_length=50,
        verbose_name='Название магазина',
        help_text='Введите название вашего магазина',
        validators=[MinLengthValidator(2, 'Название должно состоять минимум из 2 символов ')]
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание магазина',
        help_text='Расскажите о вашем магазине'
    )

    logo = models.ImageField(
        verbose_name='Логотип магазина',
        help_text='Загрузите логотип вашего магазина'
    )
    website = models.URLField(
        blank=True,
        verbose_name = 'Веб-сайт',
        help_text = 'Ссылка на сайт'
    )

    active_since = models.DateField(
        auto_now_add=True,
        verbose_name='Магазин открыт с'
    )

    store_opening_time = models.TimeField(blank=True, null=True, verbose_name='Время открытия магазина')
    store_closing_time = models.TimeField(blank=True, verbose_name='Время закрытия магазина')

    class WorkingDay(models.TextChoices):
        WEEKDAY = 'Будни', 'Пн, Вт, Ср, Чт, Пт'
        WEEKEND = 'Выходные', 'Сб, Вс'
        DAILY = 'Ежедневно', 'Пн, Вт, Ср, Чт, Пт, Сб, Вс'

    store_working_days = models.CharField(blank=True, max_length=20, choices=WorkingDay.choices, default=WorkingDay.DAILY, verbose_name='Дни работы магазина')


    def check_logo(self):
        """Проверка наличия логотипа"""
        if self.logo is None:
            raise ValidationError('Установите логотип')

    def check_for_store_opening_hours(self):
        """Проверка корректности времени работы"""
        if self.store_opening_time is None:
            raise ValidationError('Установите время открытия магазина')
        if self.store_closing_time is None:
            raise ValidationError('Установите время закрытия магазина')
        if self.store_opening_time >= self.store_closing_time:
            raise ValidationError('Время открытия не может быть позже времени закрытия')


    def __str__(self):
        """Строковое представление объекта - название магазина"""
        return self.shop_name

    def save(self, *args, **kwargs):
        """Переопределение save с валидацией перед сохранением"""
        try:
            self.full_clean()
            self.check_logo()
            self.check_for_store_opening_hours()
        except ValidationError as V:
            raise V
        super().save(*args, **kwargs)



