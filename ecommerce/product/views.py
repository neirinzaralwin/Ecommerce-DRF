from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json
from .models import Category, Brand, Product, Discount
from .validations.discount_validation import validateDiscountPercentage
from .serializers import (
    CategorySerializer,
    BrandSerializer,
    ProductSerializer,
)


class CategoryViewSet(viewsets.ViewSet):
    queryset = Category.objects.all()

    def list(self, request):
        serializer = CategorySerializer(self.queryset, many=True)
        return Response(
            {"success": True, "message": "successful", "data": serializer.data}
        )

    def create(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "success": True,
                    "message": "Category created successfully",
                    "data": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                {
                    "success": False,
                    "message": "Category creation failed",
                    "error": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


class BrandViewSet(viewsets.ViewSet):
    queryset = Brand.objects.all()

    def list(self, request):
        serializer = BrandSerializer(self.queryset, many=True)
        return Response(
            {"success": True, "message": "successful", "data": serializer.data}
        )

    def create(self, request):
        serializer = BrandSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "success": True,
                    "message": "Brand created successfully",
                    "data": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                {
                    "success": False,
                    "message": "Brand creation failed",
                    "error": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


class ProductViewSet(viewsets.ViewSet):
    queryset = Product.objects.all()

    def list(self, request):
        serializer = ProductSerializer(self.queryset, many=True)
        if serializer.data:
            return Response(
                {"success": True, "message": "successful", "data": serializer.data}
            )
        else:
            return Response({"success": True, "message": "No product yet", "data": []})

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
                                "success": False,
                                "message": "Percentage must be between 0 and 100",
                            },
                            status=status.HTTP_400_BAD_REQUEST,
                        )
            return Response(
                {
                    "success": True,
                    "message": "Product created successfully",
                    "data": ProductSerializer(product, many=False).data,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {"success": False, "message": "Invalid data", "data": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def update(self, request, pk=None):
        try:
            instance = self.queryset.get(pk=pk)
            serializer = ProductSerializer(instance, data=request.data, partial=True)
            if serializer.is_valid():
                obj = serializer.save()
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

    def destroy(self, request, pk=None):
        try:
            if pk is not None:
                product = self.queryset.get(pk=pk)
                product.delete()
                return Response(
                    {"success": True, "message": "Product deleted successfully"},
                    status=status.HTTP_200_OK,
                )
            else:
                Product.objects.all().delete()
                return Response(
                    {"success": True, "message": "All products deleted successfully"},
                    status=status.HTTP_200_OK,
                )
        except Product.DoesNotExist:
            return Response(
                {"success": False, "message": "Product doesn't exist"},
                status=status.HTTP_404_NOT_FOUND,
            )


@api_view(["GET"])
def product_detail_view(request):
    id = request.GET.get("id", None)
    queryset = Product.objects.all()
    if request.method == "GET":
        try:
            product = get_object_or_404(Product, pk=id)
            serializer = ProductSerializer(product)
            return Response(
                {"success": True, "message": "Success", "data": serializer.data}
            )
        except:
            return Response(
                {"success": True, "message": "Product not found", "data": {}}
            )
