from django.contrib import admin
from django.urls import path
from .views import CreateFreeLunchAPIView, allFreeLunchesListView
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path('lunch/send', CreateFreeLunchAPIView.as_view(), name='free_lunch' ),
    # path('lunch/<int:id>', views.get_a_lunch, name='get_a_free_lunch'),
    path("lunch/all", allFreeLunchesListView.as_view(), name="lunch-list"), 
]