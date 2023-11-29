# Register your models here.
from django.contrib import admin
from django.db import models
from .models import CustomUser, Coin, Transaction, Currency, CurrencyConverter, Watchlist
from django.contrib.auth.models import Group, User

admin.site.register(CustomUser)
admin.site.register(Coin)
admin.site.register(Transaction)
admin.site.register(Currency)
admin.site.register(CurrencyConverter)
admin.site.register(Watchlist)


# here i am extending the user model
class UserAdmin(admin.ModelAdmin):
    model = User
    # displaying the username field
    fields = ["username"]
