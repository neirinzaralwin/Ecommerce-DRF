from rest_framework import serializers
from .models import Order
from ecommerce.cart.models import Cart
from ecommerce.cart.serializers import CartSerializer


class OrderSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()
    grand_total = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Order
        exclude = ("user",)

    def get_items(self, obj):
        try:
            carts = obj.items.all()
            return CartSerializer(carts, many=True).data
        except:
            return []

    def get_grand_total(self, obj):
        carts = obj.items.all()
        if carts:
            value = 0.0
            for cart in carts:
                serializer = CartSerializer(cart)
                value += serializer.data.get("total")
            return value
        else:
            return 0.0
