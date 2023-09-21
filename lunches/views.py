
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from users.models import User
from .models import Lunch
from .serializers import LunchSerializer
import ast
from organization.models import Organization #OrganizationLunchWallet
from rest_framework.authentication import SessionAuthentication  # Import the SessionAuthentication class if you want to use it for a specific view
from rest_framework.permissions import AllowAny

class CreateFreeLunchAPIView(APIView):
    #
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        # Get data from the rest body
        #user = request.user
        user = User.objects.get(email="abdullahishuaibumaje@gmail.com")
        receivers = request.data.get('receivers')
        try:
            receivers_list = ast.literal_eval(receivers)
            quantity = request.data.get('quantity', 0)
            note = request.data.get('note', '')
        except Exception as e:
            error=str(e)
            return Response({'message':error})

        # Validate the data as needed
        if not receivers_list:
            return Response({"message": "Receivers field is required"}, status=status.HTTP_400_BAD_REQUEST)

        data = []
        try:
            organization_id = user.org_id.id
        except:

            return  Response({'message':"user does not have an organisation"})

        try:
            organization = Organization.objects.get(id=organization_id)
            #lunch_wallet = OrganizationLunchWallet.objects.get(org_id=organization)
        except Organization.DoesNotExist:
            return Response({"message": "Organization not found"}, status=status.HTTP_400_BAD_REQUEST)
        #except OrganizationLunchWallet.DoesNotExist:
            #return Response({"message": "Organization lunch wallet not found"}, status=status.HTTP_400_BAD_REQUEST)

        for receiver_id in receivers_list:
            try:
                # Attempt to fetch the receiver instance based on the receiver_id
                receiver = User.objects.get(id=int(receiver_id))

                # Calculate the lunch cost
                price = organization.lunch_price
                total_cost = int(quantity)* int(price)

                # Check if the organization has sufficient balance
                #if lunch_wallet.balance < total_cost:
                    #return Response({'detail': 'Insufficient balance in the organization lunch wallet.'}, status=status.HTTP_400_BAD_REQUEST)

                # Create the Lunch object with the receiver instance
                lunch = Lunch.objects.create(sender_id=user, receiver=receiver, note=note, quantity=quantity)

                # Update the organization lunch wallet balance
                #lunch_wallet.balance -= total_cost
                #lunch_wallet.save()

                # Serialize and append the lunch data
                lunch_serialized = LunchSerializer(lunch)
                data.append(lunch_serialized.data)
            except User.DoesNotExist:
                return Response({"message": f"User with ID {receiver_id} does not exist"}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                error = str(e)
                return Response({'message': error}, status=status.HTTP_400_BAD_REQUEST)

        #lunch_balance = lunch_wallet.balance
        return Response({"message": "Lunch request created successfully",
                         "statusCode": 201,
                         "data": data})

# from django.shortcuts import render
# from rest_framework.decorators import api_view
# from .models import Lunch
# from rest_framework.response import Response
# from rest_framework import status

# # Create your views here.
# @api_view(['GET'])
# def get_a_lunch(request, id):
#     """Returns an existing lunch by id"""

#     try:
#         lunch = Lunch.objects.get(id=id)
#     except Lunch.DoesNotExist:
#         return Response(
#             {"error": "Lunch not found"},
#             status=status.HTTP_404_NOT_FOUND
#         )

#     return Response({
#         "message": "Lunch request created successfully",
#         "statusCode": 201,
#         "data": {
#             "receiverId": lunch.receiver_id,
#             "senderId": lunch.sender_id_id,
#             "quantity": lunch.quantity,
#             "redeemed": lunch.redeemed,
#             "note": lunch.note,
#             "created_at": lunch.created_at,
#             "id": lunch.id
#         }
#     }, status=status.HTTP_201_CREATED)
