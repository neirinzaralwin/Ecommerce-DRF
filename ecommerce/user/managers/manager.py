from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, **extra_fields):
        user = self.model(**extra_fields)
        user.save()
        return user

    def create_superuser(self, **extra_fields):
        user = self.model(**extra_fields)
        user.is_admin = True
        user.role = self.model.Role.ADMIN
        user.save()
        return user

    def get_queryset(self):
        return super().get_queryset()


class StaffManager(BaseUserManager):
    def get_queryset(self):
        return super().get_queryset().filter(is_admin=False, is_staff=True)


class CustomerManager(BaseUserManager):
    def get_queryset(self):
        return super().get_queryset().filter(is_admin=False, is_staff=False)
