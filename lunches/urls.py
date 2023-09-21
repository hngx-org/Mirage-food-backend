from django.contrib import admin
from django.urls import path
from . views import CreateFreeLunchAPIView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)
urlpatterns = [
    path('api/users/<int:sender_id>/organizations/<int:organization_id>/lunches', CreateFreeLunchAPIView.as_view(), name='free_lunch' )
]