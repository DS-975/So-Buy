from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.db import models
from .models import Product, Sellers
from decimal import Decimal


# Create your models here.
class Warehouse(models.Model):
    product = models.ForeignKey(Product, related_name='product', on_delete=models.CASCADE)
    seller = models.ForeignKey(Sellers, related_name='seller', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=0, validators=[MinValueValidator(Decimal('0'))])
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Складской остаток'
        verbose_name_plural = 'Складские остатки'
        unique_together = ['product', 'seller']

    def clean(self):
        if self.product.amount == 0:
            raise ValidationError('Товара не осталось на складе.')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.product} - {self.amount} шт.'