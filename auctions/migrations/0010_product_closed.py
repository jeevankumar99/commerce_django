# Generated by Django 3.0.8 on 2020-08-26 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_auto_20200826_0717'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='closed',
            field=models.BooleanField(blank=True, default=False),
        ),
    ]
