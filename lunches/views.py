<<<<<<< HEAD

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
    #permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        # Get data from the rest body
        user = request.user
        #user = User.objects.get(email="abdullahishuaibumaje@gmail.com")
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
            # skip if the user is trying to send to himself
            if receiver_id==user_id:
                continue
            else:
    
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

=======
from rest_framework.decorators import api_view
from .models import Lunch
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import LunchSerializer
from django.http import Http404
from django.shortcuts import get_object_or_404

# Create your views here.

@api_view(['DELETE'])
def delete_free_lunch(id):
        try:
                freelunch = Lunch.objects.get(id=id)
                freelunch.delete()
                return Response({'Message': 'Free Lunch Deleted'}, status=status.HTTP_200_OK)
        except Lunch.DoesNotExist:
                raise Http404("Free Lunch does not exist at the moment")


@api_view(['PATCH'])
def update_free_lunch(request, id):
        try:
                freelunch = Lunch.objects.get(id=id)
        except Lunch.DoesNotExist:
                return Response(f"No free lunch with id {id}")
        
        if request.method == "PATCH":
                serializer = LunchSerializer(freelunch, data=request.data, partial=True)
                if serializer.is_valid():
                        serializer.save()
                        return Response({
                        "message": "Lunch request created successfully",
                        "statusCode": 201,
                        "data": {
                            "receiverId": Lunch.receiver_id,
                            "senderId": Lunch.sender_id_id,
                            "quantity": Lunch.quantity,
                            "redeemed": Lunch.redeemed,
                            "note": Lunch.note,
                            "created_at": Lunch.created_at,
                            "id": Lunch.id
                        }
                    }, status=status.HTTP_201_CREATED)
                    
class allFreeLunchesListView(APIView):
    def get(self, request):
        lunches = Lunch.objects.all()
        serializer = LunchSerializer(lunches, many=True)
        finalData = serializer.data
      

        response_data = {
            "message": "Lunch request created successfully",
            "statusCode": status.HTTP_201_CREATED,
            "data": finalData,
        }

        return Response(response_data)

class LunchDetailView(APIView):
    def get(self, request, user_id, lunch_id):
        lunch = get_object_or_404(Lunch, sender_id=user_id, id=lunch_id)
        serializer = LunchSerializer(lunch)
        return Response(serializer.data)
>>>>>>> 5dec6a69ca57e6779e69eb9872c9c3600e6fc30f
