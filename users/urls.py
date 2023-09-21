from django.urls import path
<<<<<<< HEAD
from . import views
from .views import UserListViewSet
from .views import DeleteUserView
=======
from .views import DeleteUserView
from django.urls import path
from .views import UserListViewSet, LoginView
from lunches.views import LunchDetailView


>>>>>>> 61f328dee497fbcbfd352ac01075f5d666a17e4b
urlpatterns = [
    path('users/', UserListViewSet.as_view(), name='users-list'),
    path('users/login', LoginView.as_view()),
    path('users/<int:id>/', DeleteUserView.as_view()),
<<<<<<< HEAD
    path('users/<int:user_id>/lunches/<int:lunch_id>', LunchDetailView.as_view(), name='lunch-detail'),
]

=======
    path('users/<int:user_id>/lunches/<int:lunch_id>',LunchDetailView.as_view(), name='lunch-detail'),
]
>>>>>>> 61f328dee497fbcbfd352ac01075f5d666a17e4b
