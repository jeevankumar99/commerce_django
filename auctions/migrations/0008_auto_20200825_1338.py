# Generated by Django 3.0.8 on 2020-08-25 13:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_auto_20200823_1634'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(blank=True, choices=[('Antiques', 'Antiques'), ('Books', 'Books'), ('Bussiness & Industrial', 'Bussiness & Industrial'), ('Clothing, Shoes & Accessories', 'Clothing, Shoes & Accessories'), ('Collectibles', 'Collectibles'), ('Computers, Tablets & Networking', 'Computers, Tablets & Networking'), ('Consumer Electronics', 'Consumer Electronics'), ('Crafts', 'Crafts'), ('Dolls & Bears', 'Dolls & Bears'), ('Home & Garden', 'Home & Garden'), ('Mobiles Phones & Accessories', 'Mobile Phones & Accessories'), ('Motors', 'Motors'), ('Pet Supplies', 'Pet Supplies'), ('Sporting Goods', 'Sporting Goods'), ('Toys & Hobbies', 'Toys & Hobbies'), ('Others', 'Others'), ('Videos Games & Consoles', 'Video Games & Consoles')], max_length=64),
        ),
        migrations.CreateModel(
            name='ClosedProduct',
            fields=[
                ('id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='close_product', to='auctions.Product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='close_user', to=settings.AUTH_USER_MODEL)),
                ('winning_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='winning_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
