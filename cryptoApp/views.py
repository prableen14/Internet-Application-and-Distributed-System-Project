from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect, get_object_or_404
from .forms import SignUpForm, CustomAuthenticationForm, ConverterForm, TransactionForm, CurrencyForm, CoinForm
from django.contrib.auth.decorators import login_required
from .models import Coin, CurrencyConverter, CustomUser, Transaction, SocialsProfile, Article, Currency, Watchlist
import requests
from django.utils import timezone
from django.contrib import messages


def home(request):
    return render(request, 'cryptoApp/home.html')


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            # login(request, user)
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
            return redirect('index')
        else:
            messages.error(request, 'Invalid username or password. Please try again.')
    else:
        form = CustomAuthenticationForm()

    return render(request, 'cryptoApp/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

def watchlist(request):
    if request.user.is_authenticated:
        watchlist_entry, created = Watchlist.objects.get_or_create(user=request.user)
        return render(request, 'cryptoApp/watchlist.html', {'watchlist': watchlist_entry})
    else:
        return redirect('login')
def add_to_watchlist(request, coin_id):
    if request.user.is_authenticated:
        coin = Coin.objects.get(id=coin_id)
        watchlist_entry, created = Watchlist.objects.get_or_create(user=request.user)
        watchlist_entry.coins.add(coin)
        messages.success(request, f"{coin.name} added to your watchlist.")
    else:
        messages.warning(request, "Please log in to add coins to your watchlist.")

    return redirect('index')

def remove_from_watchlist(request, coin_id):
    if request.user.is_authenticated:
        coin = get_object_or_404(Coin, id=coin_id)
        watchlist_entry, created = Watchlist.objects.get_or_create(user=request.user)

        if watchlist_entry.coins.filter(id=coin_id).exists():
            watchlist_entry.coins.remove(coin)
            messages.success(request, f"{coin.name} removed from your watchlist.")
        else:
            messages.warning(request, f"{coin.name} is not in your watchlist.")
    else:
        messages.warning(request, "Please log in to manage your watchlist.")

    return redirect('watchlist')
def index(request):
    coins = Coin.objects.all()
    for coin in coins:
        coin.market_cap = format_money(coin.market_cap)
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

    # Get the 3 trending coins (you can customize the criteria for trending)
    trending_coins = Coin.objects.order_by('-percentage_change_24h')[:3]

    recent_users = CustomUser.objects.order_by('-createdDate')[:3]

    # Retrieve the three most recent articles
    recent_articles = Article.objects.order_by('-created_at')[:2]
    print(recent_articles)

    result = {
        'recently_added_coins': recently_added_coins,
        'trending_coins': trending_coins,
        'recent_users': recent_users,
        'recent_articles': recent_articles
    }
    return result


def add_currency(request):
    if request.method == 'POST':
        form = CurrencyForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            if Currency.objects.filter(code=code).exists():
                # Currency with the given code already exists
                form.add_error('code', 'Currency with this code already exists.')
            else:
                form.save()
                messages.success(request, 'Currency added successfully.')
    else:
        form = CurrencyForm()

    return render(request, 'cryptoApp/add_currency.html', {'form': form})


def add_coin(request):
    if request.method == 'POST':
        form = CoinForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            if Coin.objects.filter(name=name).exists():
                form.add_error('name', 'Coin with this name already exists.')
            else:
                form.save()
                messages.success(request, 'Coin added successfully.')
    else:
        form = CoinForm()

    return render(request, 'cryptoApp/add_coin.html', {'form': form})


def socials_home(request):
    return render(request, 'cryptoApp/socials_home.html', {})


@login_required
def wallet_view(request, coin_id=None):
    user = request.user

    try:
        order = Coin.objects.get(pk=coin_id)
        form = TransactionForm(order, request.POST or None)

        if request.method == 'POST' and form.is_valid():
            order_price = order.price

            # Check if the order price is less than or equal to the user's balance
            if order_price <= user.balance:
                # Calculate balance_after_transaction
                balance_after_transaction = user.balance - order_price

                # Create and save the Transaction model
                transaction = Transaction.objects.create(
                    user=user,
                    order=order,
                    timestamp=timezone.now(),
                    transaction_type='buy',
                    balance_after_transaction=balance_after_transaction
                )

                # Update user balance
                user.balance = balance_after_transaction
                user.save()

                return redirect('success_view')
            else:
                # Display an error message or take appropriate action
                return redirect('insufficient_balance_view')

        return render(request, 'cryptoApp/payment.html', {'form': form, 'order': order, 'coin': order})

    except Coin.DoesNotExist:
        print(f"Order with id {coin_id} not found.")
        return render(request, 'cryptoApp/payment.html', {'form': None, 'order': None})


def success_view(request):
    return render(request, 'cryptoApp/sell_transaction.html')


def insufficient_balance_view(request):
    return render(request, 'cryptoApp/paymentfailure.html')


@login_required()
def user_transactions(request):
    user = request.user
    transactions = Transaction.objects.filter(user=user)

    return render(request, 'cryptoApp/transaction_history.html', {'transactions': transactions})


@login_required()
def sell_transaction(request, transaction_id):
    buy_transaction = get_object_or_404(Transaction, pk=transaction_id)
    order_price = buy_transaction.order.price
    # Check if the transaction is a 'buy' type before attempting to sell
    if buy_transaction.transaction_type == 'buy':
        if buy_transaction.sold:
            # Handle the case where the order has already been sold
            messages.error(request, "This order has already been sold.")
            return redirect('user_transactions')
        # Create a new 'sell' transaction
        buy_transaction.sold = True
        buy_transaction.save()
        sell_transaction = Transaction(
            user=request.user,
            order=buy_transaction.order,  # Use the same order as the buy transaction
            timestamp=timezone.now(),
            transaction_type='sell',
            balance_after_transaction=request.user.balance + buy_transaction.order.price,
        )

        # Save the new 'sell' transaction
        sell_transaction.save()

        # Update the user's balance
        request.user.balance = sell_transaction.balance_after_transaction
        request.user.save()
        # Redirect to the user_transactions page
        return redirect('success_view')

    return render(request, 'cryptoApp/sell_transaction.html', {'transaction': buy_transaction})


def socials_profile_list(request):
    if request.user.is_authenticated:
        profiles = SocialsProfile.objects.exclude(user=request.user)
        return render(request, 'cryptoApp/socials_profile_list.html', {"profiles": profiles})
    else:
        messages.success(request, ("You must be logged in to view this page ..."))
        return redirect(request, 'cryptoApp/index.html')
