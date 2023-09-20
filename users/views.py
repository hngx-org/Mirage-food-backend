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
        serializer_class = UserListSerializer()
        user_id = kwargs.get('pk')

    # checking if the user exist

        try:
            User = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({"status": False, "message": f"The user with user_id {user_id} does not exist."},
                            status=status.HTTP_404_NOT_FOUND)
        serializer = serializer_class(User, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"status": True, "message": f"Person with user_id {user_id} updated successfully."},
                            status=status.HTTP_200_OK)
        else:
            return Response({"status": False, "message": "Invalid data provided."}, status=status.HTTP_400_BAD_REQUEST)

        





