from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from users.models import User
from organization.models import Organization, OrganizationLunchWallet
from .models import Lunch
from .serializers import LunchSerializer
from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema


class CreateOrganizationFreeLunchApiView(APIView):
    permission_classes = [IsAdminUser]
    
    @swagger_auto_schema(
        operation_summary="Organization admin can send free lunch to any user in the organization",
        request_body=LunchSerializer,
        responses={201: 'lunch request created successfully',
                    400: 'Bad Request',
                    403: 'User not permitted to perform this action'}
    )
    def post(self, request, *args, **kwargs):

        data = request.data
        user = request.user

        receiver_id = data.get('receiver_id')
    
        quantity = data.get('quantity')
        if not isinstance(quantity, int):
            response = {
                "status": "failed",
                "message": "quantity must be an integer"
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        if quantity < 1:
            response = {
                "status": "failed",
                "message": "quantity cannot be less than 1 "
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(pk=user.id)
        except User.DoesNotExist:
            response = {
                "status": "error",
                "error": "User not found"
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)

        if user.org_id is None:
            response = {
                "status": "error",
                "error": "Only user with an organization can send a lunch"
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
       
        try:
            organization = Organization.objects.get(pk=user.org_id_id)
        except Organization.DoesNotExist:
            return Response(response, status=status.HTTP_404_NOT_FOUND)
    
        organization_lunch_price = organization.lunch_price
        if organization_lunch_price is None:
            response = {
                "status": "error",
                "error": "Organization lunch price not set"
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            organization_wallet = OrganizationLunchWallet.objects.get(org_id_id=organization.id)
        except OrganizationLunchWallet.DoesNotExist:
            response = {
                "status": "error",
                "error": "Organization wallet balance not set"
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        organization_wallet_balance = organization_wallet.balance
       
        if receiver_id == user.id:
            response = {
                "status": "error",
                "error": "You can't send lunch to yourself"
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
            
        if int(organization_wallet_balance) < (int(quantity) * organization_lunch_price):
            response = {
                "status": "error",
                "error": "Organization wallet balance is not enough"
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        
        # Create a lunch request
        data['sender_id'] = user.id
        data['org_id'] = user.org_id_id

        serializer = LunchSerializer(data=data)
        if serializer.is_valid():
            # Update the lunch credit balance for the user
            organization_wallet.balance = int(organization_wallet_balance) - (int(quantity) * organization_lunch_price)
            organization_wallet.save()
                
            # Create a lunch request
            serializer.save()
                
            response = {
                    "message": "Lunch request created successfully",
                    "status": "success",
                    "data": serializer.data
                }
            return Response(response, status=status.HTTP_201_CREATED)
            
        bad_response = {
                    "message": "Lunch request not created",
                    "status": "failed",
                    "data": serializer.errors
                    }
        return Response(bad_response, status=status.HTTP_400_BAD_REQUEST)


class CreateFreeLunchAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Any user can send free lunch to any user in the organization",
        request_body=LunchSerializer,
        responses={201: 'lunch request created successfully',
                    400: 'Bad Request',
                    403: "User not authorized to perform action"}
    )
    def post(self, request, *args, **kwargs):

        data = request.data
        user = request.user

        receiver_id = data.get('receiver_id')
        quantity = data.get('quantity')
        if not isinstance(quantity, int):
            response = {
                "status": "failed",
                "message": "quantity must be an integer"
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        if quantity < 1:
            response = {
                "status": "failed",
                "message": "quantity cannot be less than 1 "
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
       
        try:
            user = User.objects.get(pk=user.id)
        except User.DoesNotExist:
            response = {
                "status": "error",
                "error": "User not found"
                 }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        
        if user.org_id is None:
            response = {
                "status": "error",
                "error": "Only user with an organization can send a lunch"
                 }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        try:
            organization = Organization.objects.get(pk=user.org_id_id)
        except Organization.DoesNotExist:
            response = {
                "status": "error",
                "error": "Organization not found"
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        org_id = organization.id

        organization_lunch_price = organization.lunch_price
        if organization_lunch_price is None:
            response = {
                "status": "error",
                "error": "Organization lunch price not set"
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
    
        # Check if the user has enough lunch credits
        if int(user.lunch_credit_balance) < (int(quantity) * int(organization_lunch_price)):
            response = {
                "status": "error",
                "error": "You don't have enough lunch credits"
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        
        if user.id == receiver_id:
            response = {
                "status": "error",
                "error": "You can't send lunch to yourself"
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        
        # Create a lunch request
        data['sender_id'] = user.id
        data["org_id"] = org_id

        serializer = LunchSerializer(data=data)
        if serializer.is_valid():
        
            # Update the lunch credit balance for the user
            user.lunch_credit_balance = int(user.lunch_credit_balance) - (int(quantity) * organization_lunch_price)
            user.lunch_credit_balance = int(user.lunch_credit_balance)
            user.save()

            serializer.save()
            response = {
                    "message": "Lunch request created successfully",
                    "status": "success",
                    "data": serializer.data
                    }
            return Response(response, status=status.HTTP_201_CREATED)
        
        bad_response = {
                    "message": "Lunch request not created",
                    "status": "failed",
                    "data": serializer.errors
                }
        return Response(bad_response, status=status.HTTP_400_BAD_REQUEST)


class RetrieveLunchView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Get a lunch request by id",
        
        responses={200: 'successfully fetched lunch',
                    400: 'Bad Request',
                    403: 'Forbidden'}
    )
    def get(self, request, id):
        try:
            lunch = Lunch.objects.get(pk=id)
            # Check if the user is an admin
            if request.user.is_staff:
                serializer = LunchSerializer(lunch)
                response = {
                    "message": "Successfully fetched lunch",
                    "status": "success",
                    "data": serializer.data
                }
                return Response(response, status=status.HTTP_200_OK)

            # Check if the user is either the sender or receiver of the lunch
            elif request.user == lunch.receiver_id or request.user == lunch.sender_id:
                serializer = LunchSerializer(lunch)
                response = {
                    "message": "Successfully fetched lunch",
                    "status": "success",
                    "data": serializer.data
                }
                return Response(response, status=status.HTTP_200_OK)
            
            forbidden_response = {
                    "status": "error",
                    "message": "You're not authorized to view this lunch"
                    }
            return Response(forbidden_response, status=status.HTTP_403_FORBIDDEN)
        
        except Lunch.DoesNotExist:
            response = {
                "status": "error",
                "error": "Lunch not found"
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)


class ListAllLunchesView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="User can get all lunches sent or received by them",
        responses={200: 'successfully fetched lunches',
                    400: 'Bad Request',
                    403: 'Forbidden'}
    )
    def get(self, request):
        
        user = request.user
        user_id = user.id
        if user.is_superuser:
            lunches = Lunch.objects.all()
            serializer = LunchSerializer(lunches, many=True)
            response = {
                "message": "successfully fetched lunches",
                "status": "success",
                "data": serializer.data
                }
            return Response(response, status=status.HTTP_200_OK)

        lunches = Lunch.objects.filter(Q(sender_id=user_id) | Q(receiver_id=user_id)).all()
        serializer = LunchSerializer(lunches, many=True)
        response = {
                "message": "successfully fetched lunches",
                "status": "success",
                "data": serializer.data
            }
        return Response(response, status=status.HTTP_200_OK)


class UserRedeemLunch(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="User can redeem a lunch",
        responses={201: 'Lunch redeemed successfully',
                    400: 'Bad Request',
                    403: 'Forbidden'}
    )
    def post(self, request):
        data = request.data
        user = request.user

        lunch_id = data.get('id')
        if not isinstance(lunch_id, int):
            response = {
                "status": "failed",
                "message": "lunch id must be an integer"
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        try:
            lunch = Lunch.objects.get(pk=lunch_id)
        except Lunch.DoesNotExist:
            response = {
                "status": "error",
                "error": "Lunch not found"
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        
        try:
            user = User.objects.get(pk=user.id)
        except User.DoesNotExist:
            response = {
                "status": "error",
                "error": "User not found"
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)

        if user.id == lunch.receiver_id_id:
            if not lunch.redeemed:
                lunch.redeemed = True

                if user.org_id is None:
                    response = {
                        "status": "error",
                        "error": "Only user with an organization can redeem a lunch"
                    }
                    return Response(response, status=status.HTTP_400_BAD_REQUEST)
                
                try:
                    organization = Organization.objects.get(pk=user.org_id_id)
                except Organization.DoesNotExist:
                    response = {
                        "status": "error",
                        "message": "Organization not found"
                    }
                    return Response(response, status=status.HTTP_404_NOT_FOUND)
                
                organization_lunch_price = organization.lunch_price
                if organization_lunch_price is None:
                    response = {
                        "status": "error",
                        "message": "Organization lunch price not set"
                        }
                    return Response(response, status=status.HTTP_400_BAD_REQUEST)
                
                user_lunch_wallet_balance = int(user.lunch_credit_balance) + (int(lunch.quantity) * organization_lunch_price)
                user.lunch_credit_balance = int(user_lunch_wallet_balance)
                
                # Save the changes to the lunch and user objects
                lunch.save()
                user.save()
                
                # Serialize the lunch object for the response
                serializer = LunchSerializer(lunch)
                response = {
                            "status": "success",
                            "message": "Lunch redeemed successfully",
                            "data": serializer.data}
                return Response(response, status=status.HTTP_201_CREATED)

            bad_response = {
                "status": "error",
                "message": "Lunch has already been redeemed"}
            return Response(bad_response, status=status.HTTP_400_BAD_REQUEST)
        
        forbidden_response = {
                "status": "failed",
                "message": "You're not authorized to redeem this lunch"}
        return Response(forbidden_response, status=status.HTTP_403_FORBIDDEN)
