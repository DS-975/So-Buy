from importlib.metadata import requires

from django import forms
from django.contrib.auth.forms import UserCreationForm
from User.models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length = 30, label = 'Имя', required = True, widget=forms.TextInput(attrs={'placeholder': 'Ваше имя'}))
    last_name = forms.CharField(max_length = 30, label = 'Фамилия', required = True, widget=forms.TextInput(attrs={'placeholder': 'Ваша фамилия'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Ваш email'}))
    phone = forms.CharField(max_length=12, required=True, label='Телефон', widget=forms.TextInput(attrs={'placeholder': 'Номер телефона'}))
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'phone')

    def save(self, commit = True):
        user = super().save(commit = False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.username = user.email
        if commit:
            user.save()
        return user

class EmailAuthenticationForm(forms.Form):
    email = forms.EmailField(label = 'Email', widget=forms.EmailInput(attrs={'placeholder': 'Ваш email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Ваш пароль'}))
