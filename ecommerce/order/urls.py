from django.urls import include, path
from .views import OrderNow

app_name = "orders"

urlpatterns = [
    path("send-order/", OrderNow.as_view(), name="send-order"),
]
