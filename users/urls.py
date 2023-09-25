from django.urls import path
from .views import(
    DeleteUserView,
    UserProfileView,
    UserAddBankAccountView,
    UserProfileUpdateView,
    UserProfilePictureUpdateView)
from django.urls import path
from .views import UserListViewSet

from .views import SearchUserView
from .views import UserRegistrationView, UserLoginView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)



urlpatterns = [
    path('user/all', UserListViewSet.as_view(), name='users-list'),
    path('user/<int:id>', UserProfileView.as_view(), name='user-profile'),
    path('user/<int:id>/bank', UserAddBankAccountView.as_view(), name='user-bank'),
    path('users/<int:id>', DeleteUserView.as_view()),
    path('user/search/<str:name_or_email>', SearchUserView.as_view(), name='search-users'),
    path('auth/user/signup', UserRegistrationView.as_view(), name='user-signup'),
    path('auth/login', UserLoginView.as_view(), name='user-login'),
    path('users/<int:pk>', UserProfileUpdateView.as_view(), name='user-update'),
    path('update-profile-picture/<int:pk>', UserProfilePictureUpdateView.as_view(), name='update-profile-picture'),


    
]
