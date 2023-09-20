from django.shortcuts import render
from rest_framework.decorators import api_view
from .models import Lunch
from rest_framework.response import Response
from rest_framework import status

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
