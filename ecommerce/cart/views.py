from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, status, generics
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from ecommerce.common.common import get_user_from_access_token
from ecommerce.product.models import Product
from ecommerce.cart.models import Cart, CartSession
from ecommerce.cart.serializers import CartSerializer, CartSessionSerializer


# Create your views here.
class CartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user = get_user_from_access_token(self, request)
            cart_session, created = CartSession.objects.get_or_create(user=user)
            serializer = CartSessionSerializer(cart_session)

            return Response(
                {
                    "success": True,
                    "message": "Successful",
                    "data": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )

        except Exception as e:
            return Response(
                {
                    "success": False,
                    "message": str(e),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

    def post(self, request):
        try:
            product_id = request.data.pop("product_id", None)
            quantity = request.data.pop("quantity", None)
            user = get_user_from_access_token(self, request)
            product = get_object_or_404(Product, id=product_id)
            cart = Cart.objects.create(product=product, quantity=quantity)
            cart_session, created = CartSession.objects.get_or_create(user=user)
            cart, _ = cart_session.carts.get_or_create(product=product)
            cart.quantity += quantity
            cart.save()
            serializer = CartSessionSerializer(cart_session)

            return Response(
                {
                    "success": True,
                    "message": "Successfully added",
                    "data": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            return Response(
                {
                    "success": False,
                    "message": str(e),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

    def delete(self, request):
        try:
            cart_id = request.data.pop("cart_id", None)
            if cart_id is None:
                return Response(
                    {
                        "success": False,
                        "message": "Please enter cart_id",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            user = get_user_from_access_token(self, request)
            cart_session = get_object_or_404(CartSession, user=user)
            serializer = CartSessionSerializer(cart_session)
            cart = Cart.objects.get(id=cart_id)
            cart.delete()

            return Response(
                {
                    "success": True,
                    "message": "Successfully deleted",
                    "data": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            return Response(
                {
                    "success": False,
                    "message": str(e),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


class DeleteAllCart(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        try:
            user = get_user_from_access_token(self, request)
            cart_session = get_object_or_404(CartSession, user=user)
            cart_session.carts.clear()
            cart_session.save()
            serializer = CartSessionSerializer(cart_session)
            return Response(
                {
                    "success": True,
                    "message": "Successfully deleted",
                    "data": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            return Response(
                {
                    "success": False,
                    "message": str(e),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
