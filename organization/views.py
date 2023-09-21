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
