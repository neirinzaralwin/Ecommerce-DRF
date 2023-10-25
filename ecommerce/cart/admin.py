from django.contrib import admin

from .models import Cart, CartSession

admin.site.register(Cart)
admin.site.register(CartSession)
