from django.shortcuts import render
from django.contrib.auth import authenticate, login

from .forms import AuthenticationForm

# Create your views here.
def check_email_and_password(request):
    if request.method == 'POST':
        form = AuthenticationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                return render(request, 'templates/flatpages/success_authentifications.html', {'email': email, 'password': password})
            else:
                form.add_error(None, 'Неверная электронная почта или пароль')
        else:
            form = AuthenticationForm()
        return render(request, 'templates/flatpages/error_authentifications.html', {'form': form})





