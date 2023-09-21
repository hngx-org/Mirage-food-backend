
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from users.models import User
from .models import Lunch
from .serializers import LunchSerializer
import ast
from organization.models import Organization, OrganizationLunchWallet
from rest_framework.authentication import SessionAuthentication  # Import the SessionAuthentication class if you want to use it for a specific view
from rest_framework.permissions import AllowAny

class CreateFreeLunchAPIView(APIView):
    #
    # permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        # Get data from the rest body
        #user = request.user
        user = User.objects.get(email="abdullahishuaibumaje@gmail.com")
        user_id=user.id
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
        
        for receiver_id in receivers_list:
    
            try:
                # Attempt to fetch the receiver instance based on the receiver_id
                receiver = User.objects.get(id=int(receiver_id))

                # Create the Lunch object with the receiver instance
                lunch = Lunch.objects.create(sender_id=user, receiver=receiver, note=note, quantity=quantity)
                # Serialize and append the lunch data
                lunch_serialized = LunchSerializer(lunch)
                data.append(lunch_serialized.data)
            except User.DoesNotExist:
                return Response({"message": f"User with ID {receiver_id} does not exist"}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                error = str(e)
                return Response({'message': error}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "Lunch request created successfully",
                         "statusCode": 201,
                         "data": data})

