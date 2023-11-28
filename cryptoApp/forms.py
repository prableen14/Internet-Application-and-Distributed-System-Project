from django import forms
from django.contrib.auth import get_user_model
from .models import CustomUser, Coin, Currency, Article
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from datetime import date
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
    email = forms.EmailField(
        max_length=255,
        error_messages={
            'invalid': "Enter a valid email address.",
            'required': "This field is required.",
        },
    )

    id_or_photo = forms.ImageField(
        required=True,
        error_messages={
            'required': "This field is required.",
        },
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        User = get_user_model()
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already in use. Please choose a different one.")
        return username

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


class CurrencyForm(forms.ModelForm):
    class Meta:
        model = Currency
        fields = ['code', 'name']


class CoinForm(forms.ModelForm):
    class Meta:
        model = Coin
        fields = ['name', 'symbol', 'price', 'percentage_change_1h', 'percentage_change_24h', 'percentage_change_7d', 'market_cap', 'all_time_high', 'graph_link', 'icon_url']


class TransactionForm(forms.Form):
    order_name = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    order_price = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    card_number = forms.CharField(
        label='Card Number',
        max_length=19, min_length=16,
        widget=forms.TextInput(attrs={'pattern': '^[0-9 ]{16,19}$', 'title': 'Card number must be 16 digits'})
    )
    cvv = forms.CharField(
        label='CVV',
        max_length=3,
        widget=forms.TextInput(attrs={'pattern': '[0-9]{3}', 'title': 'CVV must be a 3-digit number'})
    )

    expiry_date = forms.CharField(
        label='Expiry Date',
        required=True,
        widget=forms.TextInput(attrs={'type': 'month'})
    )

    cardholder_name = forms.CharField(
        label='Cardholder Name',
        max_length=250,
        widget=forms.TextInput(attrs={'pattern': '[A-Za-z ]+', 'title': 'Only alphabets and spaces allowed'})
    )

    def __init__(self, coin, *args, **kwargs):
        super(TransactionForm, self).__init__(*args, **kwargs)

        # Set initial values for the fields
        self.initial['order_name'] = coin.name
        self.initial['order_price'] = coin.price

    def clean_card_number(self):
        card_number = ''.join(char for char in self.cleaned_data['card_number'] if char.isdigit())
        if not card_number.isdigit() or len(card_number) != 16:
            raise forms.ValidationError('Invalid card number. It should be a 16-digit number.')
        return card_number

    def clean_cvv(self):
        cvv = self.cleaned_data['cvv']
        if not cvv.isdigit() or len(cvv) != 3:
            raise forms.ValidationError('Invalid CVV. It should be a 3-digit number.')
        return cvv

    def clean_expiry_date(self):
        expiry_date = self.cleaned_data.get('expiry_date')

        # Convert the input string to a date object
        try:
            expiry_date = date.fromisoformat(expiry_date + '-01')  # Assuming day is 01
        except ValueError:
            raise forms.ValidationError('Invalid date format.')

        # Get the current month and year
        current_date = date.today()
        current_month, current_year = current_date.month, current_date.year

        # Check if the selected month and year are greater than or equal to the current month and year
        if expiry_date.year < current_year or (expiry_date.year == current_year and expiry_date.month < current_month):
            raise forms.ValidationError('Expiry date must be greater than or equal to the current month and year.')

        return expiry_date