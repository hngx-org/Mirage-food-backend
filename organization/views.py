from rest_framework.response import Response
from rest_framework import status
from .models import Organization
from users.models import User
# Create your views here.


def get_organization(request, user_id, organization_id):
    try:
        # Check if the user exists
        user = User.objects.get(id=user_id)
    except user.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    try:
        # Retrieve the organization based on user and organization IDs
        organization = Organization.objects.get(id=organization_id, user_id=user_id)
        organization_data = {
            'id': organization.id,
            'name': organization.name,
            'lunch_price': organization.lunch_price,
            'currency': organization.currency,
            'created_at': organization.created_at,
            'updated_at': organization.updated_at
        }
        return Response(organization_data)
    except Organization.DoesNotExist:
        return Response({'error': 'Organization not found'}, status=status.HTTP_404_NOT_FOUND)