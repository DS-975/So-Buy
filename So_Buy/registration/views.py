from django.shortcuts import render
from django.contrib.auth import authenticate, login

from .forms import AuthenticationForm

# Create your views here.
def check_email_and_password(request):
    # Обработка POST-запроса - когда пользователь отправил форму
    if request.method == 'POST':
        # Создание пустой формы для отображения
        form = AuthenticationForm(request.POST)
        # Проверяем валидность формы
        if form.is_valid():
            # Извлекаем очищенные данные из формы
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # Аутентифицируем пользователя по email
            # ПЕРЕДАЕМ email как username, потому что стандартный authenticate работает с username
            user = authenticate(request, username=email, password=password)

            # Проверяем, что пользователь найден и пароль верный
            if user is not None:
                # Логиним пользователя (Создаём сессию)
                login(request, user)
                # Перенаправляем пользователя на станицу с текстом успешной аутентификации
                return render(request, 'flatpages/success_authentifications.html', {'email': email, 'password': password})
            else:
                # Если аутентификация не удалась, вызываем ошибку
                form.add_error(None, 'Неверная электронная почта или пароль')

        return render(request, 'flatpages/error_authentifications.html', {'form': form})


    else:
        # Если форма невалидна (например, некорректный email)
        # Показываем ту же форму с сообщениями об ошибках валидации
        form = AuthenticationForm()
        return render(request, 'flatpages/error_authentifications.html', {'form': form})



