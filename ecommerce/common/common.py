from ecommerce.user.models import User
from rest_framework.response import Response
import datetime


def change_dict_key(dict, old_key, new_key, default_value=None):
    dict[new_key] = dict.pop(old_key, default_value)


def file_location(instance, filename, **kwargs):
    ct = datetime.datetime.now()
    file_path = f"products/{ct.timestamp()}-{filename}"
    return file_path
