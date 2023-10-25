from django.urls import include, path
from .views import CartView, DeleteAllCart

app_name = "carts"

urlpatterns = [
    path("add/", CartView.as_view(), name="add-to-cart"),
    path("delete-all/", DeleteAllCart.as_view(), name="delete-all-cart"),
]
