from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import OrganizationSerializer, OrganizationInviteSerializer
from users.permissions import IsAdmin
from . import workers

from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.core.mail import EmailMessage
import secrets

# Create your views here.


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



@permission_classes([IsAuthenticated, IsAdminUser])
class OrganizationInviteView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = OrganizationInviteSerializer(data=request.data)

        if serializer.is_valid():
            unique_token = secrets.token_urlsafe(16)  # Generate a 16-character token
            
            #tracking of invitee
            ##invite = InviteModel(email=serializer.validated_data['email'], token=unique_token)
            ##invite.save()
            
            # Send an email invitation 
            try:
                email_subject = f"Invitation to Join  Organization"
                email_body = f"You are invited to join our organization. Use this token: {unique_token}"
                email = EmailMessage(email_subject, email_body, to=[serializer.validated_data['email']])
                email.send()
            except Exception as Error:
                print(Error)
            
            response_data = {
                "message": "success",
                "statusCode": status.HTTP_201_CREATED,
                "data": None  
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        
        # In case of validation errors
        response_data = {
            "message": "error",
            "statusCode": status.HTTP_400_BAD_REQUEST,
            "data": serializer.errors
        }
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)