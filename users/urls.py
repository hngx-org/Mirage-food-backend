from django.urls import path
from .views import DeleteUserView
from django.urls import path
from .views import UserListViewSet, LoginView
from lunches.views import LunchDetailView
from .views import UserRegistrationView



urlpatterns = [
    path('organization/<int:org_id>/user/<int:user_id>', UserViewSet.as_view, name='get-org_user'),
    path('users/', UserListViewSet.as_view(), name='users-list'),
    path('users/login', LoginView.as_view()),
    path('users/<int:id>/', DeleteUserView.as_view()),
    path('users/<int:user_id>/lunches/<int:lunch_id>',LunchDetailView.as_view(),name='lunch-detail'),
    path('auth/user/signup/', UserRegistrationView.as_view(), name='user-signup'),
    
]
