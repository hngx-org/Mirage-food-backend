from django.urls import path
from .views import OrganizationLunchWalletView

urlpatterns = [
    path('create/', OrganizationLunchWalletView.as_view(), name='create'),
]
