import jwt, datetime
from ecommerce.user.models import User
from rest_framework.exceptions import PermissionDenied


def create_jwt_token(user: User):
    now = datetime.datetime.utcnow()
    access_payload = {
        "id": user.id,
        "exp": now + datetime.timedelta(days=15),
        "iat": now,
    }
    refresh_payload = {
        "id": user.id,
        "exp": now + datetime.timedelta(days=90),
        "iat": now,
    }
    refresh_token = jwt.encode(access_payload, "secret", algorithm="HS256")
    access_token = jwt.encode(refresh_payload, "secret", algorithm="HS256")
    return refresh_token, access_token


def get_user_from_access_token(self, request):
    try:
        prefix = request.META.get("HTTP_AUTHORIZATION").split(" ")[0]
        if prefix != "Bearer":
            raise ValueError("We need bearer authentication")
        access_token = request.META.get("HTTP_AUTHORIZATION").split(" ")[1]
        if not access_token:
            raise PermissionDenied("No access token provided.")
        payload = jwt.decode(access_token, "secret", algorithms=["HS256"])
        user = User.manager.get(id=payload["id"])
        if not user:
            raise PermissionDenied("User does not exist.")
        return user
    except Exception as e:
        print(e)
        raise PermissionDenied("You have no permission.")
