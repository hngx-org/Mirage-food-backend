from  django.urls import path
from .views import allFreeLunchesListView

urlpatterns = [
   path("all", allFreeLunchesListView.as_view(), name="lunch-list"), 
]