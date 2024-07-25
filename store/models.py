from django.db import models
import re

# Create your models here.

EMAIL_REGEX = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
def is_email(input):
    return EMAIL_REGEX.fullmatch(input) is not None

class Category(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    class Meta:
        ordering=["title"]

class Product(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    category = models.ManyToManyField(Category)
    stock = models.PositiveIntegerField(default=0)
    class Meta:
        ordering=["title"]

class User(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=100, validators=[is_email])
    pwdhash = models.BinaryField(max_length=256)

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING,
                              null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering=["created_at"]

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    class Meta:
        ordering=["quantity"]