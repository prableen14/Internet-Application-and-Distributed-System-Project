from django import forms
from .models import CustomUser, Coin, Currency
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
class SignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'id_or_photo']


class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'password')


class ConverterForm(forms.Form):
    amount = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-input',
                                                              'placeholder': 'Enter Amount to Convert'}))
    coin_type = forms.ModelChoiceField(queryset=Coin.objects.all(), empty_label=None,
                                       widget=forms.Select(attrs={'class': 'form-select'}))
    currency = forms.ModelChoiceField(queryset=Currency.objects.all(),
                                      initial='USD',
                                      widget=forms.Select(attrs={'class': 'form-select'}))

    is_coin_to_currency = forms.BooleanField(
        required=False,
        initial=True,  # Set the initial value to True or False
        widget=forms.HiddenInput(attrs={'class': 'form-toggle-input'}),  # Hidden input to store the state
    )
