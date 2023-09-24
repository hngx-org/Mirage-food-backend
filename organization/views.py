
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Organization, Invitation
from django.contrib.auth.models import User
from .serializers import InvitationSerializer

class InvitationViewSet(viewsets.ModelViewSet):
    queryset = Invitation.objects.all()
    serializer_class = InvitationSerializer

def create(self, request, *args, **kwargs):
    # Retrieve data from the request and create an invitation instance
    sender = get_object_or_404(User, pk=request.user.id)
    user_id = kwargs.get('user_id')  # Get user_id from URL parameters
    org_id = kwargs.get('org_id')    # Get org_id from URL parameters
    receiver_username = request.data.get('receiver_username')

    try:
        organization = get_object_or_404(Organization, pk=org_id)
        receiver = User.objects.get(username=receiver_username)

        # Create a new invitation
        invitation = Invitation(sender=sender, receiver=receiver, organization=organization)
        invitation.save()

        # You can customize the response message as needed
        response_data = {
            'message': 'Invitation sent successfully',
            'invitation_id': invitation.id,
        }

        return JsonResponse(response_data, status=201)

    except User.DoesNotExist:
        response_data = {'error': 'Receiver not found'}
        return JsonResponse(response_data, status=404)

from rest_framework import authentication
from rest_framework.views import APIView
from .serializers import ListInvitesSerializer
from .permissions import OrganisationAdmin
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import(
        Organization,
        OrganizationLunchWallet,
        OrganizationInvites,
        OrganizationLunchPrice
        )
from rest_framework.response import Response
from rest_framework import status
from users.models import User
<<<<<<< HEAD
from .serializers import(
        OrganizationSerializer,
        OrganizationLunchPriceSerializer
        )
from rest_framework.decorators import api_view
from .serializers import OrganizationSerializer
from rest_framework.views import APIView
# from rest_framework.decorators import api_view
from rest_framework import generics, viewsets

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


<<<<<<< HEAD
class OrganizationLunchWalletView(APIView):
=======

class OrganizationView(APIView):
    permission_classes = [ IsAdmin,]
>>>>>>> 180d01ac0945fe0739cc74b9f05870bbd243500b
    @swagger_auto_schema(
           
            operation_summary="Allows an admin to create an organization",
            request_body=OrganizationSerializer,
            responses={201: 'Created', 400: 'Bad Request'},
        )

    def post(self, request):
        request.data["lunch_price"] = request.data.get("lunch_price", 1000)
        serializer = OrganizationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        workers.Organization.create_organization(**serializer.validated_data)
        return Response(serializer.validated_data, status=status.HTTP_201_CREATED)
    
class OrganizationAPI(generics.UpdateAPIView, viewsets.GenericViewSet):
 
    
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


class OrganizationLunchWalletView(APIView):
    permission_classes = [OrganisationAdmin]

    @swagger_auto_schema(
        method="post",
        operation_summary="Create organization wallet",
        request_body=OrganizationSerializer,
        responses={201: 'Created', 400: 'Bad Request'},
    )
    @api_view(['POST'])
    def post(self, request):
        serializer = OrganizationLunchWalletSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


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
@swagger_auto_schema(
        operation_summary="List Organization Invitations",
        operation_description=  "If user is an admin this lists all the invites in their Organisation",
        responses={status.HTTP_200_OK: openapi.Response("successful", ListInvitesSerializer)},
    )

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
          
                responses={
                    status.HTTP_200_OK: openapi.Response("User details", OrganizationSerializer(many=True)),
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

    def get_queryset(self):
        return Organization.objects.all()
      
      
class DeleteOrganizationView(APIView):
    """this endpoint allows an admin user to delete a user"""
    permission_classes = [IsAdmin]
    @swagger_auto_schema(
        operation_summary="Delete a user",
        operation_description=  "This endpoint allows an admin  to delete a user. It takes in the org_id",
        responses={
            status.HTTP_200_OK: openapi.Response("Organization details", OrganizationSerializer(many=True)),
            status.HTTP_404_NOT_FOUND: "Organization not found for this user",
            status.HTTP_403_FORBIDDEN: "Permission denied",
                            
            }
    )

<<<<<<< HEAD
=======

    def delete(request, org_id):
        organization = Organization.object.get(pk=org_id)
        if request.user in organization.user_set.all():
            organization.delete()
            return Response({'message':'Organization deleted'},status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'error':'Organization not found'}, status=status.HTTP_404_NOT_FOUND)



#organizationwalletupdate changes

class OrganizationWalletUpdateView(generics.UpdateAPIView,):

    authentication_classes = [authentication.TokenAuthentication]
    serializer_class = OrganizationLunchWalletUpdateSerializer
    permission_classes=[OrganisationAdmin]

    @swagger_auto_schema(
        operation_summary="Update the organization wallet",
        operation_description="This endpoint allows an admin to update organization's lunch wallet",
        responses={
            status.HTTP_200_OK: openapi.Response("User details", OrganizationLunchWalletSerializer()),
            status.HTTP_404_NOT_FOUND: "Organization not found for this user",
            status.HTTP_403_FORBIDDEN: "Permission denied",
            }
    )

    def get_object(self):
        """get the org-id asssociated with a user"""
        user=self.request.user
        org_id=self.request.user.id
        try:
            wallet=  OrganizationLunchWallet.objects.get(id=org_id)
            return wallet
        except: OrganizationLunchWallet.DoesNotExist

    def patch(self,request,*args,**kwargs):
        wallet=self.get_object()
        serializer=self.get_serializer(wallet,data=request.data,partial=True)
        response_data={
            "message":"success",
            "status":status.HTTP_200_OK,
            "balance":None
        }
        
        if serializer.is_valid():
            serializer.save()
            return Response(response_data, status=HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
       
       
        if not request.user.is_staff:
        
            return Response({"error":"You do not have permission to change the balance"})
        return super().update(request,*args,**kwargs)  """


   
>>>>>>> 180d01ac0945fe0739cc74b9f05870bbd243500b

class OrganizationLunchPriceViewSet(viewsets.ModelViewSet):
    """
    if user is an admin, they can update lunch prices
    """
    queryset = OrganizationLunchPrice.objects.all()
    serializer_class = OrganizationLunchPriceSerializer

    permission_classes = [OrganisationAdmin]

    @action(detail=False, methods=['patch'])
    def update_lunch_price(self, request):
        try:
            new_price = request.data['lunch_price']

            org_lunch = OrganizationLunchPrice.objects.first()
            org_lunch.lunch_price = new_price
            org_lunch.save()

            return Response({'message': 'success'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response(
                    {'error': 'User not found'},
                    status=status.HTTP_404_NOT_FOUND
                    )
