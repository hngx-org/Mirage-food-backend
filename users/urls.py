from django.urls import path
from .views import LoginView
from .views import DeleteUserView
from django.urls import path
from .views import UserListViewSet, LoginView
from lunches.views import LunchDetailView
from .views import SearchUserView
from .views import UserRegistrationView, UserDetailView
from .views import LogoutView


from .views import (
    RequestPasswordResetView,
    ConfirmResetTokenView,
    PasswordResetView,
    RedeemLunchView
)

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('users/all', UserListViewSet.as_view(), name='users-list'),
    path('users/<int:id>', DeleteUserView.as_view()),
    path('users/<int:user_id>/lunches/<int:lunch_id>',LunchDetailView.as_view(),name='lunch-detail'),
    path('user/search/<str:name_or_email>', SearchUserView.as_view(), name='search-users'),
    path('auth/user/signup', UserRegistrationView.as_view(), name='user-signup'),
    # path('auth/login/', LoginView.as_view(), name='login'),
  
    path('auth/login/', TokenObtainPairView.as_view(), name='login'),

    path('user/<str:email>/request-password-reset', 
        RequestPasswordResetView.as_view(), name='request-password-reset'),
    path('user/confirm-reset-token/<str:email>/<str:token>', 
        ConfirmResetTokenView.as_view(), name='confirm-password-reset'),
    path('user/password-reset/<str:token>', 
        PasswordResetView.as_view(), name='password-reset')

    path('auth/login', TokenObtainPairView.as_view(), name='login'),
    path('auth/login/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/logout', LogoutView.as_view(), name='logout'),
    path('user/redeem', RedeemLunchView.as_view(), name='redeem-lunch'),

]
