from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Lunch
from .serializers import LunchSerializer


# Create your views here.
class UpdateLunch(APIView):
    def post(self, request):
        # Get the authenticated user
        user = request.user

        # Get or create the lunch wallet for the user
        lunch_wallet, created = Lunch.objects.get_or_create(user=user)

        # Deserialize the data from the request
        serializer = LunchSerializer(lunch_wallet, data=request.data)

        if serializer.is_valid():
            # Update the lunch wallet balance
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUES)