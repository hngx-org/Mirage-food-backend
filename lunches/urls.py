<<<<<<< HEAD
from django.urls import path 
from . import views 

urlpatterns = [
    path('update_lunch/<int:id>/', views.update_free_lunch, name='update_free_lunch'),
=======
from  django.urls import path
from .views import allFreeLunchesListView

urlpatterns = [
   path("lunch/all", allFreeLunchesListView.as_view(), name="lunch-list"), 
>>>>>>> 5dec6a69ca57e6779e69eb9872c9c3600e6fc30f
]