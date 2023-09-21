<<<<<<< HEAD
<<<<<<< HEAD
from django.urls import path
from .views import DeleteUserView

urlpatterns = [
    path('users/<int:id>/', DeleteUserView.as_view()),
=======
from django.urls import path, re_path, include

=======
from django.urls import path
from .views import DeleteUserView
from django.urls import path
>>>>>>> 5dec6a69ca57e6779e69eb9872c9c3600e6fc30f
from .views import UserListViewSet
from lunches.views import LunchDetailView

urlpatterns = [
    path('users/', UserListViewSet.as_view(), name='users-list'),
<<<<<<< HEAD
>>>>>>> 1729f3a5f3e94012b6cbf58fde706afda62051b6
=======
    path('users/<int:id>/', DeleteUserView.as_view()),
    path('users/<int:user_id>/lunches/<int:lunch_id>',LunchDetailView.as_view(),name='lunch-detail'),
>>>>>>> 5dec6a69ca57e6779e69eb9872c9c3600e6fc30f
]