
from rest_framework.views import APIView

from .models import User
from .serializers import UserListSerializer

# Create your views here.
from rest_framework import generics, permissions
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from .serializers import LoginSerializer, UserSerializer
from rest_framework.authtoken.models import Token


class LoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):

        email = request.data.get("email")
        password = request.data.get("password")

        if not self.request.data.get("email") or not self.request.data.get("password"):
            raise ValidationError(
                {"message": "Email and Password must be provided"})

        user = User.objects.filter(email=email).first()

        if not user:
            raise ValidationError({"message": "User does not exist"})

        if not user.is_active:
            raise ValidationError({"message": "User not active"})

        if user.check_password(password):
            raise ValidationError({"message": "Invalid Credentials"})

        token, created = Token.objects.get_or_create(user=user)

        token_key = ""
        if token:
            token_key = token.key
        elif created:
            token_key = created.key

        response_data = dict()
        response_data["message"] = "success"
        response_data["token"] = token_key
        response_data["user"] = UserSerializer(user).data

        return Response(response_data)


class UserListViewSet(APIView):
    def get(self, request, *args, **kwargs):
        """
        Get user details
        """
        queryset = User.objects.all()
        serializer = UserListSerializer(queryset, many=True)

        return Response({
            "message": "successfully fetched users",
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
