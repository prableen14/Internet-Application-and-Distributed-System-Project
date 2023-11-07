from django import forms
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
class SignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'id_or_photo']

class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'password')