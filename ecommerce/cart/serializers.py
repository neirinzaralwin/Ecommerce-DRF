from rest_framework import serializers
from ecommerce.product.serializers import ProductSerializer
from ecommerce.user.models import User
from ecommerce.product.models import Product
from ecommerce.cart.models import Cart, CartSession
from ecommerce.user.serializers import UserSerializer


class CartSerializer(serializers.ModelSerializer):
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source="parent", write_only=True
    )
    product = ProductSerializer(read_only=True)

    class Meta:
        model = Cart
        fields = "__all__"


class CartSessionSerializer(serializers.ModelSerializer):
    # Fields
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.manager.all(), source="parent", write_only=True
    )
    total = serializers.SerializerMethodField()
    carts = serializers.SerializerMethodField()
    user = UserSerializer(write_only=True)

    class Meta:
        model = CartSession
        fields = "__all__"

    def get_carts(self, obj):
        try:
            carts = obj.carts.all()
            return CartSerializer(carts, many=True).data
        except:
            return []

    def get_total(self, obj):
        carts = obj.carts.all()
        if carts:
            value = 0.0
            for cart in carts:
                value += cart.product.price
            return value
        else:
            return 0.0
