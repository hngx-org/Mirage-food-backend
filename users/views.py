from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User

from .serializers import UserListSerializer

class UserRetrieveUpdateSet(APIView):
    def get_object(self, pk):
        """
        Gets a user object with the given pk
        """
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            return None

    def get(self, request, pk, format=None):
        """
        Gets user details
        """
        user = User.get_object(pk)
        serializer = UserListSerializer(user, many=True)

        return Response({
            "message" : "successfully fetched users",
            "statusCode": status.HTTP_200_OK,
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        """
        Updates user details
        """
        user = self.get_object(pk)
        serializer = UserListSerializer(user, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "message" : "successfully updated user",
                "statusCode": status.HTTP_200_OK,
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    