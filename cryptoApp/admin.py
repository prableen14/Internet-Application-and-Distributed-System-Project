# Register your models here.
from django.contrib import admin
from django.db import models
from .models import CustomUser, Coin

admin.site.register(CustomUser)
admin.site.register(Coin)
