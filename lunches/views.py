from rest_framework.views import APIView 
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Lunch
from .serializers import LunchSerializer
from django.http import Http404

@api_view(['GET'])
def user_lunch_list(request, id):
    try:
        freelunch = Lunch.objects.filter(receiver_id=id)
        serializer = LunchSerializer(freelunch, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Lunch.DoesNotExist:
        raise Http404("Free lunch does not exist at the moment")
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
def delete_free_lunch(request, id):
    try:
        freelunch = Lunch.objects.get(id=id)
        freelunch.delete()
        return Response({'Message': 'Free Lunch Deleted'}, status=status.HTTP_200_OK)
    except Lunch.DoesNotExist:
        raise Http404("Free lunch does not exist at the moment")

@api_view(['PATCH'])
def update_free_lunch(request, id):
    try:
        freelunch = Lunch.objects.get(id=id)
    except Lunch.DoesNotExist:
        return Response(f"No free lunch with id {id}", status=status.HTTP_404_NOT_FOUND)
    
    if request.method == "PATCH":
        serializer = LunchSerializer(freelunch, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class allFreeLunchesListView(APIView):
    def get(self, request):
        lunches = Lunch.objects.all()
        serializer = LunchSerializer(lunches, many=True)
        return Response(serializer.data)

class LunchDetailView(APIView):
    def get(self, request, user_id, lunch_id):
        lunch = get_object_or_404(Lunch, sender_id=user_id, id=lunch_id)
        serializer = LunchSerializer(lunch)
        return Response(serializer.data)
