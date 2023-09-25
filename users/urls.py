from django.urls import path
from .views import LoginView
from .views import DeleteUserView, UserProfileView, UserAddBankAccountView, UserUpdateView, UserProfilePictureUpdateView
from django.urls import path
from .views import UserListViewSet, LoginView

from .views import SearchUserView
from .views import UserRegistrationView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('user/all', UserListViewSet.as_view(), name='users-list'),
    path('user/<int:id>', UserProfileView.as_view(), name='user-profile'),
    path('user/<int:id>/bank', UserAddBankAccountView.as_view(), name='user-bank'),
    path('users/<int:id>', DeleteUserView.as_view()),
    #path('users/<int:user_id>/lunches/<int:lunch_id>',LunchDetailView.as_view(),name='lunch-detail'),
    path('user/search/<str:name_or_email>', SearchUserView.as_view(), name='search-users'),
    path('auth/user/signup', UserRegistrationView.as_view(), name='user-signup'),
    # path('auth/login/', LoginView.as_view(), name='login')
    path('auth/login', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('updateuser/<int:pk>', UserUpdateView.as_view(), name='user-update'),
    path('update-profile-picture/<int:pk>', UserProfilePictureUpdateView.as_view(), name='update-profile-picture'),


    
]
