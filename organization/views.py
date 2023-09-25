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
from rest_framework.decorators import api_view
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Organization
from users.permissions import IsAdmin
from . import workers
from rest_framework.views import APIView
from .serializers import OrganizationLunchWalletSerializer
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAdminUser

class OrganizationView(APIView):
    permission_classes = [
        IsAuthenticated,
    ]

    def post(self, request):
        request.data["lunch_price"] = request.data.get("lunch_price", 1000)
        serializer = OrganizationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        workers.Organization.create_organization(**serializer.validated_data)
        return Response(serializer.validated_data, status=status.HTTP_201_CREATED)
    
class OrganizationLunchWalletView(APIView):
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

    def get(self, request):
        user = request.user
        invites = OrganizationInvites.objects.filter(org_id=user.org_id)
        return Response(ListInvitesSerializer(invites).data)

def organization_balance(request, organization_id):
    
    organization = get_object_or_404(Organization, id=organization_id)

    # Query the OrganizationLunchWallet model to get the balance for this organization
    lunch_wallet = OrganizationLunchWallet.objects.filter(org_id=organization_id).first()

    if lunch_wallet:
        balance = lunch_wallet.balance
    else:
        balance = 0.00  # default balance if no lunch wallet record exists

    return JsonResponse({'organization_balance': balance})

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

class OrganizationInviteView(APIView):
    """
    If user is an admin this lists all the invites in their Organisation
    """

    permission_classes = [OrganisationAdmin]

    def get(self, request):
        user = request.user
        invites = OrganizationInvites.objects.filter(org_id=user.org_id)
        return Response(ListInvitesSerializer(invites).data)

    def post(self, request):
        invite_created_and_sent = workers.Organization.create_organization_invite(
            admin_user=request.user, to_email=request.data.get("email")
        )
        if invite_created_and_sent:
            return Response({"message": "Invite sent"}, status=status.HTTP_201_CREATED)
        return Response({"message": "Invite failed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
class UpdateWalletAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
    def patch(self, request, **kwargs):
        balance = request.data.get('balance')
        user = request.user
        org_id = user.org_id

        try:
            # Retrieve the organization's lunch wallet based on the organization ID
            lunch_wallet = OrganizationLunchWallet.objects.get(org_id=org_id)

            # Update the balance
            lunch_wallet.balance = balance
            lunch_wallet.save()

            # Serialize the updated wallet data
            serialized_data = OrganizationLunchWalletSerializer(lunch_wallet).data

            return Response({
                "message": "success",
                "statusCode": status.HTTP_200_OK,
                "data": serialized_data
            })

        except OrganizationLunchWallet.DoesNotExist:
            return Response({
                "message": "Organization lunch wallet not found",
                "statusCode": status.HTTP_404_NOT_FOUND
            })

        except Exception as e:
            return Response({
                "message": "An error occurred while updating the wallet",
                "statusCode": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "error": str(e)
            })

