from django.urls import path, re_path, include

from .views import UserListViewSet

urlpatterns = [
    path('users/', UserListViewSet.as_view(), name='users-list'),
]