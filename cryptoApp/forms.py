from django import forms
from .models import CustomUser, Coin, Currency, Article
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
class SignUpForm(UserCreationForm):
    name = forms.CharField(max_length=255, label='Name')
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'id_or_photo']

    password1 = forms.CharField(
        label='Password',
        strip=False,
        widget=forms.PasswordInput,
        error_messages={},
    )

    username = forms.CharField(
        max_length=150,
        error_messages={
            'unique': "A user with that username already exists.",
            'invalid': "Enter a valid username. This value may contain only letters, numbers, and @/./+/-/_ characters.",
            'required': "This field is required.",
        },
    )
    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.first_name = self.cleaned_data['name']
        if commit:
            user.save()
        return user

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['password2'].widget = forms.HiddenInput()
        self.fields.pop('password2', None)

class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'password')


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content']


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
