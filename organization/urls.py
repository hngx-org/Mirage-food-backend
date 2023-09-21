from . import views
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import OrganizationAPI

app_name = "organization"

router = DefaultRouter()
router.register("", OrganizationAPI, basename="organization")

urlpatterns = [
    path("", include(router.urls)),
    path('organization/<int:org_id>/user/<int:user_id>', views.get_user, name='get_user'),
    path("organization/<int:pk>/",OrganizationAPI.as_view({"put": "update"}), name="organization"),
    path("organization/invitations", views.ListInvitesView.as_view()),
    path('users/<int:user_id>/organizations/<int:org_id>', views.get_organization, name='get-organization'),
    path('get_balance/<int:organization_id>/', views.organization_balance, name='get_balance'),


]
