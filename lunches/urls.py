from django.contrib import admin
from django.urls import path, include
from . views import CreateFreeLunchAPIView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)
urlpatterns = [
    path('api/lunch/send',CreateFreeLunchAPIView.as_view(), name="free_lunch"),
    
    

]