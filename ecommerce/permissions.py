from rest_framework import permissions
from ecommerce.user.models import User


class IsAdminOrReadOnly(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        admin_permission = super().has_permission(request, view)  # is authenticated
        if not request.user.is_admin:
            return False
        return admin_permission or request.method == "GET"


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
