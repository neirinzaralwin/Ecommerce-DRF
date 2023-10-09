from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .serializers import UserSerializer


class UserCreate(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        user_serialzer = UserSerializer(data=request.data)
        if user_serialzer.is_valid():
            newuser = user_serialzer.save()
            return Response(
                {"success": True, "message": "successful", "data": user_serialzer.data},
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
