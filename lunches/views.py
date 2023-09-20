
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.models import User
from .models import Lunch
from .serializers import LunchSerializer
import ast
from organization.models import Organization, OrganizationLunchWallet

class CreateFreeLunchAPIView(APIView):
    authentication_classes = [JWTAuthentication]  # Use JWT Authentication
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # Get data from the request body
        user = request.user
        receivers = request.data.get('receivers')
        receivers_list = ast.literal_eval(receivers)
        quantity = request.data.get('quantity', 0)
        note = request.data.get('note', '')

        # Validate the data as needed
        if not receivers:
            return Response({"message": "Receivers field is required"}, status=status.HTTP_400_BAD_REQUEST)

        data = []
        organization_id = 1  # Assuming organization ID is 1

        try:
            organization = Organization.objects.get(id=organization_id)
            lunch_wallet = OrganizationLunchWallet.objects.get(org_id=organization)
        except Organization.DoesNotExist:
            return Response({"message": "Organization not found"}, status=status.HTTP_400_BAD_REQUEST)
        except OrganizationLunchWallet.DoesNotExist:
            return Response({"message": "Organization lunch wallet not found"}, status=status.HTTP_400_BAD_REQUEST)

        for receiver_id in receivers_list:
            try:
                # Attempt to fetch the receiver instance based on the receiver_id
                receiver = User.objects.get(id=int(receiver_id))

                # Calculate the lunch cost
                price = organization.lunch_price
                total_cost = quantity * price

                # Check if the organization has sufficient balance
                if lunch_wallet.balance < total_cost:
                    return Response({'detail': 'Insufficient balance in the organization lunch wallet.'}, status=status.HTTP_400_BAD_REQUEST)

                # Create the Lunch object with the receiver instance
                lunch = Lunch.objects.create(sender=user, receiver=receiver, note=note, quantity=quantity)

                # Update the organization lunch wallet balance
                lunch_wallet.balance -= total_cost
                lunch_wallet.save()

                # Serialize and append the lunch data
                lunch_serialized = LunchSerializer(lunch)
                data.append(lunch_serialized.data)
            except User.DoesNotExist:
                return Response({"message": f"User with ID {receiver_id} does not exist"}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                error = str(e)
                return Response({'message': error}, status=status.HTTP_400_BAD_REQUEST)

        lunch_balance = lunch_wallet.balance
        return Response({"message": "Lunch request created successfully",
                         "statusCode": 201,
                         "walletBalance": lunch_balance,
                         "data": data})

