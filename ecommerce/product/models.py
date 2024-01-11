from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from ecommerce.common.common import file_location
from django.utils.translation import gettext_lazy as _


class Category(MPTTModel):
    name = models.CharField(max_length=100)
    parent = TreeForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)

    class MPTTMeta:
        order_insertion_by = ["name"]

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Discount(models.Model):
    name = models.CharField(max_length=100)
    percentage = models.FloatField()

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    image = models.ImageField(
        _("Image"),
        upload_to=file_location,
        default="default/product_default.jpg",
    )


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    description = models.TextField(blank=True)
    stock = models.IntegerField(blank=False, null=False, default=0)
    is_active = models.BooleanField(default=True)
    is_digital = models.BooleanField(default=False)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True, blank=True)
    category = TreeForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True
    )
    discounts = models.ManyToManyField(Discount, blank=True)
    images = models.ManyToManyField(ProductImage, blank=True)

    def __str__(self):
        return self.name

    # ordering
    class Meta:
        ordering = ["id"]
