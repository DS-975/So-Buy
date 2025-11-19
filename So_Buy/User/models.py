from encodings.punycode import digits
from django.contrib.auth.models import AbstractUser

from django.core.validators import MinLengthValidator, MinValueValidator, MaxLengthValidator
from django.db import models
from django.core.exceptions import ValidationError


# Create your models here.
class CustomUser(AbstractUser):


    name = models.CharField(max_length=20, null=True)
    surname = models.CharField(max_length=20, null=True)
    password = models.CharField(max_length=128, validators=[MinLengthValidator(8), MaxLengthValidator(128)])
    email = models.EmailField(unique=True, verbose_name="email", blank=False)
    phone = models.CharField(max_length=12, unique=True, verbose_name='phone', blank=False)
    balance = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)], default=0.00)


    def check_password(self):
        if len(self.password) < 8:
            raise ValidationError('Длина пароля не должна быть меньше 8 символов')
        if len(self.password) > 128:
            raise ValidationError('Длина пароля не должна быть больше 128 символов')

    def check_phone(self):
        if len(self.phone) != 12:
            raise ValidationError('Номер должен состоять из 12 символов')
        if not self.phone.startswith('+'):
            raise ValidationError('Номер должен начинаться с +')
        if not self.phone[1:].isdigit():
            raise ValidationError('Номер должен состоять из цифр после знака +')



    def save(self, *args, **kwargs):
        self.check_password()
        self.check_phone()
        super().save(*args, **kwargs)


    def __str__(self):
        return f'Имя : {self.name.title()}, Фамилия : {self.surname.title()}'





