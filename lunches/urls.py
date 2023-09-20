from django.contrib import admin
from django.urls import path
from .views import SendFreeLunch

urlpatterns = [
    path('api/users/<int:sender_id>/organizations/<int:organization_id>/lunches', SendFreeLunch.as_view(), name='send-free-lunch'),
]