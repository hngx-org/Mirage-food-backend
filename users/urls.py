from django.urls import path
from .views import UserRetrieveUpdateSet

urlpatterns = [
# path('users/', UserListViewSet.as_view(), name='user-list'),
path('users/<int:pk>/', UserRetrieveUpdateSet.as_view(), name='user-retrieve-update-set'),
]
