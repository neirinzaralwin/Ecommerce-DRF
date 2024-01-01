from rest_framework import serializers
from ecommerce.contact_us.models import Contact


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = "__all__"
