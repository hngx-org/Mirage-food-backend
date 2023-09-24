from rest_framework.response import Response
from .serializers import UserRegistrationSerializer,UserListSerializer, UserAddBankAccountSerializer
from .models import User
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework import generics
from rest_framework.permissions import AllowAny , IsAuthenticated, IsAdminUser
from django.contrib.auth import authenticate, login

from .serializers import SearchedUserSerializer
from django.http import Http404

# Create your views here.


class ApiStatusView(APIView):
    permission_classes = [ AllowAny]

    def  get(self, request):
        return Response("API is Live", status=status.HTTP_200_OK)


class LoginView(APIView):
    def post(self, request, *args, **kwargs):
    # Get username and password from the request
        email = request.data.get('email')
        password = request.data.get('password')

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
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)



class UserAddBankAccountView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def patch(self, request, id):
        try:
            user = User.objects.get(pk=id)

            data = request.data
            serializer = UserAddBankAccountSerializer(user, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                response = {
                    "status": "success",
                    "message": "successfully created bank account",

                }
                return Response(response, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            response = {
                "status": "error",
                "message": "User does not exist",
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)



class RetrieveDeleteUserView(APIView):
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
        
    def get(self, request, id):
        try:
            user = User.objects.get(pk=id)
            serializer = UserListSerializer(user)
            response = {
                "status": "success",
                "message": "User retrieved successfully",
                "data": serializer.data
            }
            return Response(response, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            response = {
                "status": "error",
                "message": "User does not exist",
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)







# class UserRegistrationView(generics.CreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserRegistrationSerializer
#     permission_classes = [AllowAny]

class UserRegistrationView(APIView):
    permission_classes = [
        AllowAny
    ]

    def post(self, request):
        data = request.data
        lunch_credit_balance = 1000
        data['lunch_credit_balance'] = lunch_credit_balance

        serializer = UserRegistrationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            response = {
                "status": "success",
                "message": "User created successfully",
                "data": serializer.data,
            }
            return Response(response, status=status.HTTP_201_CREATED)

        bad_response = {
            "status": "error",
            "message": "Bad request",
            "data": serializer.errors,
        }
        return Response(bad_response, status=status.HTTP_400_BAD_REQUEST)



class UserListViewSet(APIView):
    permission_classes = [IsAdminUser]

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


class SearchUserView(APIView):
    permission_classes = [IsAuthenticated]
    "Api view accepting either a name (first or last) or email parameter to search for a user"

    def get_object(self, param:str):
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

    def get(self, request, name_or_email:str, *args, **kwargs):
        instance = self.get_object(name_or_email)
        serializer = SearchedUserSerializer(instance)
        return Response({
            'message': 'User Found',
            'statusCode': status.HTTP_200_OK,
            'data': serializer.data
        }, status=status.HTTP_200_OK)

