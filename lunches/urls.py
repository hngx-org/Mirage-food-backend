from  django.urls import path
from .views import allFreeLunchesListView

urlpatterns = [
   path("lunch/all", allFreeLunchesListView.as_view(), name="lunch-list"), 
]