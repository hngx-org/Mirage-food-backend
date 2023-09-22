from django.urls import path
from .views import LoginView
from .views import DeleteUserView
from django.urls import path
from .views import UserListViewSet, LoginView
from lunches.views import LunchDetailView
from .views import SearchUserView
from .views import UserRegistrationView


urlpatterns = [
    path('users/', UserListViewSet.as_view(), name='users-list'),
    path('users/<int:id>/', DeleteUserView.as_view()),
    path('users/<int:user_id>/lunches/<int:lunch_id>',LunchDetailView.as_view(),name='lunch-detail'),
    path('search/<str:name_or_email>/', SearchUserView.as_view(), name='search-users'),
    path('auth/user/signup/', UserRegistrationView.as_view(), name='user-signup'),
    path('auth/login/', LoginView.as_view(), name='login')

    
]
