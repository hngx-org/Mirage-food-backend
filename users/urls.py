
from django.urls import path
from .views import UserRegistrationView

urlpatterns = [
    
    path('auth/user/signup/', UserRegistrationView.as_view(), name='user-signup'),
    
]
