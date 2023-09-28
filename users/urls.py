from django.urls import path
from .views import(
    DeleteUserView,
    UserProfileView,
    UserAddBankAccountView,
    ApiStatusView)
from django.urls import path
from .views import UserListViewSet
from .views import SearchUserView
from .views import UserRegistrationView,  UserLoginView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,)
from .views import change_password
from .views import PasswordReset, ResetPasswordAPI
from .views import LogoutView



urlpatterns = [
    path('user/all', UserListViewSet.as_view(), name='users-list'),
    path('user/<int:id>', UserProfileView.as_view(), name='user-profile'),
    path('user/<int:id>/bank', UserAddBankAccountView.as_view(), name='user-bank'),
    path('user/<int:id>', DeleteUserView.as_view()),
    path('user/search/<str:name_or_email>', SearchUserView.as_view(), name='search-users'),
    path('auth/user/signup', UserRegistrationView.as_view(), name='user-signup'),
    path('auth/login', UserLoginView.as_view(), name='user-login'),  
    path('status', ApiStatusView.as_view(), name='ApiStatus'),
    path('user/change_password', change_password, name='change_password'),
    path(
        "user/reset_password",
        PasswordReset.as_view(),
        name="request-password-reset",),
    path(
        "user/password-reset/<str:encoded_pk>/<str:token>",
        ResetPasswordAPI.as_view(),
        name="reset-password",
    ),
    path('auth/logout', LogoutView.as_view(), name='logout'),

]
