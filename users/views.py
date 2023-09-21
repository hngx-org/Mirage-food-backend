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
        Update the user details with the below lines of codes
        """
        user = self.get_object(pk)
        serializer = UserListSerializer(user, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "message" : "successfully updated user information",
                "statusCode": status.HTTP_200_OK,
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# Check the comment at the last line of this file.

# '''
# the PUT AND PATCH functionality
# '''

# class UpdateUserDetailsView(RetrieveUpdateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserListSerializer

#     def put(self, request, *args, **kwargs):
#         user_id = kwargs.get('pk')

#         # Checking if the user exists
#         try:
#             user = User.objects.get(pk=user_id)
#         except User.DoesNotExist:
#             return Response({"status": False, "message": f"The user with user_id {user_id} does not exist."},
#                             status=status.HTTP_404_NOT_FOUND)

#         serializer = self.get_serializer(user, data=request.data, partial=True)

#         if serializer.is_valid():
#             serializer.save()
#             return Response({"status": True, "message": f"Person with user_id {user_id} updated successfully."},
#                             status=status.HTTP_200_OK)
#         else:
#             return Response({"status": False, "message": "Invalid data provided."}, status=status.HTTP_400_BAD_REQUEST)

# I commented it because I am not sure if we need it or not. And I think we can make do with the above code. PATCH is not part of our task