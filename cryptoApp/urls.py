from django.urls import path
from cryptoApp import views
from django.contrib.auth import views as auth_views
from cryptoApp.views.article_views import (
  ArticleCreateView, ArticleListView, ArticleDetailView
)

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('profile/', views.profile_view, name='profile'),
    path('login/', views.custom_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', views.index, name='index'),
    path('coin/<int:coin_id>', views.coin_detail, name='coin_detail'),
    path('socials_home/', views.socials_home, name="socials_home"),
    path(
      'articles/create/', ArticleCreateView.as_view(),
      name='article_create'
    ),
    path('articles/', ArticleListView.as_view(), name='article_list'),
    path(
      'articles/<int:pk>/', ArticleDetailView.as_view(),
      name='article_detail'
    ),
]
