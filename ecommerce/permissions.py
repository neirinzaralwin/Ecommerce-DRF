from rest_framework import permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from ecommerce.common.common import get_user_from_access_token


class IsAdminOrReadOnly(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        result = super().has_permission(request, view)  # is Authenticated
        if result:
            requested_role = request.data.get("role")
            return requested_role == "Admin"
        else:
            return request.method == "GET"


class IsAdminOrStaff(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        user = get_user_from_access_token(self, request)
        if user is not None:
            if user.is_staff or user.is_admin:
                return True
        return False


class IsAdminInheritStaff(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method != "POST":
            return False
        if request.user.is_staff:
            requested_role = request.data.get("role")
            if requested_role is None or requested_role == "Customer":
                return True
            return False
        return request.user.is_admin
