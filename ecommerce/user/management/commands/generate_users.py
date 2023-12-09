from faker import Faker
from ecommerce.user.models import User
from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string
import random


fake = Faker(["en_US"])


class Command(BaseCommand):
    help = "Generate random users"

    def add_arguments(self, parser):
        parser.add_argument(
            "count", type=int, help="Indicates the number of users to be created"
        )

    def handle(self, *args, **kwargs):
        count = kwargs["count"]

        for i in range(count):
            username = fake.name()
            phone = f"09{random.randint(1, 999999999)}"
            address = fake.address()

            User.manager.create_user(
                username=username,
                phone=phone,
                password=get_random_string(12),
                address=address,
            )

        self.stdout.write(
            self.style.SUCCESS(f"{count} users are generated successfully")
        )
