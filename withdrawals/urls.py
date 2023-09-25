from django.urls import path
from .views import WithdrawalUpdateView, WithdrawalCreateView

urlpatterns = [
    path('withdrawal/request', WithdrawalCreateView.as_view(), name='withdrawal-create'),
    path('withdrawals/<int:pk>', WithdrawalUpdateView.as_view(), name='withdrawal-update'),
]