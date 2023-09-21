from rest_framework.response import Response
from rest_framework import status
from users.models import User
from .serializers import OrganizationSerializer
from rest_framework.views import APIView
# from rest_framework.decorators import api_view
from rest_framework import generics, viewsets

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Organization


# Create your views here.

class UserOrganizationAPI(APIView):
    @swagger_auto_schema(
                operation_summary="Get a user's organization",
                responses={
                    status.HTTP_200_OK: openapi.Response("User details", OrganizationSerializer()),
                    status.HTTP_404_NOT_FOUND: "Organization not found for this user",
                    status.HTTP_403_FORBIDDEN: "Permission denied",
                    }
        )
    def get(request, user_id, org_id):
        try:
            user = User.objects.get(pk=user_id)
            organization = user.org_id  # Retrieve the organization associated with the user
            if organization and organization.id == org_id:
                serializer = OrganizationSerializer(organization)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Organization not found for this user'}, status=status.HTTP_404_NOT_FOUND)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

class OrganizationAPI(generics.UpdateAPIView, viewsets.GenericViewSet):
    """Base view for organization update (put | patch)"""  # can be modified when adding other methods

    serializer_class = OrganizationSerializer

    def get_queryset(self):
        return Organization.objects.all()

    ...
