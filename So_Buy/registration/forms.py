from enum import unique

from django import forms

class AuthenticationForm(forms.Form):
    email = forms.EmailField(label='Электронная почта') # Поле email, для пользователя поле будет отображаться как Электронная почта
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль') # Поле password, для пользователя поле будет отображаться как Пароль


