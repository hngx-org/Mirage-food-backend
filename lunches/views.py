from django.shortcuts import render
from rest_framework.decorators import api_view
from .models import Lunch
from .serializer import LunchSerializer
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.http import Http404

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
    try:
        freelunch = Lunch.objects.get(id=id)
        freelunch.delete()
        return Response({'Message': 'Free Lunch Deleted'}, status=status.HTTP_200_OK)
    except Lunch.DoesNotExist:
        raise Http404("Free lunch does not exist at the moment")
