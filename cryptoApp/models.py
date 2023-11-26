# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.conf import settings
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone

User = settings.AUTH_USER_MODEL
from django.db.models.signals import post_save


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    id_or_photo = models.FileField(upload_to='id_photos/', null=True, blank=True)
    groups = models.ManyToManyField(Group, related_name='customuser_set', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='customuser_set', blank=True)
    createdDate = models.DateTimeField(auto_now_add=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=500.00)


class Coin(models.Model):
    name = models.CharField(max_length=250, null=True)
    symbol = models.CharField(max_length=10, null=True)
    price = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    percentage_change_1h = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    percentage_change_24h = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    percentage_change_7d = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    market_cap = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    all_time_high = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    graph_link = models.URLField(blank=True)
    icon_url = models.URLField(blank=True)
    createdDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}"


class Currency(models.Model):
    code = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.code


class CurrencyConverter(models.Model):
    coin = models.ForeignKey(Coin, on_delete=models.CASCADE)
    amount = models.FloatField()
    currency = models.CharField(max_length=3)
    result = models.FloatField()
    is_coin_to_currency = models.BooleanField()

    def __str__(self):
        return f"{self.amount} {self.coin.symbol} to {self.currency}"


class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('buy', 'Buy'),
        ('sell', 'Sell'),
    )

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    order = models.ForeignKey(Coin, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    transaction_type = models.CharField(max_length=4, choices=TRANSACTION_TYPES)
    balance_after_transaction = models.DecimalField(max_digits=10, decimal_places=2)
    sold = models.BooleanField(default=False)


class Profile(models.Model):
    objects = None
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    follows = models.ManyToManyField("self",
                                     related_name="followed_by",
                                     symmetrical=False,
                                     blank=True)
    date_modified = models.DateTimeField(User,auto_now=True)

    def __str__(self):
        return self.user.username


# creating a profile when new users signup
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)  # creating a profile automatically for every user that gets created
        user_profile.save()
        # user follow themselves
        user_profile.follows.set([instance.profile.id])  # I am getting the id from the migrations file
        user_profile.save()  # we save twice because first we have to save the profile that was created and the
        # second time when they are followed


post_save.connect(create_profile, sender=User)  # when a new user has been saved we will create a new profile

