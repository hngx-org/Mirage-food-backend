from rest_framework import authentication
from rest_framework.views import APIView
from users.serializers import UserRegistrationSerializer
from .models import Organization, OrganizationLunchWallet, OrganizationInvites
from rest_framework.response import Response
from rest_framework import status
from users.models import User
from .serializers import OrganizationSerializer, OrganizationInviteSerializer
from rest_framework.decorators import api_view
from rest_framework import generics, viewsets
import secrets
from django.urls import reverse
from django.contrib.auth.hashers import make_password

from .models import Organization
from users.permissions import IsAdmin
from rest_framework.permissions import AllowAny
from . import workers
from django.core.mail import send_mail


class CreateOrganizationView(APIView):
    permission_classes = [
        IsAdmin
    ]

    def post(self, request):
        
        data = request.data
        serializer = OrganizationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            response = {
                "status": "success",
                "message": "organization created successfully",
                "data": serializer.data
            }
            return Response(response, status=status.HTTP_201_CREATED)
        bad_response = {
                "status": "error",
                "message": "bad request",
                "data": serializer.errors
            }
        return Response(bad_response, status=status.HTTP_400_BAD_REQUEST)



class CreateOrganizationInviteView(APIView):
    permission_classes = [
        IsAdmin
    ]

    def post(self, request):
        data = request.data
        org_admin = User.objects.get(pk=request.user.id)
        org_id = org_admin.org_id
        data["org_id"] = org_id.id
        token = secrets.token_urlsafe(10)
        data["token"] = token
        serializer = OrganizationInviteSerializer(data=data)
        if serializer.is_valid():
            # Save the data to the database
            invite = serializer.save()
            
            # Send email to the invitee
            subject = 'Invitation to join Mirage Free Lunch App'
            message = 'Click the link to sign up'
            from_email = 'abiolaadedayo1993@gmail.com'
            recipient_list = [invite.email]
            token = invite.token  # Access the token from the saved instance

            # Generate the invitation URL
            invite_url = f"http://127.0.0.1/api/organization/invite/?token={token}"
            message += f'\n\n{invite_url}'

            try:
                send_mail(subject, message, from_email, recipient_list)
                response = {
                    "status": "success",
                    "message": "Invitation email sent successfully"
                }
                return Response(response, status=status.HTTP_200_OK)
            except Exception as e:
                failed_response = {
                    "status": "failed",
                    "message": f"Email not sent: {str(e)}"
                }
                return Response(failed_response, status=status.HTTP_400_BAD_REQUEST)
        else:
            bad_response = {
                "status": "error",
                "message": "Bad request",
                "data": serializer.errors
            }
            return Response(bad_response, status=status.HTTP_400_BAD_REQUEST)


class CreateStaffFromOrganizationView(APIView):
    permission_classes = [
        IsAdmin
    ]

    def post(self, request):
        data = request.data
        org_admin = User.objects.get(pk=request.user.id)
        org_id = org_admin.org_id

        # Check if the organization invite exists for the provided email
        organization_invite = OrganizationInvites.objects.filter(email=data["email"]).first()
        if not organization_invite:
            bad_response = {
                "status": "error",
                "message": "Organization invite not found for the provided email",
            }
            return Response(bad_response, status=status.HTTP_400_BAD_REQUEST)

        # Assign org_id and refresh_token to data
        data["org_id"] = org_id.id
        data["refresh_token"] = organization_invite.token

        serializer = UserRegistrationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            response = {
                "status": "success",
                "message": "Staff created successfully",
                "data": serializer.data,
            }
            return Response(response, status=status.HTTP_201_CREATED)

        bad_response = {
            "status": "error",
            "message": "Bad request",
            "data": serializer.errors,
        }
        return Response(bad_response, status=status.HTTP_400_BAD_REQUEST)
    

class StaffConfirmTokenAndSignUpView(APIView):
    permission_classes = [
        AllowAny
    ]

    def post(self, request):
        data = request.data
        refresh_token = data["token"]
        user = User.objects.filter(refresh_token=refresh_token).first()
        if not user:
            bad_response = {
                "status": "error",
                "message": "Invalid token",
            }
            return Response(bad_response, status=status.HTTP_400_BAD_REQUEST)
        # Explicitly hash the password
        password = data.get("password")
        if password:
            hashed_password = make_password(password)
            user.password = hashed_password

        serializer = UserRegistrationSerializer(user, data=data)
        if serializer.is_valid():
            user.refresh_token = None
            serializer.save()
            response = {
                "status": "success",
                "message": "User Account Created successfully",
                "data": serializer.data,
            }
            return Response(response, status=status.HTTP_201_CREATED)

        bad_response = {
            "status": "error",
            "message": "Bad request",
            "data": serializer.errors,
        }
        return Response(bad_response, status=status.HTTP_400_BAD_REQUEST)

    
# class OrganizationLunchWalletView(APIView):
#     def post(self, request):
#         serializer = OrganizationLunchWalletSerializer(data=request.data)

#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
# # Create your views here.


# class ListInvitesView(APIView):
#     """
#     If user is an admin this lists all the invites in their Organisation
#     """
#     authentication_classes = [authentication.TokenAuthentication]
#     permission_classes = [OrganisationAdmin]

#     def get(self, request):
#         user = request.user
#         invites = OrganizationInvites.objects.filter(org_id=user.org_id)
#         return Response(ListInvitesSerializer(invites).data)

# def organization_balance(request, organization_id):
    
#     organization = get_object_or_404(Organization, id=organization_id)

#     # Query the OrganizationLunchWallet model to get the balance for this organization
#     lunch_wallet = OrganizationLunchWallet.objects.filter(org_id=organization_id).first()

#     if lunch_wallet:
#         balance = lunch_wallet.balance
#     else:
#         balance = 0.00  # default balance if no lunch wallet record exists

#     return JsonResponse({'organization_balance': balance})

# @api_view(['GET'])
# def get_organization(request, user_id, org_id):
#     try:
#         user = User.objects.get(pk=user_id)
#         organization = user.org_id  # Retrieve the organization associated with the user
#         if organization and organization.id == org_id:
#             serializer = OrganizationSerializer(organization)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         else:
#             return Response({'error': 'Organization not found for this user'}, status=status.HTTP_404_NOT_FOUND)
#     except User.DoesNotExist:
#         return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


# class OrganizationAPI(generics.UpdateAPIView, viewsets.GenericViewSet):
#     """Base view for organization update (put | patch)"""  # can be modified when adding other methods

#     serializer_class = OrganizationSerializer

#     def get_queryset(self):
#         return Organization.objects.all()

#     ...

