from django.urls import path, re_path, include

from .views import UserListViewSet

urlpatterns = [
    # URL pattern for GET user details should be here
    path('users/<int:pk>', UserListViewSet.as_view(), name='users-list'),
]