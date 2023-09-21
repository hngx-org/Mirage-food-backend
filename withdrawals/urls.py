from django.urls import path
<<<<<<< HEAD
from .views import WithdrawalUpdateView

urlpatterns = [
=======
from .views import WithdrawalUpdateView, LunchWithdrawalCreateView

urlpatterns = [
    path('withdrawal/request', LunchWithdrawalCreateView.as_view(), name='withdrawal-create'),
>>>>>>> 61f328dee497fbcbfd352ac01075f5d666a17e4b
    path('withdrawals/<int:pk>/', WithdrawalUpdateView.as_view(), name='withdrawal-update'),
]