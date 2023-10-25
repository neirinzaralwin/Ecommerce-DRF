from django.db import models
from django.utils import timezone
from ecommerce.user.models import User
from ecommerce.product.models import Product, Category, Brand, ProductImage


class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)


class CartSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    carts = models.ManyToManyField(Cart, blank=True)
