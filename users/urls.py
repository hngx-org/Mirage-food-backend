from django.urls import path
from users import views

urlpatterns = [
    path('users/:id/organizations/:id/employees?employee=id', views.get_user, name='get_user'),
]