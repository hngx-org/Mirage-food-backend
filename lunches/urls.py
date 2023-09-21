from django.urls import path
<<<<<<< HEAD
from . import views

urlpatterns = [
    path('api/users/<int:id>/lunches', views.user_lunch_list, name='user-lunch-list'),
    path('api/lunch/all', views.allFreeLunchesListView.as_view(), name='lunch-list'),
    path('api/lunch/<int:user_id>/<int:lunch_id>', views.LunchDetailView.as_view(), name='lunch-detail'),
    path('api/lunch/<int:id>/delete', views.delete_free_lunch, name='delete-free-lunch'),
    path('api/lunch/<int:id>/update', views.update_free_lunch, name='update-free-lunch'),
]

=======
from .views import CreateFreeLunchAPIView, allFreeLunchesListView
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path('lunch/send', CreateFreeLunchAPIView.as_view(), name='free_lunch' ),
    path('update_lunch/<int:id>/', views.update_free_lunch, name='update_free_lunch'),
    path("lunch/all", allFreeLunchesListView.as_view(), name="lunch-list"), 
    path('lunch/<int:id>', views.delete_free_lunch),

 
]
>>>>>>> 61f328dee497fbcbfd352ac01075f5d666a17e4b
