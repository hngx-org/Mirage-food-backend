from django.urls import path
from .views import WithdrawalUpdateView

urlpatterns = [
    path('withdrawals/<int:pk>/', WithdrawalUpdateView.as_view(), name='withdrawal-update'),
]