from django.urls import path
from .views import UserRetrieveUpdateSet

urlpatterns = [

path('users/<int:pk>/', UserRetrieveUpdateSet.as_view(), name='user-retrieve-update-set'),
]
