# Generated by Django 4.2.7 on 2023-11-11 22:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cryptoApp', '0002_coin_percentage_change_1h_coin_percentage_change_7d'),
    ]

    operations = [
        migrations.AddField(
            model_name='coin',
            name='icon_url',
            field=models.URLField(blank=True),
        ),
    ]
