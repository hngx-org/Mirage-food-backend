from django.urls import path
from .views import LunchWithdrawalCreateView

urlpatterns = [
    path('withdrawal/request', LunchWithdrawalCreateView.as_view(), name='withdrawal-create'),
      
]