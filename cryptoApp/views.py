from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import ArticleForm, SignUpForm, CustomAuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Article, Coin


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
    return render(request, 'cryptoApp/index.html', {'coins': coins})


def coin_detail(request, coin_id):
    coin = get_object_or_404(Coin, id=coin_id)
    return render(request, 'cryptoApp/coinDetail.html', {'coin': coin})


def socials_home(request):
    return render(request, 'cryptoApp/socials_home.html', {})


class ArticleCreateView(View):
    def get(self, request, *args, **kwargs):
        form = ArticleForm()
        return render(request, 'cryptoApp/create_article.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            return redirect('article_list')  # Redirect to the view displaying all articles
        return render(request, 'cryptoApp/create_article.html', {'form': form})


class ArticleListView(View):
    def get(self, request, *args, **kwargs):
        articles = Article.objects.all()  # Retrieve all articles from the database
        return render(
            request, 'cryptoApp/article_list.html', {'articles': articles}
        )
