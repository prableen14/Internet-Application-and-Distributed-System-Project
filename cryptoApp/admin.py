# Register your models here.
from django.contrib import admin
from django.db import models
from .models import CustomUser, Coin, Transaction, Profile
from django.contrib.auth.models import Group, User


class ProfileInLine(admin.StackedInline):
    model = Profile


# extend user model
class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ["username"]
    inlines = [ProfileInLine]


admin.site.register(CustomUser)
admin.site.register(Coin)
admin.site.register(Transaction)

# admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Profile)
