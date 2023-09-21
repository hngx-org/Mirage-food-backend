from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User
from .serializers import UserListSerializer


# Beginning of the user update
class UserRetrieveUpdateSet(APIView):
    def get_object(self, id):
        """
        Gets a user object with the given pk
        """
        try:
            return User.objects.get(id=id)
        except User.DoesNotExist:
            return None

    def get(self, request,id=None, format=None):
        """
        Gets user details
        """
        user = self.get_object(id)
        if user is None:
            return Response({
                "message": f"User with id {id} does not exist.",
                "statusCode": status.HTTP_404_NOT_FOUND,
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = UserListSerializer(user)

        return Response({
            "message": "Successfully fetched user",
            "statusCode": status.HTTP_200_OK,
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def put(self, request, id, format=None):
        """
        Update the user details
        """
        user = self.get_object(id)
        serializer = UserListSerializer(user, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Successfully updated user information",
                "statusCode": status.HTTP_200_OK,
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# the patch function
    '''
    The patch method is responsible for performing the patch operation on the endpoint.
    That it make it possible to partially update the user details
    '''

    def patch(self, request, id, format=None):
        """
        Partially update user details
        """
        user = self.get_object(id)

        if user is None:
            return Response({
                "message": f"User with pk {id} does not exist.",
                "statusCode": status.HTTP_404_NOT_FOUND,
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = UserListSerializer(user, data=request.data, partial=True)  # Use partial=True to enable partial updates

        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Successfully partially updated user information",
                "statusCode": status.HTTP_200_OK,
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)