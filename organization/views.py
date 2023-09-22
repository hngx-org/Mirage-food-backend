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
from users.permissions import IsAdmin
from . import workers

from rest_framework.views import APIView
from .serializers import OrganizationLunchWalletSerializer
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST


#organizationwalletupdate changes
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from rest_framework import generics, status
from .serializers import OrganizationLunchWalletUpdateSerializer
from rest_framework.decorators import api_view



class OrganizationView(APIView):
 


    permission_classes = [
        IsAdmin,
    ]

    def post(self, request):
        request.data["lunch_price"] = request.data.get("lunch_price", 1000)
        serializer = OrganizationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        workers.Organization.create_organization(**serializer.validated_data)
        return Response(serializer.validated_data, status=status.HTTP_201_CREATED)
    



class OrganizationLunchWalletView(APIView):
    """
    Create an organization lunch wallet

    
      - To create a new instance a send POST request with the required data
        ```
        Example POST request data:
        {
            "name": "oranisation id",
            "lunch price": "enter amount 2dp",
            "currency"
        }
        ```
    """
    @swagger_auto_schema(
        operation_summary="Create organization wallet",
        request_body=OrganizationSerializer,
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
    
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [OrganisationAdmin]

    @swagger_auto_schema(
        operation_summary="List Organization Invitations",
        operation_description=  "If user is an admin this lists all the invites in their Organisation",
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
    
    #Use this endpoint to retrieve the organization associated with a specific user. It takes two parameters , org_id to identify the organisation and user_id to identify the user.The org_id must be associated with the user_id in order to get the organization. Invalid parameters will result to errors.


    @swagger_auto_schema(
                operation_summary="Get a user's organization",
                operation_description= "Use this endpoint to retrieve the organization associated with a specific user. It takes two parameters , org_id to identify the organisation and user_id to identify the user.The org_id must be associated with the user_id in order to get the organization. Invalid parameters will result to errors.",
                parameters= "user_id and org_id,",
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
    """
    This endpoint allows the user to update the details of an organization by retrieving an organization using the organization id.
     - To create a new instance a send POST request with the required data,
    ```
            Example POST request data:
            {
                "name": "oranisation id",
                "lunch price": "enter amount 2dp",
                "currency"
            }
    ```
    """
    
    """Base view for organization update (put | patch)"""  # can be modified when adding other methods

    serializer_class = OrganizationSerializer

    @swagger_auto_schema(
        operation_summary="Get all organizations",
        operation_description=  "This endpoint allows the user to update the details of an organization by retrieving an organization using the organization id - To create a new instance a send POST request with the required data",


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

class OrganizationWalletUpdateView(generics.UpdateAPIView,):
    """
    This endpoint allows an admin user to update the organization wallet
    The requested org_id must match the requested org_id inorder to update the wallet
       ```
        Example POST request data:
        {
            "org_id": "integer",
            "balance": "enter amount 2dp",
           
        }
        ```

    """
   

    #authentication_classes = [authentication.TokenAuthentication]
    queryset=OrganizationLunchWallet.objects.all()
    serializer_class = OrganizationLunchWalletSerializer
    permission_classes=[OrganisationAdmin]

    @swagger_auto_schema(
                        operation_summary="Update the organization wallet i.e balance by admin",
                        responses={
                            status.HTTP_200_OK: openapi.Response("User details", OrganizationLunchWalletSerializer()),
                            status.HTTP_404_NOT_FOUND: "Organization not found for this user",
                            status.HTTP_403_FORBIDDEN: "Permission denied",
                            }
                )


    
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


   