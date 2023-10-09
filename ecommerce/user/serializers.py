from rest_framework import serializers
from .models import User, Staff, Customer


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=150,
        required=True,
        write_only=True,
        read_only=False,
        style={"input_type": "password"},
    )
    role = serializers.ChoiceField(choices=["Staff", "Customer"], required=False)

    class Meta:
        model = User
        fields = "__all__"

    def create(self, validated_data):
        role = validated_data.pop("role", None)
        instance = self.Meta.model(**validated_data)
        if role is None:
            instance.role = instance.base_role
        instance.save()
        return instance
