<<<<<<< HEAD
<<<<<<< HEAD
from django.shortcuts import render
from rest_framework.views import APIView
from .models import User
from rest_framework.response import Response
=======
>>>>>>> 5dec6a69ca57e6779e69eb9872c9c3600e6fc30f
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User
from .serializers import UserListSerializer

# Create your views here.

<<<<<<< HEAD
class DeleteUserView:

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
=======
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User

from .serializers import UserListSerializer

=======
>>>>>>> 5dec6a69ca57e6779e69eb9872c9c3600e6fc30f
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
<<<<<<< HEAD
>>>>>>> 1729f3a5f3e94012b6cbf58fde706afda62051b6
=======

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
>>>>>>> 5dec6a69ca57e6779e69eb9872c9c3600e6fc30f
