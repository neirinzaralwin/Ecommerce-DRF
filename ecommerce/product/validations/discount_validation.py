from rest_framework import status
from rest_framework.response import Response


def validateDiscountPercentage(percentage):
    if percentage > 100 or percentage < 0:
        print("invalid percentage")
        return False
    return True
