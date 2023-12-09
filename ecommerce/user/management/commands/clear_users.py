from ecommerce.user.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Clear all users"

    def handle(self, *args, **kwargs):
        User.manager.all().delete()
        self.stdout.write(self.style.WARNING("All users have been deleted"))
