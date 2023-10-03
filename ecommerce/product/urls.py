from django.urls import path, re_path
from .views import ProductViewSet, CategoryViewSet, BrandViewSet, product_detail_view

category_list = CategoryViewSet.as_view(
    {"get": "list", "post": "create"}
)  # Binding ViewSets to URLs explicitly

brand_list = BrandViewSet.as_view({"get": "list", "post": "create"})
product_list = ProductViewSet.as_view(
    {"get": "list", "post": "create", "delete": "destroy"}
)

urlpatterns = [
    path("product/", product_list, name="product-list"),
    path("product/<int:pk>/", product_list, name="delete-product"),
    path("product/detail/", product_detail_view, name="product-detail-view"),
    path("category/", category_list, name="category-list"),
    path("brand/", brand_list, name="brand-list"),
]
