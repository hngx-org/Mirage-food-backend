from django.urls import path
from .views import DeleteUserView

urlpatterns = [
    path('users/<int:id>/', DeleteUserView.as_view()),
]
