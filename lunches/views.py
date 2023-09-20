from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Lunch  # Import your Lunch model
from .serializers import LunchSerializer  # Import your LunchSerializer

class CreateFreeLunchAPIView(APIView):
    def post(self, request, *args, **kwargs):
        # Get data from the request body
        sender = 1 # Assuming request.user is the sender
        receivers = request.data.get('receivers', [])
        quantity = request.data.get('quantity', 0)
        note = request.data.get('note', '')

        # Validate the data as needed
        if not receivers:
            return Response({"message": "Receivers field is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Prevent the user from sending lunch to themselves
        if sender.id in receivers:
            return Response({"message": "You cannot send lunch to yourself"}, status=status.HTTP_400_BAD_REQUEST)

        data = []

        for receiver_id in receivers:
            try:
                lunch = Lunch.objects.create(sender=sender, receiver=receiver_id, note=note, quantity=quantity)
                lunch_serialized = LunchSerializer(lunch)
                data.append(lunch_serialized.data)
            except Exception as e:
                error = str(e)
                return Response({'message': error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"message": "Lunch request created successfully", "data": data}, status=status.HTTP_201_CREATED)
