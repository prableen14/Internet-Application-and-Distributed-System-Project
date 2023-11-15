# Register your models here.
from django.contrib import admin
from django.db import models
from .models import CustomUser, Coin, Order, Transaction

admin.site.register(CustomUser)
admin.site.register(Coin)
admin.site.register(Order)
admin.site.register(Transaction)
