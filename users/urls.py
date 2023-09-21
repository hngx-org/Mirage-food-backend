from django.urls import path
from .views import UserRetrieveUpdateSet

urlpatterns = [

path('users/<int:id>/', UserRetrieveUpdateSet.as_view(), name='user-retrieve-update-set'),
]
