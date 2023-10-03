from rest_framework import serializers
from .models import Category, Brand, Product, ProductDiscount


class CategorySerializer(serializers.ModelSerializer):
    parent_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), allow_null=True, source="parent"
    )

    class Meta:
        model = Category
        fields = ["id", "name", "parent_id"]


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = "__all__"


class ProductDiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductDiscount
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    brand = BrandSerializer()
    category = CategorySerializer()
    discounts = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = "__all__"

    def get_discounts(self, obj):
        try:
            discounts = obj.discounts.all()
            return ProductDiscountSerializer(discounts, many=True).data
        except:
            return []


class ProductCreateSerializer(serializers.ModelSerializer):
    brand_id = serializers.PrimaryKeyRelatedField(
        queryset=Brand.objects.all(), allow_null=True, source="brand"
    )
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), allow_null=True, source="category"
    )
    discounts = serializers.SerializerMethodField()

    class Meta:
        model = Product
        exclude = ["category", "brand"]

    def get_discounts(self, obj):
        try:
            discounts = obj.discounts.all()
            return ProductDiscountSerializer(discounts, many=True).data
        except:
            return []
