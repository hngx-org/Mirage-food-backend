from django.urls import path
from . import views

urlpatterns = [
    path('api/users/<int:id>/lunches', views.user_lunch_list, name='user-lunch-list'),
    path('api/lunch/all', views.allFreeLunchesListView.as_view(), name='lunch-list'),
    path('api/lunch/<int:user_id>/<int:lunch_id>', views.LunchDetailView.as_view(), name='lunch-detail'),
    path('api/lunch/<int:id>/delete', views.delete_free_lunch, name='delete-free-lunch'),
    path('api/lunch/<int:id>/update', views.update_free_lunch, name='update-free-lunch'),
]

