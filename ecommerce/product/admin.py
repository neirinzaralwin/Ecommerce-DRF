from django.contrib import admin

from .models import Category, Brand, Product, Discount

admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Discount)
admin.site.register(Product)
