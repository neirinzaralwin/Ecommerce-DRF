from rest_framework import serializers
from .models import Category, Brand, Product, Discount, ProductImage
from django.conf import settings


class CategorySerializer(serializers.ModelSerializer):
    parent_category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), allow_null=True, source="parent"
    )

    class Meta:
        model = Category
        fields = ["id", "name", "parent_category_id"]


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = "__all__"


class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = "__all__"


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["image"]


class ProductSerializer(serializers.ModelSerializer):
    brand = BrandSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    brand_id = serializers.PrimaryKeyRelatedField(
        queryset=Brand.objects.all(), source="brand", allow_null=False, write_only=True
    )
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source="category",
        allow_null=True,
        write_only=True,
    )
    discount_price = serializers.SerializerMethodField(read_only=True)
    discounts = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField(required=False)

    class Meta:
        model = Product
        fields = "__all__"

    def get_images(self, obj):
        try:
            images = obj.images.all()
            image_urls = [img.image.url for img in images]
            return image_urls
        except:
            return []

    def get_discounts(self, obj):
        try:
            discounts = obj.discounts.all()
            return DiscountSerializer(discounts, many=True).data
        except:
            return []

    def get_discount_price(self, obj):
        original_price = obj.price
        discounts = obj.discounts.all()
        price_list = []
        if discounts:
            for discount in discounts:
                price = (discount.percentage / 100) * original_price
                price_list.append(price)
            return sum(price_list)
        return original_price
