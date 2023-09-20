from django.contrib import admin
from django.urls import path, include
from . views import CreateFreeLunchAPIView
urlpatterns = [
    path('send_free_lunch',CreateFreeLunchAPIView.as_view(), name="free_lunch"),

]