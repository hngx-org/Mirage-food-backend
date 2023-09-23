from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from users.models import User
from organization.models import Organization, OrganizationLunchWallet
from .models import Lunch
from .serializers import LunchSerializer


class CreateFreeLunchAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):

        data = request.data

        receiver_id = data.get('receiver_id')
        quantity = data.get('quantity')
        note = data.get('note')
        org_id_id = data.get('org_id_id')
        sender_id = data.get('sender_id')

        # Get the user making the request
        user = request.user

        # Check if the user has enough lunch credits
        if int(user.lunch_credit_balance) < int(quantity):
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
            serializer = LunchSerializer(data=data)
            print(serializer)
            
            if serializer.is_valid():
        
                # Update the lunch credit balance for the user
                
                user.lunch_credit_balance = int(user.lunch_credit_balance) - (int(quantity)*100)
                user.save()
                
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


class RetrieveLunchView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        try:

            lunch = Lunch.objects.get(pk=id)
            serializer = LunchSerializer(lunch)
            response = {
                "message": "successfully fetched lunches",
                "statusCode": status.HTTP_200_OK,
                "data": serializer.data
            }
            return Response(response, status=status.HTTP_200_OK)
        except Lunch.DoesNotExist:
            return Response(
                {"message": "Lunches not found"},
                status=status.HTTP_404_NOT_FOUND
            )

class ListAllLunchesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        
        lunches = Lunch.objects.all()
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
                
                # Update the lunch credit balance for the user
                user = User.objects.get(pk=request.user.id)
                user_lunch_wallet_balance = (int(lunch.quantity) * 100) + int(user.lunch_credit_balance)
                user.lunch_credit_balance = user_lunch_wallet_balance
                
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
