from django.urls import path
from . import views

urlpatterns = [
    path("invitations", views.ListInvitesView.as_view())
]
