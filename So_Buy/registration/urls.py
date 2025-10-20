from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.check_email_and_password, name='login')
]