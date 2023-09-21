from django.urls import path, re_path, include

from .views import UserListViewSet

urlpatterns = [
    # URL pattern for GET all users should be here
    path('users/<int:pk>', UserListViewSet.as_view(), name='users-list'),
]