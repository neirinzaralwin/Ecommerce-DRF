from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Category, Brand, Product, Discount, ProductImage
from .validations.discount_validation import validateDiscountPercentage
from ecommerce.common.custom_pagination import CustomPagination, PaginationHandlerMixin
from ecommerce.user.managers.jwt_manager import get_user_from_access_token

from ecommerce.permissions import (
    IsAdminInheritStaff,
    IsAdminOrStaff,
    IsAuthenticated,
    AllowAny,
)
from .serializers import (
    CategorySerializer,
    BrandSerializer,
    ProductSerializer,
    ProductImageSerializer,
)
from rest_framework.parsers import MultiPartParser, FormParser
from django.conf import settings


class CategoryViewSet(PaginationHandlerMixin, viewsets.ViewSet):
    pagination_class = CustomPagination
    queryset = Category.objects.all()
    permission_classes = [IsAuthenticated]

    def list(self, request):
        return self.custom_paginated_response(
            serializer_class=CategorySerializer, queryset=self.queryset
        )

    def create(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                {"error": "Category creation failed"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class BrandViewSet(viewsets.ViewSet, PaginationHandlerMixin):
    pagination_class = CustomPagination
    queryset = Brand.objects.all()
    permission_classes = [IsAuthenticated]

    def list(self, request):
        return self.custom_paginated_response(
            serializer_class=BrandSerializer, queryset=self.queryset
        )

    def create(self, request):
        serializer = BrandSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                {"error": "Brand creation failed"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class ProductViewSet(viewsets.ViewSet, PaginationHandlerMixin):
    pagination_class = CustomPagination
    queryset = Product.objects.all()
    permission_classes = [IsAuthenticated]

    def list(self, request):
        return self.custom_paginated_response(
            serializer_class=ProductSerializer, queryset=self.queryset
        )

    def create(self, request):
        discounts_data = request.data.pop("discounts", None)
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            obj = serializer.save()
            product = Product.objects.get(id=obj.id)
            if discounts_data:
                for dis in discounts_data:
                    if validateDiscountPercentage(dis.get("percentage")):
                        discount = Discount.objects.create(
                            name=dis.get("name"),
                            percentage=dis.get("percentage"),
                            product=product,  # Associate the discount with the product
                        )
                        product.discounts.add(discount)
                        product.save()
                    else:
                        return Response(
                            {
                                "error": "Percentage must be between 0 and 100",
                            },
                            status=status.HTTP_400_BAD_REQUEST,
                        )
            return Response(
                ProductSerializer(product, many=False).data,
                status=status.HTTP_201_CREATED,
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )

    def update(self, request, pk=None):
        # check admin or staff to update product
        user = get_user_from_access_token(self, request)
        if user is not None:
            if not (user.is_staff or user.is_admin):
                return Response(
                    {"error": "You are not authorized to update products"},
                    status=status.HTTP_403_FORBIDDEN,
                )

        try:
            discounts_data = request.data.pop("discounts", None)
            instance = self.queryset.get(pk=pk)
            serializer = ProductSerializer(instance, data=request.data, partial=True)
            if serializer.is_valid():
                obj = serializer.save()
                product = Product.objects.get(id=obj.id)
                if discounts_data:
                    product.discounts.clear()
                    for dis in discounts_data:
                        if validateDiscountPercentage(dis.get("percentage")):
                            discount = Discount.objects.create(
                                name=dis.get("name"),
                                percentage=dis.get("percentage"),
                                product=product,  # Associate the discount with the product
                            )
                            product.discounts.add(discount)
                            product.save()
                        else:
                            return Response(
                                {"error": "Percentage must be between 0 and 100"},
                                status=status.HTTP_400_BAD_REQUEST,
                            )
                return Response(
                    ProductSerializer(obj, many=False).data,
                    status=status.HTTP_200_OK,
                )
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )
        except:
            return Response(
                {"error": "Product not found"},
                status=status.HTTP_200_OK,
            )

    def destroy(self, request, pk=None):
        try:
            if pk is not None:
                product = self.queryset.get(pk=pk)
                product.delete()
                return Response(
                    status=status.HTTP_200_OK,
                )
            else:
                Product.objects.all().delete()
                return Response(
                    status=status.HTTP_200_OK,
                )
        except Product.DoesNotExist:
            return Response(
                {"error": "Product doesn't exist"},
                status=status.HTTP_404_NOT_FOUND,
            )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def product_detail_view(request):
    id = request.GET.get("id", None)
    queryset = Product.objects.all()
    if request.method == "GET":
        try:
            product = get_object_or_404(Product, pk=id)
            serializer = ProductSerializer(product)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(
                {"error": "Product not found"},
                status=status.HTTP_404_NOT_FOUND,
            )


class ProductImageUpload(APIView):
    permission_classes = [IsAdminOrStaff]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, pk=None):
        try:
            images = request.data.pop("images", None)
            obj = Product.objects.get(pk=pk)
            if images is not None:
                product = Product.objects.get(id=obj.id)
                if images:
                    product.images.clear()
                    for image in images:
                        image = ProductImage.objects.create(image=image)
                        product.images.add(image)
                        product.save()
                return Response(
                    {
                        "success": True,
                        "message": "Product updated successfully",
                        "data": ProductSerializer(obj, many=False).data,
                    },
                    status=status.HTTP_200_OK,
                )
            return Response(
                {
                    "success": False,
                    "message": "Invalid data",
                    "data": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        except:
            return Response(
                {"success": True, "message": "Product not found", "data": {}}
            )
