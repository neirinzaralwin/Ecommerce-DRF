from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from ecommerce.permissions import (
    IsAdminInheritStaff,
    IsAdminOrStaff,
    IsAuthenticated,
    AllowAny,
)
from ecommerce.user.managers.jwt_manager import get_user_from_access_token
from ecommerce.common.custom_pagination import CustomPagination, PaginationHandlerMixin
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from .models import OrderStatus, Order
from .serializers import OrderSerializer
from ecommerce.cart.models import Cart, CartSession
from ecommerce.cart.serializers import CartSerializer, CartSessionSerializer


class AllOrderAdminView(APIView, PaginationHandlerMixin):
    pagination_class = CustomPagination
    permission_classes = [IsAdminOrStaff]

    def get(self, request):
        try:
            orders = Order.objects.all()
            return self.custom_paginated_response(
                serializer_class=OrderSerializer, queryset=orders
            )

        except Exception as e:
            return Response(
                {
                    "success": False,
                    "message": str(e),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


class OrderNow(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            user = get_user_from_access_token(self, request)
            cart_session = get_object_or_404(CartSession, user=user)

            if not cart_session.carts.exists():
                raise ValueError("Cart is empty")

            order = Order.objects.create(user=user, status=OrderStatus.PENDING)
            order.items.set(cart_session.carts.all())
            order.save()
            cart_session.carts.clear()
            cart_session.save()
            serializer = OrderSerializer(order)

            return Response(
                {
                    "success": True,
                    "message": "Ordered successfully",
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response(
                {
                    "success": False,
                    "message": str(e),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
