from django.urls import path
from . import views

urlpatterns = [
    path('get_balance/<int:organization_id>/', views.organization_balance, name='get_balance'),
]


