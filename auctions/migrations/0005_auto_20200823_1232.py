# Generated by Django 3.0.8 on 2020-08-23 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_auto_20200823_1230'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(blank=True, choices=[('Antiques', 'Antiques'), ('Books', 'Books'), ('Bussiness & Industrial', 'Bussiness & Industrial'), ('Clothing, Shoes & Accessories', 'Clothing, Shoes & Accessories'), ('Collectibles', 'Collectibles'), ('Computers, Tablets & Networking', 'Computers/Tables & Networking'), ('Consumer Electronics', 'Consumer Electronics'), ('Crafts', 'Crafts'), ('Dolls & Bears', 'Dolls & Bears'), ('Home & Garden', 'Home & Garden'), ('Motors', 'Motors'), ('Pet Supplies', 'Pet Supplies'), ('Sporting Goods', 'Sporting Goods'), ('Toys & Hobbies', 'Toys & Hobbies'), ('Other', 'Other')], default='Others', max_length=64),
        ),
        migrations.AlterField(
            model_name='product',
            name='image_url',
            field=models.CharField(blank=True, default=None, max_length=1024),
        ),
    ]
