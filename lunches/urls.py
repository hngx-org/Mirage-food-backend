from django.urls import path 
from .views import allFreeLunchesListView
from . import views 

urlpatterns = [
    path('update_lunch/<int:id>/', views.update_free_lunch, name='update_free_lunch'),
    path("lunch/all", allFreeLunchesListView.as_view(), name="lunch-list"), 
]