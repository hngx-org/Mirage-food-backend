from django.urls import path
from .views import LoginView
from .views import DeleteUserView
from django.urls import path
from .views import UserListViewSet, LoginView, SearchUserView, DeleteUserView, UserRegistrationView, UpdateUserBankDetailsView
from lunches.views import LunchDetailView


urlpatterns = [
    path('users/all', UserListViewSet.as_view(), name='users-list'),
    path('users/<int:id>/', DeleteUserView.as_view()),
    path('users/<int:user_id>/lunches/<int:lunch_id>',LunchDetailView.as_view(),name='lunch-detail'),
    path('user/search/<str:name_or_email>/', SearchUserView.as_view(), name='search-users'),
    path('auth/user/signup/', UserRegistrationView.as_view(), name='user-signup'),
    path('auth/login/', LoginView.as_view(), name='login'),

    # URL pattern to update user bank details
    path('users/<int:id>/bank-details/', UpdateUserBankDetailsView, name='user-bank-details')

    
]
