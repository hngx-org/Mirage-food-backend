from django.urls import path
from .views import LoginView
from .views import RetrieveDeleteUserView
from django.urls import path
from .views import UserListViewSet, LoginView
from .views import SearchUserView
from .views import UserRegistrationView
from .views import RetrieveDeleteUserView, UserAddBankAccountView, ApiStatusView, UserUpdateView, UserProfilePictureUpdateView
from .views import change_password
from .views import PasswordReset, ResetPasswordAPI



from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('user/all', UserListViewSet.as_view(), name='users-list'),
    path('user/<int:id>', RetrieveDeleteUserView.as_view()),
    path('user/<int:id>/bank', UserAddBankAccountView.as_view(), name='user-bank'),
    path('user/search/<str:name_or_email>', SearchUserView.as_view(), name='search-users'),
    path('auth/user/signup', UserRegistrationView.as_view(), name='user-signup'),
    path('auth/login', TokenObtainPairView.as_view(), name='login'),
    path('status', ApiStatusView.as_view(), name='ApiStatus'),
    path('change_password/', change_password, name='change_password'),
    path(
        "user/reset_password",
        PasswordReset.as_view(),
        name="request-password-reset",
    ),
    path(
        "user/password-reset/<str:encoded_pk>/<str:token>/",
        ResetPasswordAPI.as_view(),
        name="reset-password",
    ),
    path('user/<int:pk>', UserUpdateView.as_view(), name='user-update'),
    path('update-profile-picture/<int:pk>', UserProfilePictureUpdateView.as_view(), name='update-profile-picture')

    
]
