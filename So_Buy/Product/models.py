from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from Seller.models import Sellers

# Create your models here.
class Product(models.Model):
    seller_id = models.ForeignKey(Sellers, related_name='seller', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name='Название товара')
    description = models.TextField(
        blank=True,
        verbose_name='Описание'
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    images = models.ImageField(upload_to='products/%Y/%m/%d/',verbose_name='Изображение')
    is_active = models.BooleanField(default=True)

    def check_name(self):
        if self.name is None:
            raise ValidationError('Введите название товара')
        if len(self.name) < 2:
            raise ValidationError('Название должно быть минимум из 2 символов')

    def check_price(self):
        if self.price is None:
            raise ValidationError('Установите цену товара')
        if self.price <= 0:
            raise ValidationError('Цена не должна быть меньше или равной нулю')

    def check_images(self):
        if self.images is None:
            raise ValidationError('Добавьте изображения товара')


    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name} - {self.price}'
