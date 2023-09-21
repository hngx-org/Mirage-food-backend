from django.urls import path
from .views import DeleteUserView
<<<<<<< Updated upstream
from django.urls import path
from .views import UserListViewSet


urlpatterns = [
    path('users/', UserListViewSet.as_view(), name='users-list'),
=======

urlpatterns = [
>>>>>>> Stashed changes
    path('users/<int:id>/', DeleteUserView.as_view()),
]