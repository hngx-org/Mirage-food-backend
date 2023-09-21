<<<<<<< HEAD
from django.contrib import admin
from django.urls import path
from . views import CreateFreeLunchAPIView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)
urlpatterns = [
    path('api/lunch/send', CreateFreeLunchAPIView.as_view(), name='free_lunch' )
]
# from django.urls import path, re_path, include

# from . import views

# urlpatterns = [
#     path('lunch/<int:id>', views.get_a_lunch, name='get_a_free_lunch'),
# ]
=======
from  django.urls import path
from .views import allFreeLunchesListView

urlpatterns = [
   path("lunch/all", allFreeLunchesListView.as_view(), name="lunch-list"), 
]
>>>>>>> 5dec6a69ca57e6779e69eb9872c9c3600e6fc30f
