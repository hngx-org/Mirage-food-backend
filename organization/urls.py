from django.urls import path
from .views import OrganizationLunchWalletView
from . import views
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import OrganizationAPI, UserOrganizationAPI, DeleteOrganizationView

#oragnizationwalletupdate changes
from .views import OrganizationWalletUpdateView

app_name = "organization"

router = DefaultRouter()
router.register("", OrganizationAPI, basename="organization")

urlpatterns = [
    path("", include(router.urls)),
    path("organization/create", views.OrganizationView.as_view()),
    path('create', OrganizationLunchWalletView.as_view(), name='create'),
    path("organization/<int:pk>/", OrganizationAPI.as_view({"put": "update"}), name="organization"),
    path("organization/invitations", views.ListInvitesView.as_view()),
    path('users/<int:user_id>/organizations/<int:org_id>', views.UserOrganizationAPI.as_view(), name='get-organization'),
    path('get_balance/<int:organization_id>/', views.organization_balance, name='get_balance'),
    path("organization/wallet/update",views.OrganizationWalletUpdateView.as_view(),name="wallet-update"),
    path('users/<int:org_id>/', DeleteOrganizationView.as_view(), name='delete_organization'),


]

