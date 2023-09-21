from django.contrib import admin
from django.urls import path
from . views import CreateFreeLunchAPIView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)
urlpatterns = [
    path('api/users/<int:sender_id>/organizations/<int:organization_id>/lunches', CreateFreeLunchAPIView.as_view(), name='free_lunch' )
]
from django.urls import path, re_path, include

from . import views

urlpatterns = [
    path('lunch/<int:id>', views.get_a_lunch, name='get_a_free_lunch'),
]
