from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from lunches.views import UpdateLunch

urlpatterns = [
    path('update-lunch-wallet', UpdateLunch.as_view(), name='update-lunch-wallet'),
]