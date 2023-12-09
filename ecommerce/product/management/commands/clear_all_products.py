from django.core.management.base import BaseCommand
from ecommerce.product.models import Category, Brand, Product


class Command(BaseCommand):
    help = "Clear all products"

    def handle(self, *args, **kwargs):
        Product.objects.all().delete()
        Brand.objects.all().delete()
        Category.objects.all().delete()
        self.stdout.write(self.style.WARNING("All products have been deleted"))
