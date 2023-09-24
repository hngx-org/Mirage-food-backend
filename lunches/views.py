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


class CreateOrganizationFreeLunchApiView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, *args, **kwargs):
        data = request.data
        receiver_id = data.get('receiver_id')
        quantity = data.get('quantity')
        note = data.get('note')
        data['sender_id'] = request.user.id
        data['org_id'] = request.user.org_id.id

        organization = Organization.objects.filter(id=request.user.org_id.id).first()
    
        organization_lunch_price = organization.lunch_price
        organization_wallet = OrganizationLunchWallet.objects.filter(org_id=organization).first()
        organization_wallet_balance = organization_wallet.balance

        if receiver_id == request.user.id:
            return Response(
                {"error": "You can't send lunch to yourself"},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        if int(organization_wallet_balance) < (int(quantity) * organization_lunch_price):
            return Response(
                    {"error": "Organization doesn't have enough lunch credits"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            # Create a lunch request
            serializer = LunchSerializer(data=data)
            if serializer.is_valid():
                # Update the lunch credit balance for the user
                organization_wallet.balance = int(organization_wallet_balance) - (int(quantity)*organization_lunch_price)
                organization_wallet.save()
                
                # Create a lunch request
                serializer.save()
                
                response = {
                    "message": "Lunch request created successfully",
                    "statusCode": status.HTTP_201_CREATED,
                    "data": serializer.data
                }
                return Response(response, status=status.HTTP_201_CREATED)
            else:
                bad_response = {
                    "message": "Lunch request not created",
                    "statusCode": status.HTTP_400_BAD_REQUEST,
                    "data": serializer.errors
                }
                return Response(bad_response, status=status.HTTP_400_BAD_REQUEST)





class CreateFreeLunchAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):

        data = request.data
        receiver_id = data.get('receiver_id')
        quantity = data.get('quantity')
        if quantity is None:
            quantity = 1
        note = data.get('note')
        request.user.id
        user = User.objects.get(pk=request.user.id)
        if user.org_id_id is None:
            return Response(
                {"error": "Only user with an organization can send a lunch"},
                status=status.HTTP_400_BAD_REQUEST
            )

        organization = Organization.objects.filter(id=request.user.org_id_id).first()
        org_id_id = organization.id
        organization_lunch_price = organization.lunch_price
        
        # Get the user making the request
        user = request.user
       
        # Check if the user has enough lunch credits
        if int(user.lunch_credit_balance) < (int(quantity) * int(organization_lunch_price)):
            return Response(
                {"error": "You don't have enough lunch credits"},
                status=status.HTTP_400_BAD_REQUEST
            )
        elif user.id == receiver_id:
            return Response(
                {"error": "You can't send lunch to yourself"},
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
            # Create a lunch request
            data['sender_id'] = user.id  # Set the sender_id
            data["org_id"] = org_id_id
            serializer = LunchSerializer(data=data)
            
            if serializer.is_valid():
        
                # Update the lunch credit balance for the user
                organization = Organization.objects.filter(id=org_id_id).first()
                organization_lunch_price = organization.lunch_price
                
                user.lunch_credit_balance = int(user.lunch_credit_balance) - (int(quantity)*organization_lunch_price)
                user.lunch_credit_balance = int(user.lunch_credit_balance)
                user.save()
                serializer.save()
                
                response = {
                    "message": "Lunch request created successfully",
                    "statusCode": status.HTTP_201_CREATED,
                    "data": serializer.data
                }
                return Response(response, status=status.HTTP_201_CREATED)
            else:
                bad_response = {
                    "message": "Lunch request not created",
                    "statusCode": status.HTTP_400_BAD_REQUEST,
                    "data": serializer.errors
                }
                return Response(bad_response, status=status.HTTP_400_BAD_REQUEST)


class RetrieveLunchView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        try:
            lunch = Lunch.objects.get(pk=id)
            print(type(request.user.id), type(lunch.receiver_id))

            # Check if the user is an admin
            if request.user.is_staff:
                serializer = LunchSerializer(lunch)
                response = {
                    "message": "Successfully fetched lunch",
                    "statusCode": status.HTTP_200_OK,
                    "data": serializer.data
                }
                return Response(response, status=status.HTTP_200_OK)

            # Check if the user is either the sender or receiver of the lunch
            elif request.user == (lunch.receiver_id or lunch.sender_id):
                serializer = LunchSerializer(lunch)
                response = {
                    "message": "Successfully fetched lunch",
                    "statusCode": status.HTTP_200_OK,
                    "data": serializer.data
                }
                return Response(response, status=status.HTTP_200_OK)
            else:
                forbidden_response = {"message": "You're not authorized to view this lunch"}
                return Response(forbidden_response, status=status.HTTP_403_FORBIDDEN)
        except Lunch.DoesNotExist:
            return Response(
                {"message": "Lunch not found"},
                status=status.HTTP_404_NOT_FOUND
            )


class ListAllLunchesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        
        user = request.user
        lunches = Lunch.objects.filter(Q(sender_id=user.id) | Q(receiver_id=user.id)).all()
        serializer = LunchSerializer(lunches, many=True)
        response = {
                "message": "successfully fetched lunches",
                "statusCode": status.HTTP_200_OK,
                "data": serializer.data
            }
        return Response(response, status=status.HTTP_200_OK)


class UserRedeemLunch(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        lunch_id = data.get('id')

        try:
            lunch = Lunch.objects.get(pk=lunch_id)
        except Lunch.DoesNotExist:
            return Response(
                {"message": "Lunch is not found"}, status=status.HTTP_404_NOT_FOUND
            )

        if request.user.id == lunch.receiver_id.id:
            
            if not lunch.redeemed:
                lunch.redeemed = True

                if request.user.org_id_id is None:
                    return Response(
                        {"error": "Only user with an organization can redeem a lunch"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                # Update the lunch credit balance for the user
                organization = Organization.objects.filter(id=request.user.org_id.id).first()
                organization_lunch_price = organization.lunch_price
                user = User.objects.get(pk=request.user.id)
                user_lunch_wallet_balance = (int(lunch.quantity) * organization_lunch_price) + int(user.lunch_credit_balance)
                user.lunch_credit_balance = int(user_lunch_wallet_balance)
                
                # Save the changes to the lunch and user objects
                lunch.save()
                user.save()
                
                # Serialize the lunch object for the response
                serializer = LunchSerializer(lunch)
                response = {"message": "Lunch redeemed successfully",
                            "data": serializer.data}
                
                return Response(response, status=status.HTTP_201_CREATED)
            else:
                bad_response = {"message": "Lunch has already been redeemed"}
                return Response(bad_response, status=status.HTTP_400_BAD_REQUEST)
        else:
            forbidden_response = {"message": "You're not authorized to redeem this lunch"}
            return Response(forbidden_response, status=status.HTTP_403_FORBIDDEN)
