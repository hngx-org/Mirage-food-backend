
from rest_framework.response import Response
from rest_framework import status
from users.models import User
from .serializers import OrganizationSerializer
from rest_framework.decorators import api_view
from rest_framework import generics, viewsets

from .models import Organization

from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import OrganizationLunchWalletSerializer
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST

class OrganizationLunchWalletView(APIView):
    def post(self, request):
        serializer = OrganizationLunchWalletSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
# Create your views here.


@api_view(['GET'])
def get_organization(request, user_id, org_id):
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

