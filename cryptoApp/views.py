from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect, get_object_or_404
from .forms import SignUpForm, CustomAuthenticationForm, ConverterForm
from django.contrib.auth.decorators import login_required
from .models import Coin, CurrencyConverter, CustomUser
import requests


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'cryptoApp/signup.html', {'form': form})


def custom_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            print("User authenticated:", user.username)
            login(request, user)
            return redirect('profile')
        else:
            print("Authentication failed for user:", username)
    else:
        form = CustomAuthenticationForm()

    return render(request, 'cryptoApp/login.html', {'form': form})


@login_required
def profile_view(request):
    user = request.user
    return render(request, 'cryptoApp/profile.html', {'user': user})


def index(request):
    coins = Coin.objects.all()
    highlight = get_hightlight_details()
    return render(request, 'cryptoApp/index.html', {'coins': coins, 'highlight': highlight})


def coin_detail(request, coin_id):
    coin = get_object_or_404(Coin, id=coin_id)
    print(coin.icon_url)
    return render(request, 'cryptoApp/coinDetail.html', {'coin': coin})


def format_money(amount):
    return "{:,.2f}".format(amount)


def calculate_conversion(coin, amount, currency, is_coin_to_currency=True):
    coin_data = requests.get(f'https://api.coingecko.com/api/v3/coins/{coin.name.lower()}').json()
    coin.price = coin_data.get('market_data', {}).get('current_price', {}).get(currency.code.lower(), coin.price)
    coin.save()

    if is_coin_to_currency:
        result = amount * float(coin.price)
    else:
        result = amount / float(coin.price)

    return result


def converter(request):
    result = None
    display_result = None

    if request.method == 'POST':
        form = ConverterForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            print(data['currency'])
            coin = get_object_or_404(Coin, name=data['coin_type'])
            print(data['is_coin_to_currency'])
            result = calculate_conversion(coin, data['amount'], data['currency'], data['is_coin_to_currency'])
            converter_instance = CurrencyConverter.objects.create(
                coin=coin,
                amount=data['amount'],
                currency=data['currency'],
                result=result,
                is_coin_to_currency=data['is_coin_to_currency']
            )
            if data['is_coin_to_currency']:
                display_result = f"{result} {data['currency'].code}"
            else:
                display_result = f"{result} {coin.name}"
    else:
        form = ConverterForm()

    return render(request, 'cryptoApp/converter.html', {'form': form, 'result': display_result})


def get_hightlight_details():
    # Get the 3 most recently added coins
    recently_added_coins = Coin.objects.order_by('-createdDate')[:3]
    print(recently_added_coins)

    # Get the 3 trending coins (you can customize the criteria for trending)
    trending_coins = Coin.objects.order_by('-percentage_change_24h')[:3]
    recent_users = CustomUser.objects.order_by('-createdDate')[:3]

    result = {
        'recently_added_coins': recently_added_coins,
        'trending_coins': trending_coins,
        'recent_users': recent_users,
    }
    return result


def socials_home(request):
    return render(request, 'cryptoApp/socials_home.html',{})
