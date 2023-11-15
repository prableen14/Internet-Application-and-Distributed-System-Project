# Create your models here.
from django.db import models
from django.contrib.auth.models import User, AbstractUser, Group, Permission


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    id_or_photo = models.FileField(upload_to='id_photos/', null=True, blank=True)
    groups = models.ManyToManyField(Group, related_name='customuser_set', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='customuser_set', blank=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=500.00)


class Coin(models.Model):
    name = models.CharField(max_length=250,null=True)
    symbol = models.CharField(max_length=10, null=True)
    price = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    percentage_change_1h = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    percentage_change_24h = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    percentage_change_7d = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    market_cap = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    all_time_high = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    graph_link = models.URLField(blank=True)
    icon_url = models.URLField(blank=True)

    def __str__(self):
        return f"{self.name}"

#temporary model Order. Will be replaced with actual details model
class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)


class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('buy', 'Buy'),
        ('sell', 'Sell'),
    )

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    transaction_type = models.CharField(max_length=4, choices=TRANSACTION_TYPES)
    balance_after_transaction = models.DecimalField(max_digits=10, decimal_places=2)
    sold = models.BooleanField(default=False)