from faker import Faker
from faker.providers import internet
from ecommerce.product.models import Category, Brand, Product, ProductImage
from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string
import random


fake = Faker(["en_US"])
fake.add_provider(internet)


# local functions
def create_category():
    for i in range(3):
        Category.objects.create(name=f"Category_{fake.word()}")


def create_brand():
    for i in range(3):
        Brand.objects.create(name=fake.word())


def create_product(count):
    image_url = "https://picsum.photos/200"
    for i in range(count):
        name = "Product " + fake.word()
        description = fake.text()
        is_digital = bool(random.randint(0, 1))
        price = random.randint(1000, 100000)
        # Select random category and brand
        category = Category.objects.order_by("?").first()
        brand = Brand.objects.order_by("?").first()
        # Create image
        # image = ProductImage(image=fake.image_url())
        image = ProductImage(image=image_url)
        image.save()
        # Create the product
        product = Product.objects.create(
            name=name,
            price=price,
            is_digital=is_digital,
            category=category,
            brand=brand,
        )
        product.images.add(image)


class Command(BaseCommand):
    help = "Generate random users"

    def add_arguments(self, parser):
        parser.add_argument(
            "count", type=int, help="Indicates the number of users to be created"
        )

    def handle(self, *args, **kwargs):
        count = kwargs["count"]
        create_category()
        create_brand()
        create_product(count)
        self.stdout.write(
            self.style.SUCCESS(f"{count} products are generated successfully")
        )
