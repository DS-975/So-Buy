from django.urls import path
from . import views

urlpatterns = [
    path('success_authentification/', views.check_email_and_password, name='check_email_and_password')
]