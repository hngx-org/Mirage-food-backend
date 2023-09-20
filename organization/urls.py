from django.urls import path
from . import views

urlpatterns = [
    path("users/<int:user_pk>/organisations/<int:org_pk>/invitations",
         views.AllInvites.as_view())
]
