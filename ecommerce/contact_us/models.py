from django.db import models
from django.utils import timezone


class ContactType(models.TextChoices):
    FACEBOOK = "FACEBOOK", "Facebook"
    MESSENGER = "MESSENGER", "Messenger"
    TELEGRAM = "TELEGRAM", "Telegram"
    PHONE = "PHONE", "Phone"
    VIBER = "VIBER", "Viber"


# Create your models here.
class Contact(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    value = models.CharField(max_length=50, null=False, blank=False)
    contact_type = models.CharField(
        max_length=25, choices=ContactType.choices, null=False, blank=False
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)


class AboutUs(models.Model):
    text = models.TextField(default="", max_length=3000)
