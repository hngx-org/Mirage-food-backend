from rest_framework.response import Response
from rest_framework import status
from .models import Organization
from users.models import User
from .serializers import OrganizationSerializer


# Create your views here.


def get_organization(request, user_id, organization_id):
    try:
        # Check if the user exists
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    try:
        # Retrieve the organization based on user and organization IDs
        organization = Organization.objects.get(id=organization_id, user_id=user_id)
        serializer = OrganizationSerializer(organization)  # Serialize the organization
        return Response(serializer.data)
    except Organization.DoesNotExist:
        return Response({'error': 'Organization not found'}, status=status.HTTP_404_NOT_FOUND)
