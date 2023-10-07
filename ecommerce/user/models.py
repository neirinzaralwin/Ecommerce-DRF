from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.utils import timezone
from django.contrib.auth.hashers import make_password


class UserManager(BaseUserManager):
    def create_user(self, **extra_fields):
        user = self.model(**extra_fields)
        user.save()
        return user

    def create_superuser(self, **extra_fields):
        user = self.create_user(**extra_fields)
        user.is_admin = True
        user.role = self.model.Role.ADMIN
        user.save()
        return user

    # def update_user(self, pk, **extra_fields):
    #     model = self.model(**extra_fields)
    #     if pk is not None:
    #         user = self.model.manager.get(pk=pk)
    #         for field, value in extra_fields.items():
    #             setattr(user, field, value)
    #         user.save()
    #         return user


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
    base_role = Role.ADMIN
    role = models.CharField(max_length=50, choices=Role.choices)
    manager = UserManager()
    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.username

    def save(self, pk=None, *args, **kwargs):
        self.updated_at = timezone.now()
        if pk is None:
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
        else:
            print(f"----- args {args}-----")
            print("----- user is updated -----")
        super().save(*args, **kwargs)


class Staff(User):
    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        self.role = self.Role.STAFF
        self.is_staff = True
        super().save(*args, **kwargs)


class Customer(User):
    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        self.role = self.Role.CUSTOMER
        super().save(*args, **kwargs)
