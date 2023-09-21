from rest_framework.response import Response
from rest_framework import status
from users.models import User
from .serializers import OrganizationSerializer, OrganizationInviteSerializer
from rest_framework.decorators import api_view
from rest_framework import generics, viewsets
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.core.mail import EmailMessage
import secrets

from .models import Organization
from .models import OrganizationInvites




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



class OrganizationInviteCreateView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]  

    def post(self, request, *args, **kwargs):
        # Validate the request data using the serializer
        serializer = OrganizationInviteSerializer(data=request.data)
        if serializer.is_valid():
            # Generate an invite token 
            invite_token = secrets.token_urlsafe(8)

            # Creates and save the organization invite to the database
            invite = OrganizationInvites(
                org_id=request.user.organization,  
                email=serializer.validated_data["email"],
                token=invite_token,
            )
            invite.save()

            # Send an email invitation to the invitee
            try:
                email_subject = f"Invitation to Join  {request.user.organization.name}"
                email_body = f"You are invited to join our organization. Use this token: {invite_token}"
                email = EmailMessage(email_subject, email_body, from_email= "freelunch - mirage", to=[serializer.validated_data['email']])
                email.send()
            except Exception as Error:
                print(Error)

            # Respond with a success message
            response_data = {
                "message": "success",
                "statusCode": 200,
                "data": None
            }
            return Response(response_data, status=status.HTTP_200_OK)

        # If the serializer is not valid, it will respond with validation errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
