from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from organization.views import InvitationViewSet

router = DefaultRouter()
router.register(r'invitations', InvitationViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    # Add other URL patterns as needed
]
