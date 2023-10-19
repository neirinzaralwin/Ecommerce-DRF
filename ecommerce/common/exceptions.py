from rest_framework.views import exception_handler
from rest_framework.response import Response
from ecommerce.common.common import change_dict_key


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    response.data["success"] = False
    change_dict_key(response.data, "detail", "message")

    return response
