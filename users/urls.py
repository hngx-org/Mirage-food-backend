from django.urls import path
from .views import DeleteUserView
from django.urls import path
from .views import UserListViewSet
from lunches.views import LunchDetailView
from . import views

urlpatterns = [
    path('organization/<org_id>/user/<user_id>', views.get_user, name='get_user'),
    path('users/', UserListViewSet.as_view(), name='users-list'),
    path('users/<int:id>/', DeleteUserView.as_view()),
    path('users/<int:user_id>/lunches/<int:lunch_id>',LunchDetailView.as_view(),name='lunch-detail'),
]