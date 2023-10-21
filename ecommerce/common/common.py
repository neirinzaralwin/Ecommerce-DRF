from ecommerce.user.models import User
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
import datetime


def change_dict_key(dict, old_key, new_key, default_value=None):
    dict[new_key] = dict.pop(old_key, default_value)


def get_user_from_access_token(self, request):
    try:
        access_token = request.META.get("HTTP_AUTHORIZATION").split(" ")[1]
        decoded_token = JWTAuthentication.get_validated_token(
            self, raw_token=access_token
        )
        user_id = decoded_token["user_id"]
        user = User.manager.get(id=user_id)

        return user
    except:
        raise PermissionDenied("You have no permission.")


def file_location(instance, filename, **kwargs):
    ct = datetime.datetime.now()
    file_path = f"products/{ct.timestamp()}-{filename}"
    return file_path
