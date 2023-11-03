from rest_framework import permissions
from ecommerce.user.managers.jwt_manager import get_user_from_access_token


class AllowAny(permissions.AllowAny):
    def has_permission(self, request, view):
        return True


class IsAuthenticated(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        user = get_user_from_access_token(self, request)
        if not user:
            return False
        else:
            return True


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
        requested_role = request.data.get("role", None)
        if requested_role is None:
            requested_role = "Customer"
        requested_user = get_user_from_access_token(self, request)
        if requested_user.is_admin:
            return True
        if requested_user.is_staff:
            if requested_role == "Customer":
                return True
        return False
