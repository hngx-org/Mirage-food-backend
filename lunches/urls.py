from django.urls import path
from . import views

urlpatterns = [
    path('lunch/<int:id>', views.delete_free_lunch),
]