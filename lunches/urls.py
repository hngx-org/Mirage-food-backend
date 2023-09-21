from django.contrib import admin
from django.urls import path
from . views import CreateFreeLunchAPIView, UpdateWalletAPIView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('api/lunch/send', CreateFreeLunchAPIView.as_view(), name='free_lunch' ),
    path('api/organization/wallet/update',UpdateWalletAPIView.as_view(), name='free_lunch' ),

]
# from django.urls import path, re_path, include

# from . import views

# urlpatterns = [
#     path('lunch/<int:id>', views.get_a_lunch, name='get_a_free_lunch'),
# ]
