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
    path("organization/launch/update", UpdateOrganizationLunchPriceView.as_view(), name="update-organization-lunch-price"),    

]







# urlpatterns = [
#     path("organization/create", CreateOrganizationView.as_view(), name="create-organization"),
#     path("organization/invite", Corganization = Organization.objects.filter(id=request.user.org_id.id).first()
#                 organization_lunch_price = organization.lunch_price
#                 if organization:
#                     user = User.objects.get(pk=request.user.id)
#                     user_lunch_wallet_balance = (int(lunch.quantity) * organization_lunch_price) + int(user.lunch_credit_balance)
#                     user.lunch_credit_balance = user_lunch_wallet_balance


#                 else:
#                     user = User.objects.get(pk=request.user.id)
#                     user_lunch_wallet_balance = (int(lunch.quantity) * 100) + int(user.lunch_credit_balance)
#                     user.lunch_credit_balance = user_lunch_wallet_balancereateOrganizationInviteView.as_view(), name="create-invite"),
#     path("organization/staff/auth/signup", CreateStaffFromOrganizationView.as_view(), name="create-staff-from-invite"),
#     path("organization/staff/signup", StaffConfirmTokenAndSignUpView.as_view(), name="staff-signup"),
#     # path("organization/wallet/update", UpdateOrganizationLunchWallet.as_view(),name="organization-lunch-wallet")
# ]
