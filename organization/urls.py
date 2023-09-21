from django.urls import path
from . import views
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import OrganizationAPI

app_name = "organization"

router = DefaultRouter()
router.register("", OrganizationAPI, basename="organization")

urlpatterns = [
    path("", include(router.urls)),
    path("organization/<int:pk>/", OrganizationAPI.as_view({"put": "update"}), name="organization"),
    path('users/<int:user_id>/organizations/<int:org_id>', views.get_organization, name='get-organization'),
    path('get_balance/<int:organization_id>/', views.organization_balance, name='get_balance'),


]
