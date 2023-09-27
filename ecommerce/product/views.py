from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.response import Response
from .models import Category, Brand, Product
from .serializers import CategorySerializer, BrandSerializer, ProductSerializer

class CategoryViewSet(viewsets.ViewSet):
    queryset = Category.objects.all()
    
    @extend_schema(responses=CategorySerializer)
    def list(self, request):
        serializer = CategorySerializer(self.queryset, many=True)
        return Response({
            "success" : True,
            "message" : "successful",
            "data" : serializer.data
        })

class BrandViewSet(viewsets.ViewSet):
    queryset = Brand.objects.all()
    
    @extend_schema(responses=BrandSerializer)
    def list(self, request):
        serializer = BrandSerializer(self.queryset, many=True)
        return Response({
            "success" : True,
            "message" : "successful",
            "data" : serializer.data
        })

class ProductViewSet(viewsets.ViewSet):
    queryset = Product.objects.all()
    @extend_schema(responses=ProductSerializer)
    def list(self, request):
        serializer = ProductSerializer(self.queryset, many=True)
        return Response({
            "success" : True,
            "message" : "successful",
            "data" : serializer.data
        })
