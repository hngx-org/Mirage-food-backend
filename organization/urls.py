from django.urls import path
from .views import OrganizationLunchWalletView

from . import views
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (OrganizationAPI, 
                    OrganizationInviteCreateView, UserOrganizationAPI, 
                    OrganizationLunchPriceViewSet, DeleteOrganizationView)



#oragnizationwalletupdate changes
from .views import OrganizationWalletUpdateView


 # Correct import path

# Create a router for your viewsets
router = DefaultRouter()
router.register(r'invitations', views.InvitationViewSet)  # Correct viewset import path

#urlpatterns = [
    #path('admin/', admin.site.urls),
    #path('api/users/<int:user_id>/organizations/<int:org_id>/', include(router.urls)),





app_name = "organization"

router = DefaultRouter()
router.register("", OrganizationAPI, basename="organization")

urlpatterns = [
    path("", include(router.urls)),
    path("organization/create", OrganizationInviteCreateView.as_view()),
    path('create', OrganizationLunchWalletView.as_view(), name='create'),
    path("organization/<int:pk>/", OrganizationAPI.as_view({"put": "update"}), name="organization"),

    # path('users/<int:user_id>/organizations/<int:org_id>', views.get_organization, name='get-organization'),
    path('organization/invite/', OrganizationInviteCreateView.as_view(), name="organization-invite" ),


    path('users/<int:user_id>/organizations/<int:org_id>', views.UserOrganizationAPI.as_view(), name='get-organization'),
    path('get_balance/<int:organization_id>/', views.organization_balance, name='get_balance'),
    path(
        'organization/lunch/update/',
        OrganizationLunchPriceViewSet.as_view({'patch'}),
        name='update_lunch_price'
        ),
    path("organization/wallet/update",views.OrganizationWalletUpdateView.as_view(),name="wallet-update"),
    path('users/<int:org_id>/', DeleteOrganizationView.as_view(), name='delete_organization'),
    ]




