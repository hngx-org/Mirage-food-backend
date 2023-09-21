from rest_framework.decorators import api_view
from .models import Lunch
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import LunchSerializer
from django.http import Http404
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
