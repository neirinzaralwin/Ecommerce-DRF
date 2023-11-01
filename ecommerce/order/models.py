from django.db import models
from ecommerce.user.models import User
from ecommerce.cart.models import Cart


class OrderStatus:
    PENDING = "pending"
    CONFIRMED = "confirmed"
    REJECTED = "rejected"
    DELIVERED = "delivered"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    items = models.ManyToManyField(Cart, blank=False)
    status = models.CharField(max_length=20, default=OrderStatus.PENDING)
