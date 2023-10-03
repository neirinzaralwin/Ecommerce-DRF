from rest_framework import serializers
from .models import Category, Brand, Product, Discount


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

    # def validate_percentage(self, value):
    #     if value < 0 or value > 100:
    #         raise serializers.ValidationError(
    #             "Discount percentage must be between 0 and 100"
    #         )
    #     return value


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
            return DiscountSerializer(discounts, many=True).data
        except:
            return []


class ProductCreateSerializer(serializers.ModelSerializer):
    brand_id = serializers.PrimaryKeyRelatedField(
        queryset=Brand.objects.all(), allow_null=True, source="brand"
    )
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), allow_null=True, source="category"
    )

    class Meta:
        model = Product
        exclude = ["category", "brand"]
