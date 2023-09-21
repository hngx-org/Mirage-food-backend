from rest_framework.decorators import api_view
from .models import Lunch
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404 
from .serializers import LunchSerializer

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
                        return Response({"Lunch updated successfully": serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Create your views here.
@api_view(['GET'])
def get_a_lunch(request, id):
    """Returns an existing lunch by id"""

    try:
        lunch = Lunch.objects.get(id=id)
    except Lunch.DoesNotExist:
        return Response(
            {"error": "Lunch not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    return Response({
        "message": "Lunch request created successfully",
        "statusCode": 201,
        "data": {
            "receiverId": lunch.receiver_id,
            "senderId": lunch.sender_id_id,
            "quantity": lunch.quantity,
            "redeemed": lunch.redeemed,
            "note": lunch.note,
            "created_at": lunch.created_at,
            "id": lunch.id
        }
    }, status=status.HTTP_201_CREATED)
