from django.urls import path

from .views import UserRetrieveUpdateSet
from .views import DeleteUserView
from django.urls import path
from .views import UserListViewSet
from lunches.views import LunchDetailView

urlpatterns = [
    path('users/', UserListViewSet.as_view(), name='users-list'),
    path('users/<int:id>/', UserRetrieveUpdateSet.as_view(), name='user-retrieve-update-set'),
    path('users/<int:id>/', DeleteUserView.as_view()),
    path('users/<int:user_id>/lunches/<int:lunch_id>',LunchDetailView.as_view(),name='lunch-detail'),
]

