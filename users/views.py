from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import User
from .serializers import UserListSerializer

# Create your views here.

class UserListViewSet(APIView):
    @swagger_auto_schema(
            operation_summary="List all users",
            responses={status.HTTP_200_OK: openapi.Response("List of users", UserListSerializer(many=True))}
    )
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

    @swagger_auto_schema(
            operation_summary="Get a user's details",
            responses={
                status.HTTP_200_OK: openapi.Response("User details", UserListSerializer()),
                status.HTTP_404_NOT_FOUND: "User does not exist",
                status.HTTP_403_FORBIDDEN: "Permission denied",
                }
    )
    def get(self, pk):
        try:
            return UserListSerializer(User.objects.get(pk=id)).data
        except:
            return Response({
                'error': 'User does not exist'
            }, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
            operation_summary="Delete a user",
            responses={
                status.HTTP_204_NO_CONTENT: "User Deleted",
                status.HTTP_404_NOT_FOUND: "User does not exist",
                status.HTTP_403_FORBIDDEN: "Permission denied",
                }
    )
    def delete(self, request, pk):
        user = self.get_user_by_pk(pk=id)
        user.delete()
        return Response({'Message': 'User Deleted'}, status=status.HTTP_204_NO_CONTENT)
