from django.shortcuts import get_object_or_404, get_list_or_404
from .models import User
from .serializers import UserSerializer, UserListSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

class UserViewSet(APIView):
    def get_user(self, request, pk, *args, **kwargs):
        """
        Get a particular user from user_id, name or email
        """
        try:
            user = get_object_or_404(User, id=pk)
            serializer = UserSerializer(user, many=True)
        except:
            user = get_list_or_404(User, first_name=pk)
            serializer = UserSerializer(user)
        return Response({
            "message": "User found",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

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

class DeleteUserView(APIView):

    def get_user_by_pk(self, pk):
        try:
            return User.objects.get(pk=id)
        except:
            return Response({
                'error': 'User does not exist'
            }, status=status.HTTP_404_NOT_FOUND)


    def delete_user(self, request, pk):
        user = self.get_user_by_pk(pk=id)
        user.delete()
        return Response({'Message': 'User Deleted'}, status=status.HTTP_204_NO_CONTENT)
