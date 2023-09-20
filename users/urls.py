<<<<<<< HEAD
from django.urls import path
from .views import DeleteUserView

urlpatterns = [
    path('users/<int:id>/', DeleteUserView.as_view()),
=======
from django.urls import path, re_path, include

from .views import UserListViewSet

urlpatterns = [
    path('users/', UserListViewSet.as_view(), name='users-list'),
>>>>>>> 1729f3a5f3e94012b6cbf58fde706afda62051b6
]