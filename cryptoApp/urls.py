from django.urls import path
from cryptoApp import views
from django.contrib.auth import views as auth_views
from cryptoApp.article_views import (
  ArticleCreateView, ArticleListView, ArticleDetailView
)

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.custom_login, name='login'),
    path('logout/', views.logout_view, name='logout_view'),
    path('index/', views.index, name='index'),
    path('coin/<int:coin_id>', views.coin_detail, name='coin_detail'),
    path('converter/', views.converter, name='converter'),
    path('watchlist/', views.watchlist, name='watchlist'),
    path('add_to_watchlist/<int:coin_id>/', views.add_to_watchlist, name='add_to_watchlist'),
    path('remove_from_watchlist/<int:coin_id>/', views.remove_from_watchlist, name='remove_from_watchlist'),
    path('socials_home/', views.socials_home, name="socials_home"),
    path('transaction/', views.user_transactions, name='user_transactions'),
    path('wallet/<int:coin_id>/', views.wallet_view, name='wallet_view'),
    path('sell_transaction/<int:transaction_id>/', views.sell_transaction, name='sell_transaction'),
    path('success/', views.success_view, name='success_view'),
    path('failure/', views.insufficient_balance_view, name='insufficient_balance_view'),
    path('submit_exchange/', views.add_currency, name='submit_exchange'),
    path('submit_crypto/', views.add_coin, name='submit_crypto'),
    path(
      'articles/create/', ArticleCreateView.as_view(),
      name='article_create'
    ),
    path('articles/', ArticleListView.as_view(), name='article_list'),
    path(
      'articles/<int:pk>/', ArticleDetailView.as_view(),
      name='article_detail'
    ),
    path('socials_profile_list/', views.socials_profile_list, name="socials_profile_list"),
    path('socials_profile/<int:pk>', views.socials_profile_list, name="socials_profile_list"),

]
