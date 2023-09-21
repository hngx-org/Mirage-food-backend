from django.urls import path
from . import views
from .views import UserListViewSet
from .views import DeleteUserView
urlpatterns = [
    path('users/', UserListViewSet.as_view(), name='users-list'),
    path('users/<int:id>/', DeleteUserView.as_view()),
    path('users/<int:user_id>/lunches/<int:lunch_id>', LunchDetailView.as_view(), name='lunch-detail'),
]

