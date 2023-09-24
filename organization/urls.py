from django.urls import path
from .views import (CreateOrganizationView,
                    CreateOrganizationInviteView,
                    CreateStaffFromOrganizationView,
                    StaffConfirmTokenAndSignUpView,
                    OrganizationLunchWalletView,
                    UpdateOrganizationLunchPriceView)

urlpatterns = [
    path("organization/create", CreateOrganizationView.as_view(), name="create-organization"),
    path("organization/invite", CreateOrganizationInviteView.as_view(), name="create-invite"),
    path("organization/staff/auth/signup", CreateStaffFromOrganizationView.as_view(), name="create-staff-from-invite"),
    path("organization/staff/signup", StaffConfirmTokenAndSignUpView.as_view(), name="staff-signup"),
    path("organization/wallet/update", OrganizationLunchWalletView.as_view(), name="update-organization-wallet"),
    path("organization/lunch/update", UpdateOrganizationLunchPriceView.as_view(), name="update-organization-lunch-price"),    

]
