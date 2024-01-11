from django.shortcuts import get_object_or_404
from ecommerce.permissions import (
    IsAdminInheritStaff,
    IsAdminOrStaff,
    IsAuthenticated,
    AllowAny,
)
from ecommerce.contact_us.models import Contact, ContactType
from ecommerce.contact_us.serializers import ContactSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView


class ContactTypeView(APIView):
    permission_classes = [IsAdminOrStaff]

    def get(self, request):
        contactTypeList = [choice[0] for choice in ContactType.choices]
        return Response({"data": sorted(contactTypeList)}, status=status.HTTP_200_OK)


class ContactViewSet(viewsets.ViewSet):
    permission_classes = [IsAdminOrStaff]
    queryset = Contact.objects.all()

    def list(self, request):
        queryset = Contact.objects.all()
        serializer = ContactSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        contact = get_object_or_404(Contact, pk=pk)
        serializer = ContactSerializer(contact, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        try:
            if pk is not None:
                contact = self.queryset.get(pk=pk)
                contact.delete()
                return Response(
                    {"message": "Contact deleted successfully"},
                    status=status.HTTP_200_OK,
                )
            else:
                Contact.objects.all().delete()
                return Response(
                    {"message": "All contacts deleted successfully"},
                    status=status.HTTP_200_OK,
                )
        except Contact.DoesNotExist:
            return Response(
                {"error": "Contact doesn't exist"},
                status=status.HTTP_404_NOT_FOUND,
            )
