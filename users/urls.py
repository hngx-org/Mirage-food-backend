from django.urls import path
from .views import LoginView
from .views import RetrieveDeleteUserView
from django.urls import path
from .views import UserListViewSet, LoginView
from .views import SearchUserView
from .views import UserRegistrationView
from .views import RetrieveDeleteUserView, UserAddBankAccountView

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
     path('auth/login', TokenObtainPairView.as_view(), name='login')
    
]
