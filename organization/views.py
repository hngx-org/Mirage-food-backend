
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
from .models import Organization, OrganizationLunchWallet, OrganizationInvites
from rest_framework.response import Response
from rest_framework import status
from users.models import User
from .serializers import OrganizationSerializer
from rest_framework.decorators import api_view
from rest_framework import generics, viewsets

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

