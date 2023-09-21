from django.urls import path
from .views import DeleteUserView
from django.urls import path
from .views import UserListViewSet


urlpatterns = [
    path('users/', UserListViewSet.as_view(), name='users-list'),
    path('users/<int:id>/', DeleteUserView.as_view()),
]