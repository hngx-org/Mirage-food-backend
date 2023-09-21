from django.contrib import admin
from django.urls import path, include

from rest_framework.routers import DefaultRouter
from organization.views import InvitationViewSet

router = DefaultRouter()
router.register(r'invitations', InvitationViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('users/', include(router.urls)),

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('organization.urls')),
    path('api/', include('users.urls')),
    path('api/', include('lunches.urls')),


    # Add other URL patterns as needed
]
