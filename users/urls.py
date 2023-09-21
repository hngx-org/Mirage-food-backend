from django.urls import path
from .views import UserSignupView

urlpatterns = [
    path('user/auth/signup/', UserSignupView.as_view(), name='user-signup'),
]
