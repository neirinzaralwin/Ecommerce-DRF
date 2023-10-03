from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json
from .models import Category, Brand, Product
from .serializers import (
    CategorySerializer,
    BrandSerializer,
    ProductSerializer,
    ProductCreateSerializer,
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
        serializer = ProductCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            product = Product.objects.get(id=serializer.data.get("id"))
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
