from django.urls import path
from .views import (CreateFreeLunchAPIView,
                    RetrieveLunchView,
                    ListAllLunchesView,
                    UserRedeemLunch,
                    CreateOrganizationFreeLunchApiView)


urlpatterns = [
    path('lunch/send', CreateFreeLunchAPIView.as_view(), name='free_lunch' ),
    path('lunch/organization/send', CreateOrganizationFreeLunchApiView.as_view(), name='free_lunch_organization' ),
    path("lunch/all", ListAllLunchesView.as_view(), name="lunch-list"), 
    path("user/redeem", UserRedeemLunch.as_view(), name="lunch-redeem"),
    path('lunch/<int:id>', RetrieveLunchView.as_view(), name='get_lunch'),


 
]
