from django.urls import path
from . import views

urlpatterns = [

    path('api/users/<int:id>/lunches', views.user_lunch_list, name='user-lunch-list'),
]
