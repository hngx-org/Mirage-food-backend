from rest_framework.response import Response
from .serializers import UserRegistrationSerializer,UserListSerializer
from .models import User
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework import generics
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate, login


from .models import User
from .serializers import (
    UserRegistrationSerializer,
    UserListSerializer,
    SearchedUserSerializer,
    UserDetailsSerializer,
)
from . import workers


# Create your views here.
class LoginView(APIView):
    def post(self, request, *args, **kwargs):
    # Get username and password from the request
        email = request.data.get('email')
        password = request.data.get('password')

        # Authenticate the user
        user = authenticate(request, email=email, password=password)

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

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserListSerializer

    def get_queryset(self):
        try:
            org_id = self.kwargs['org_id']
            user_id = self.kwargs['user_id']
            user = User.objects.filter(org_id=org_id, id=user_id)
            serialize = UserListSerializer(user)
            return Response(
                {'Message': 'User Deleted',
                 'data': serialize.data
                 }, status=status.HTTP_204_NO_CONTENT)
        except:
            return Response({
                'error': 'User does not exist'
            }, status=status.HTTP_404_NOT_FOUND)

        if user is not None:
            # If authentication is successful, create or retrieve a token
            token, created = Token.objects.get_or_create(user=user)
            login(request, user)  # Optional: Log the user in
            response_data = {
                "message": "User authenticated successfully",
                "statusCode": status.HTTP_200_OK,
                "data": {
                    "access_token": token.key,
                    "email": user.email,
                    "id": user.id,
                    "isAdmin": user.is_staff  # Assuming 'is_staff' signifies admin status
                }
            }
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response(
                {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )


class DeleteUserView(APIView):

    def get_user_by_pk(self, pk):
        try:
            return User.objects.get(pk=id)
        except:
            return Response({
                'error': 'User does not exist.'
            }, status=status.HTTP_404_NOT_FOUND)

    def delete_user(self, request, pk):
        user = self.get_user_by_pk(pk=id)
        user.delete()
        return Response({'Message': 'User Deleted'}, status=status.HTTP_204_NO_CONTENT)


class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]
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


