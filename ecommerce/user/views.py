from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from .serializers import UserSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import User, Customer
from django.contrib.auth.hashers import make_password
from ecommerce.permissions import IsAdminInheritStaff


class UserCreate(APIView):
    permission_classes = [IsAdminInheritStaff]

    def post(self, request):
        user_serialzer = UserSerializer(data=request.data)
        if user_serialzer.is_valid():
            newuser = user_serialzer.save()
            return Response(
                {
                    "success": True,
                    "message": "successful",
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


class UserInfoFromToken(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    user_model = User
    serializer_class = UserSerializer

    def get(self, request):
        access_token = request.META.get("HTTP_AUTHORIZATION").split(" ")[1]
        decoded_token = JWTAuthentication.get_validated_token(
            self, raw_token=access_token
        )
        user_id = decoded_token["user_id"]
        user = self.user_model.manager.get(id=user_id)
        if user:
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


class UserLogin(TokenObtainPairView):
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
            if user.check_password(password):
                response = super().post(request, *args, **kwargs)
                print(f" response token {response.data}")
                return Response(
                    {
                        "success": True,
                        "message": "successfully login",
                        "refresh_token": response.data.get("refresh"),
                        "access_token": response.data.get("access"),
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
