from django.urls import path 
from . import views 

urlpatterns = [
    path('update_lunch/<int:id>/', views.update_free_lunch, name='update_free_lunch'),
]