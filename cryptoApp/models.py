# Create your models here.
from django.db import models
from django.contrib.auth.models import User, AbstractUser, Group, Permission
from django.conf import settings
from django.db.models.signals import post_save


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    id_or_photo = models.FileField(upload_to='id_photos/', null=True, blank=True)
    groups = models.ManyToManyField(Group, related_name='customuser_set', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='customuser_set', blank=True)
    createdDate = models.DateTimeField(auto_now_add=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=500.00)

class Watchlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    coins = models.ManyToManyField('Coin')
    def __str__(self):
        coin_names = ', '.join([coin.name for coin in self.coins.all()])
        return f"{self.user.username}'s Watchlist - {coin_names}"
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


class SocialsProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)  # one user will have only onle profile
    follows = models.ManyToManyField("self",
                                     related_name="followed_by",
                                     symmetrical=False,
                                     blank=True)
    date_modified = models.DateTimeField(User, auto_now=True)
    def __str__(self):
        return self.user.username
    # one user can follow many profiles - ManyToManyField
    # related_name - will be using this later for search query
    # symmetrical -  False -  so that if I follow someone they don't have to necessarily follow me
    # blank=True - this means that if i want to I don't have to follow anyone


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

def create_socialsprofile(sender, instance, created, **kwargs):
    if created:
        user_socialsprofile, created = SocialsProfile.objects.get_or_create(user=instance)
        if created:
            user_socialsprofile.follows.add(user_socialsprofile)
            user_socialsprofile.save()

        # Connect the signal
        post_save.connect(create_socialsprofile, sender=CustomUser)

        # user_socialsprofile = SocialsProfile(user=instance)
        # user_socialsprofile.save()
        # user_socialsprofile.follows.add([user_socialsprofile.id])
        # user_socialsprofile.save()


# post_save.connect(create_socialsprofile, sender=CustomUser)