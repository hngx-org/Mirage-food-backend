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

from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import OrganizationLunchWalletSerializer
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST

from rest_framework.decorators import api_view


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
