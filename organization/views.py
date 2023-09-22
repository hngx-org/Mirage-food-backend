from rest_framework import authentication
from rest_framework.views import APIView
from .serializers import ListInvitesSerializer
from .permissions import OrganisationAdmin
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Organization, OrganizationLunchWallet, OrganizationInvites
from rest_framework.response import Response
from rest_framework import status
from users.models import User
from .serializers import OrganizationSerializer
from rest_framework.views import APIView
# from rest_framework.decorators import api_view
from rest_framework import generics, viewsets
from users.permissions import IsAdmin

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


from .models import Organization

from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import OrganizationLunchWalletSerializer
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST

<<<<<<< HEAD
#organizationwalletupdate changes
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from rest_framework import generics, status
from .serializers import OrganizationLunchWalletUpdateSerializer


=======
from rest_framework.decorators import api_view
>>>>>>> 2e4a341bb10e028bb9dc79bd4cf3be5b6e8c092b

class OrganizationLunchWalletView(APIView):
    @swagger_auto_schema(
        operation_summary="Create organization wallet",
        request_body=OrganizationLunchWalletSerializer,
        responses={201: 'Created', 400: 'Bad Request'},
    )
    def post(self, request):
        serializer = OrganizationLunchWalletSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
# Create your views here.


class ListInvitesView(APIView):
    """
    If user is an admin this lists all the invites in their Organisation
    """
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [OrganisationAdmin]

    @swagger_auto_schema(
        operation_summary="List Organization Invitations",
        responses={status.HTTP_200_OK: openapi.Response("successful", ListInvitesSerializer)},
    )
    def get(self, request):
        user = request.user
        invites = OrganizationInvites.objects.filter(org_id=user.org_id)
        return Response(ListInvitesSerializer(invites).data)

@api_view(['GET'])
def organization_balance(request, organization_id):
    
    organization = get_object_or_404(Organization, id=organization_id)

    # Query the OrganizationLunchWallet model to get the balance for this organization
    lunch_wallet = OrganizationLunchWallet.objects.filter(org_id=organization_id).first()

    if lunch_wallet:
        balance = lunch_wallet.balance
    else:
        balance = 0.00  # default balance if no lunch wallet record exists

    return JsonResponse({'organization_balance': balance})


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

    @swagger_auto_schema(
                operation_summary="Get all organizations",
                responses={
                    status.HTTP_200_OK: openapi.Response("Organization details", OrganizationSerializer(many=True)),
                    }
        )
    def get_queryset(self):
        return Organization.objects.all()
      
class DeleteOrganizationView(APIView):
    permission_classes = [IsAdmin]
    def delete(request, org_id):
        organization = Organization.object.get(pk=org_id)
        if request.user in organization.user_set.all():
            organization.delete()
            return Response({'message':'Organization deleted'},status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'error':'Organization not found'}, status=status.HTTP_404_NOT_FOUND)


#organizationwalletupdate changes

class OrganizationWalletUpdateView(generics.RetrieveUpdateAPIView,):
    #authentication_classes = [authentication.TokenAuthentication]
    queryset=OrganizationLunchWallet.objects.all()
    serializer_class = OrganizationLunchWalletSerializer
    permission_classes=[OrganisationAdmin]
    
    def get_object(self):
        """get the org-id asssociated with a user"""
        org_id=self.request.user.org_id
        try:
            return  OrganizationLunchWallet.objects.get(org_id=org_id)

        except: OrganizationLunchWallet.DoesNotExist

    def update(self,request,*args,**kwargs):
        if not request.user.is_staff:
        
            return Response({"error":"You do not have permission to change the balance"})
        return super().update(request,*args,**kwargs)  


