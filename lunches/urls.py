from django.urls import path
from .views import CreateFreeLunchAPIView, allFreeLunchesListView
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path('lunch/send', CreateFreeLunchAPIView.as_view(), name='free_lunch' ),
    path('update_lunch/<int:id>/', views.update_free_lunch, name='update_free_lunch'),
    path("lunch/all", allFreeLunchesListView.as_view(), name="lunch-list"), 
 
]