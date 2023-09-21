from django.shortcuts import render
from rest_framework.decorators import api_view
from .models import Lunch
from rest_framework.response import Response
from rest_framework import status
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
