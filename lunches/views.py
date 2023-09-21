from rest_framework.decorators import api_view
from .models import Lunch
from .serializer import LunchSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
<<<<<<< HEAD
from django.shortcuts import get_object_or_404
=======
from .serializers import LunchSerializer
>>>>>>> 5dec6a69ca57e6779e69eb9872c9c3600e6fc30f
from django.http import Http404
from django.shortcuts import get_object_or_404

@api_view(['GET'])
def user_lunch_list(request, id):
    try:
        freelunch = Lunch.object.filter(reciever_id=id)
        serializer = Lunchserializer(freelunch, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Lunch.DoesNotExist:
        raise Http404("Free lunch does not exist at the moment")
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
def delete_free_lunch(id):
<<<<<<< HEAD
    try:
        freelunch = Lunch.objects.get(id=id)
        freelunch.delete()
        return Response({'Message': 'Free Lunch Deleted'}, status=status.HTTP_200_OK)
    except Lunch.DoesNotExist:
        raise Http404("Free lunch does not exist at the moment")
=======
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
