
from django.urls import path
from .views import organization_balance

urlpatterns = [
    path('get_balance/<int:organization_id>/', organization_balance.as_view(), name='get_balance'),
]


 