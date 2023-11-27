from django.urls import path
from . import views
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
    path('transaction/', views.user_transactions, name='user_transactions'),
    path('wallet/<int:coin_id>/', views.wallet_view, name='wallet_view'),
    path('sell_transaction/<int:transaction_id>/', views.sell_transaction, name='sell_transaction'),
    path('success/', views.success_view, name='success_view'),
    path('failure/', views.insufficient_balance_view, name='insufficient_balance_view'),
    path('articles/create/', ArticleCreateView.as_view(),name='article_create'),
    path('articles/', ArticleListView.as_view(), name='article_list'),
    path('articles/<int:pk>/', ArticleDetailView.as_view(),name='article_detail'),
    path('s_home/',views.s_home, name="s_home"),
    path('profile_list/', views.profile_list, name='profile_list'),
    path('profile/<int:pk>', views.profile, name='profile' ),
    path('update_user/', views.update_user, name='update_user' ),
    path('beet_like/<int:pk>', views.beet_like, name='beet_like' ),

]
