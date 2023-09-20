from django.urls import path
from . import views

urlpatterns = [
    path('users/<int:user_id>/organizations/<int:organization_id>', views.get_organization, name='get-organization'),
]
