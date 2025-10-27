from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.core.exceptions import ValidationError

from .models import Product
from .models import Buyer

# Create your models here.
class Reviews(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    buyer_id = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    assessment = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment =models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        """Простой метод проверяющий комментарий на наличие ненормативной лексики"""
        if self.comment:
            bad_words = ['хуйня', 'пизда', 'ебал', 'ебать', 'блядь', 'нахуя', 'бля',
                'сука', 'мудак', 'гондон', 'пидор', 'хуесос']

            comment_lower = self.comment.lower()

            for bad in bad_words:
                if bad in comment_lower:
                    raise ValidationError('Ненормативная лексика недопустима!')


    def __str__(self):
        return f'{self.comment}'

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

