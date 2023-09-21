from django.shortcuts import render
from .models import Lunch
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import lunchSerializer
# Create your views here.

class allFreeLunchesListView(APIView):
    def get(self, request):
        lunches = Lunch.objects.all()
        serializer = lunchSerializer(lunches, many=True)
        finalData = serializer.data
      

        response_data = {
            "message": "Lunch request created successfully",
            "statusCode": status.HTTP_201_CREATED,
            "data": finalData,
        }

        return Response(response_data)