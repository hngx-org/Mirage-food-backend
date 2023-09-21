from . import views
from .views import DeleteUserView
from django.urls import path
from .views import UserListViewSet, LoginView
from lunches.views import LunchDetailView


urlpatterns = [
    path('users/', UserListViewSet.as_view(), name='users-list'),
    path('users/login', LoginView.as_view()),
    path('users/<int:id>/', DeleteUserView.as_view()),
    path('users/<int:user_id>/lunches/<int:lunch_id>', LunchDetailView.as_view(), name='lunch-detail'),
]
