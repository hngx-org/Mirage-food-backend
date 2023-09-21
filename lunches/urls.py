<<<<<<< HEAD
from django.urls import path
from . import views

urlpatterns = [

    path('api/users/<int:id>/lunches', views.user_lunch_list, name='user-lunch-list'),
]
=======
from  django.urls import path
from .views import allFreeLunchesListView

urlpatterns = [
   path("lunch/all", allFreeLunchesListView.as_view(), name="lunch-list"), 
]
>>>>>>> 5dec6a69ca57e6779e69eb9872c9c3600e6fc30f
