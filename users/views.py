from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User

from .serializers import UserListSerializer

class UserListViewSet(APIView):
    def get(self, request, *args, **kwargs):
        """
        Get user details
        """
        queryset = User.objects.all()
        serializer = UserListSerializer(queryset, many=True)

        return Response({
            "message" : "successfully fetched users",
            "statusCode": status.HTTP_200_OK,
            "data": serializer.data
        }, status=status.HTTP_200_OK)
    
def put(selt,request, *args, **kwargs):
        
        '''
        updating user details
        '''
        queryset = User.objects.all()
        





