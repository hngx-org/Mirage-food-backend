from django.contrib import admin
from django.urls import path
from . views import CreateFreeLunchAPIView, UpdateLunch
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)
urlpatterns = [
    path('api/lunch/send',CreateFreeLunchAPIView.as_view(), name="free_lunch"),
    path('update-lunch-wallet', UpdateLunch.as_view(), name='update-lunch-wallet'),
]