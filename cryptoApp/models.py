# Create your models here.
from django.db import models
from django.contrib.auth.models import User, AbstractUser, Group, Permission

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    id_or_photo = models.FileField(upload_to='id_photos/', null=True, blank=True)
    groups = models.ManyToManyField(Group, related_name='customuser_set', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='customuser_set', blank=True)
