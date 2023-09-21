from django.urls import path
from .views import DeleteUserView, UserListViewSet

urlpatterns = [
    path('users/<int:id>/', DeleteUserView.as_view()),
    path('users/', UserListViewSet.as_view(), name='users-list'),
]