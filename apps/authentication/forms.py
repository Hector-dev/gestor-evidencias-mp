from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm as DjangoUserCreationForm, UserChangeForm as DjangoUserChangeForm

class UserCreationForm(DjangoUserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'identification', 'position', 'department', 'phone', 'role', 'password1', 'password2')

class UserChangeForm(DjangoUserChangeForm):
    password = None  # No mostrar el campo de contraseña
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'identification', 'position', 'department', 'phone', 'role', 'is_active', 'is_staff') 