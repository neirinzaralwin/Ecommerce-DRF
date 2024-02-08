from django.urls import include, path
from .views import ContactViewSet, ContactTypeView, AboutUsViewSet

app_name = "contacts"

contact_view = ContactViewSet.as_view(
    {"get": "list", "post": "create", "patch": "update", "delete": "destroy"}
)
about_us_view = AboutUsViewSet.as_view({"get": "retrieve", "patch": "update"})


urlpatterns = [
    path("contacts/", contact_view, name="contact-list"),
    path("contacts/<int:pk>/", contact_view, name="contact-delete-update"),
    path("contacts/delete-all/", contact_view, name="contact-delete-all"),
    path("contacts/create/", contact_view, name="contact-create"),
    path("contacts/types/", ContactTypeView.as_view(), name="contact-types"),
    # about us description
    path("contacts/about-us/", about_us_view, name="about-us"),
]
