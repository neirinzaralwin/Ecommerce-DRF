from django.urls import include, path
from .views import OrderNow, AllOrderAdminView

app_name = "orders"

urlpatterns = [
    path("send-order/", OrderNow.as_view(), name="send-order"),
    path(
        "all-orders-admin-view/",
        AllOrderAdminView.as_view(),
        name="all-orders-admin-view",
    ),
]
