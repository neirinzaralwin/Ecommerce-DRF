from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer
from ecommerce.common.custom_pagination import CustomPagination, PaginationHandlerMixin
from .managers.jwt_manager import create_jwt_token, get_user_from_access_token

# from rest_framework_simplejwt.views import TokenObtainPairView
# from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import User, Customer
from .serializers import UserSerializer
from django.contrib.auth.hashers import make_password
from ecommerce.permissions import (
    IsAdminInheritStaff,
    IsAdminOrStaff,
    IsAuthenticated,
    AllowAny,
)


class UserCreate(APIView):
    permission_classes = [IsAdminInheritStaff]

    def post(self, request):
        user_serialzer = UserSerializer(data=request.data)
        if user_serialzer.is_valid():
            newuser = user_serialzer.save()
            refresh_token, access_token = create_jwt_token(user=newuser)
            return Response(
                {
                    "success": True,
                    "message": "Registration successful",
                    "refresh_token": refresh_token,
                    "access_token": access_token,
                    "data": user_serialzer.data,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {
                "success": False,
                "message": "User registration failed",
                "error": user_serialzer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )


class UserListView(APIView, PaginationHandlerMixin):
    pagination_class = CustomPagination
    permission_classes = [IsAdminOrStaff]

    def get(self, request):
        users = User.manager.all()
        return self.custom_paginated_response(
            serializer_class=UserSerializer, queryset=users
        )


class UserInfoFromToken(APIView):
    permission_classes = [IsAuthenticated]
    user_model = User
    serializer_class = UserSerializer

    def get(self, request):
        user = get_user_from_access_token(self, request)
        if user is not None:
            serializer = self.serializer_class(instance=user)
            return Response(
                {
                    "success": True,
                    "message": "successfully get user information",
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"success": False, "message": "User does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )


# class UserLogin(TokenObtainPairView):
class UserLogin(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        phone = request.data.get("phone")
        password = request.data.get("password")
        try:
            user = User.manager.get(phone=phone)
            serializer = UserSerializer(instance=user)
            if not user.is_active:
                return Response(
                    {"success": False, "message": "Your account is inactive"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if user.check_password(password + user.salt):
                # response = super().post(request, *args, **kwargs)
                refresh_token, access_token = create_jwt_token(user=user)
                return Response(
                    {
                        "success": True,
                        "message": "successfully login",
                        "refresh_token": refresh_token,
                        "access_token": access_token,
                        "data": serializer.data,
                    },
                    status=status.HTTP_200_OK,
                )
            return Response(
                {"success": False, "message": "Wrong password"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except User.DoesNotExist:
            return Response(
                {"success": False, "message": "User does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )
