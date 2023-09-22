from django.urls import path
from .views import OrganizationLunchWalletView
from . import views
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import OrganizationAPI, UserOrganizationAPI, DeleteOrganizationView

app_name = "organization"

router = DefaultRouter()
router.register("", OrganizationAPI, basename="organization")

urlpatterns = [
    # path("", include(router.urls)),
    path('create/', OrganizationLunchWalletView.as_view(), name='create'),
    path("organization/<int:pk>/", OrganizationAPI.as_view({"put": "update"}), name="organization"),
    path("organization/invitations", views.ListInvitesView.as_view()),
    path('users/<int:user_id>/organizations/<int:org_id>', views.UserOrganizationAPI.as_view(), name='get-organization'),
    path('get_balance/<int:organization_id>/', views.organization_balance, name='get_balance'),
    path('users/<int:org_id>/', DeleteOrganizationView.as_view(), name='delete_organization')

]

