from rest_framework.response import Response
from django.http import Http404
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework import generics
from rest_framework.permissions import AllowAny , IsAuthenticated
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
        email = request.data.get("email")
        password = request.data.get("password")

        # Authenticate the user
        user = authenticate(request, email=email, password=password)

        if user is not None:
            # If authentication is successful, create or retrieve a token
            token, created = Token.objects.get_or_create(user=user)
            login(request, user)  # Optional: Log the user in
            response_data = {
                "message": "User authenticated successfully",
                "statusCode": status.HTTP_200_OK,
                "access_token": token.key,
                "email": user.email,
                "id": user.id,
                "isAdmin": user.is_staff  # Assuming 'is_staff' signifies admin status
                }
 
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response(
                {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )


# class DeleteUserView(APIView):

#     def get_user_by_pk(self, pk):
#         try:
#             return User.objects.get(pk=id)
#         except:
#             return Response({
#                 'error': 'User does not exist.'
#             }, status=status.HTTP_404_NOT_FOUND)

#     def delete_user(self, request, pk):
#         user = self.get_user_by_pk(pk=id)
#         user.delete()
#         return Response({'Message': 'User Deleted'}, status=status.HTTP_204_NO_CONTENT)

class DeleteUserView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, id):

        try:
            user = User.objects.get(pk=id)
            user.delete()
            response = {
                "status": "success",
                "message": "User deleted successfully",
            }
            return Response(response, status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            error_response = {
                "status": "error","message": "User does not exist",
            }
            return Response(error_response, status=status.HTTP_404_NOT_FOUND)






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

        return Response(
            {
                "message": "successfully fetched users",
                "statusCode": status.HTTP_200_OK,
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


class SearchUserView(APIView):
    "Api view accepting either a name (first or last) or email parameter to search for a user"

    def get_object(self, param: str):
        try:
            return User.objects.get(first_name=param)
        except User.DoesNotExist:
            try:
                return User.objects.get(last_name=param)
            except User.DoesNotExist:
                try:
                    return User.objects.get(email=param)
                except User.DoesNotExist:
                    raise Http404

    def get(self, request, name_or_email: str, *args, **kwargs):
        instance = self.get_object(name_or_email)
        serializer = SearchedUserSerializer(instance)
        return Response(
            {
                "message": "User Found",
                "statusCode": status.HTTP_200_OK,
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


class UserDetailView(APIView):
    def get(self, request):
        """
        Get user details
        """
        user = request.user
        user_details = workers.UserWorker.get_user_details(user.id)
        serializer = UserDetailsSerializer(user_details)
        return Response(
            {
                "message": "User data fetched",
                "statusCode": status.HTTP_200_OK,
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
            message="User data fetched",
        )
