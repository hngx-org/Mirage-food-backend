from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Lunch
from .serializers import LunchSerializer

class CreateFreeLunchAPIView(APIView):
    def post(self, request, format=None):
        serializer = LunchSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"free food sent",
                            "data":serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"message":"Bad request",
                        "error":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
