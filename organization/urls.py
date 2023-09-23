from django.urls import path
from .views import (CreateOrganizationView,
                    CreateOrganizationInviteView,
                    CreateStaffFromOrganizationView,
                    StaffConfirmTokenAndSignUpView)


urlpatterns = [
    path("organization/create", CreateOrganizationView.as_view(), name="create-organization"),
    path("organization/invite", CreateOrganizationInviteView.as_view(), name="create-invite"),
    path("organization/staff/auth/signup", CreateStaffFromOrganizationView.as_view(), name="create-staff-from-invite"),
    path("organization/staff/signup", StaffConfirmTokenAndSignUpView.as_view(), name="staff-signup")
]