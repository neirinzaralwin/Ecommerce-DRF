from django.urls import path, re_path
from .views import (
    ProductViewSet,
    CategoryViewSet,
    BrandViewSet,
    product_detail_view,
    ProductImageUpload,
)

category_list = CategoryViewSet.as_view(
    {"get": "list", "post": "create"}
)  # Binding ViewSets to URLs explicitly

brand_list = BrandViewSet.as_view({"get": "list", "post": "create"})
product_list = ProductViewSet.as_view(
    {"get": "list", "post": "create", "patch": "update", "delete": "destroy"}
)


urlpatterns = [
    path("product/", product_list, name="product-list"),
    path("product/<int:pk>/", product_list, name="delete-product"),
    path(
        "product/<int:pk>/attach_image",
        ProductImageUpload.as_view(),
        name="attach-product-image",
    ),
    path("product/detail/", product_detail_view, name="product-detail-view"),
    path("category/", category_list, name="category-list"),
    path("brand/", brand_list, name="brand-list"),
]
