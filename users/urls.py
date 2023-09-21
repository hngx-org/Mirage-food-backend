from django.urls import path
<<<<<<< HEAD
from .views import UserRetrieveUpdateSet

urlpatterns = [

path('users/<int:id>/', UserRetrieveUpdateSet.as_view(), name='user-retrieve-update-set'),
]
=======
from .views import DeleteUserView
from django.urls import path
from .views import UserListViewSet
from lunches.views import LunchDetailView

urlpatterns = [
    path('users/', UserListViewSet.as_view(), name='users-list'),
    path('users/<int:id>/', DeleteUserView.as_view()),
    path('users/<int:user_id>/lunches/<int:lunch_id>',LunchDetailView.as_view(),name='lunch-detail'),
]
>>>>>>> 5dec6a69ca57e6779e69eb9872c9c3600e6fc30f
