from django.contrib.auth.models import AbstractUser
from django.db import models

CATERGORIES = (
    ("Antiques", "Antiques"),
    ("Books", "Books"),
    ("Bussiness & Industrial", "Bussiness & Industrial"),
    ("Clothing, Shoes & Accessories", "Clothing, Shoes & Accessories"),
    ("Collectibles", "Collectibles"),
    ("Computers, Tablets & Networking", "Computers, Tablets & Networking"),
    ("Consumer Electronics", "Consumer Electronics"),
    ("Crafts", "Crafts"),
    ("Dolls & Bears", "Dolls & Bears"),
    ("Home & Garden", "Home & Garden"),
    ("Mobiles Phones & Accessories", "Mobile Phones & Accessories"),
    ("Motors", "Motors"),
    ("Pet Supplies", "Pet Supplies"),
    ("Sporting Goods", "Sporting Goods"),
    ("Toys & Hobbies", "Toys & Hobbies"),
    ("Others", "Others"),
    ("Videos Games & Consoles", "Video Games & Consoles")
)

class User(AbstractUser):
    pass


class Product(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    user = models.ForeignKey('User', related_name="product_user", on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    description = models.TextField(max_length=1024)
    image_url = models.CharField(max_length=1024, blank=True)
    opening_bid = models.PositiveIntegerField()
    current_bid = models.PositiveIntegerField(default=0)
    category = models.CharField(max_length=64, choices=CATERGORIES, blank=True)
    closed = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return f"#{self.id} {self.title}"



class Comment(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name="comment_product")
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name="comment_user")
    comment = models.TextField(max_length=512)

    def __str__(self):
        return f"#{self.id} {self.user} on {self.product.title}"


class Bid(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    bid = models.PositiveIntegerField()
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name="bid_user")
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name="bid_product")

    def __str__(self):
        return f"${self.bid} by {self.user} on {self.product.title}"


class Watchlist(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name="watch_user")
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name="watch_product")

    def __str__(self):
        return f"{self.user} is watching {self.product.title}"

class ClosedProduct(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name="close_user")
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name="close_product")
    winning_user = models.ForeignKey(
        'User', 
        on_delete=models.CASCADE, 
        related_name="winning_user",
        default=None,
        blank=True,
        null=True
    )

    def __str__(self):
        return f"#{self.id} {self.product.title} won by {self.winning_user}"


