from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from .managers.manager import UserManager, StaffManager, CustomerManager


class User(AbstractBaseUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        STAFF = "STAFF", "Staff"
        CUSTOMER = "CUSTOMER", "Customer"

    username = models.CharField(max_length=250)
    phone = models.CharField(max_length=20, unique=True)
    created_at = models.DateTimeField(default=timezone.now())
    updated_at = models.DateTimeField(default=timezone.now())
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    base_role = Role.CUSTOMER
    role = models.CharField(max_length=50, choices=Role.choices)
    manager = UserManager()
    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        if not self.username:
            raise ValueError("You must provide a username")
        if not self.phone:
            raise ValueError("You must provide a phone number")
        if not self.password:
            raise ValueError("You must provide a password")
        else:
            self.password = make_password(self.password)
        if not self.role:
            self.role = Role.CUSTOMER
        print("----- user is saved -----")
        super().save(*args, **kwargs)


class Staff(User):
    class Meta:
        proxy = True

    manager = StaffManager()

    def save(self, *args, **kwargs):
        self.role = self.Role.STAFF
        self.is_staff = True
        super().save(*args, **kwargs)


class Customer(User):
    class Meta:
        proxy = True

    manager = CustomerManager()

    def save(self, *args, **kwargs):
        self.role = self.Role.CUSTOMER
        super().save(*args, **kwargs)
