from django.urls import path
from .views import DeleteOrganizationView

urlpatterns = [
    path('users/<int:org_id>/', DeleteOrganizationView.as_view(), name='delete_organization'),

]