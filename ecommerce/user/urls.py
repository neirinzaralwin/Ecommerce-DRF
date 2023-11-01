from django.urls import include, path
from .views import UserCreate, UserLogin, UserInfoFromToken, UserListView

app_name = "users"

urlpatterns = [
    path("register/", UserCreate.as_view(), name="create_user"),
    path("login/", UserLogin.as_view(), name="login"),
    path("info/", UserInfoFromToken.as_view(), name="user_info"),
    path("list/", UserListView.as_view(), name="user_list"),
    path("cart/", include("ecommerce.cart.urls")),
    path("order/", include("ecommerce.order.urls")),
]
