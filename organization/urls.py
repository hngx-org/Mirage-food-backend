from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views  # Correct import path

# Create a router for your viewsets
router = DefaultRouter()
router.register(r'invitations', views.InvitationViewSet)  # Correct viewset import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/<int:user_id>/organizations/<int:org_id>/', include(router.urls)),
]
