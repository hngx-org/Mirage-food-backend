from django.urls import path,re_path
from .views import UpdateUserDetailsView


urlpatterns = [
     path('users/<int:pk>/', UpdateUserDetailsView.as_view(), name='user-detail'),
]


