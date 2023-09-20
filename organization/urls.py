from django.urls import path

from . import views

urlpatterns = [
    path("create", views.OrganizationView.as_view()),
    path("invite/", views.OrganizationInviteView.as_view(), name="organization-invite"),
]
