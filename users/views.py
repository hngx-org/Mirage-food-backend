from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import User

from .serializers import UserListSerializer

class UserListViewSet(APIView):
    @swagger_auto_schema(
            operation_summary="List all users",
            responses={200: openapi.Response("List of albums", UserListSerializer(many=True))}
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