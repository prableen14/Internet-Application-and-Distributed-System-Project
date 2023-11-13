# Register your models here.
from django.contrib import admin
from django.db import models
from .models import CustomUser, Coin
from django.contrib.auth.models import Group, User

admin.site.register(CustomUser)
admin.site.register(Coin)


# here i am extending the user model
class UserAdmin(admin.ModelAdmin):
    model = User
    # displaying the username field
    fields = ["username"]
