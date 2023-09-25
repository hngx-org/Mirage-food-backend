from rest_framework.response import Response
from .serializers import (
    UserRegistrationSerializer,
    UserListSerializer,
    UserAddBankAccountSerializer,
    UserUpdateSerializer, UserProfilePictureSerializer)
from .models import User
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from django.contrib.auth import authenticate, login
from drf_yasg.utils import swagger_auto_schema
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)


from .serializers import SearchedUserSerializer
from django.http import Http404

# Create your views here.
class UserLoginView(TokenObtainPairView):
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        operation_summary="Login a user",
        responses={
            200: "successfully logged in",
            400: 'Bad Request'},
    )

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            user = User.objects.get(email=request.data['email'])

            user_profile_data = {
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "phone": user.phone,
                "organization_id": user.org_id.id,
                "lunch_credit_balance": user.lunch_credit_balance,
            }
            response.data["data"] = user_profile_data
        return response




class DeleteUserView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def delete(self, request, pk):

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
                "status": "error",
                "message": "User does not exist",
            }
            return Response(error_response, status=status.HTTP_404_NOT_FOUND)


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        try:
            user = User.objects.get(pk=id)
            if request.user.is_staff:
                serializer = UserListSerializer(user)
                response = {
                    "status": "success",
                    "message": "User retrieved successfully",
                    "data": serializer.data
                }
                return Response(response, status=status.HTTP_200_OK)
            if user == request.user:
                serializer = UserListSerializer(user)
                response = {
                    "status": "success",
                    "message": "User retrieved successfully",
                    "data": serializer.data
                }
                return Response(response, status=status.HTTP_200_OK) 
            else:
                response = {
                        "status": "error",
                        "message": "You are not authorized to view this user",
                        }
                return Response(response, status=status.HTTP_403_FORBIDDEN)    
        except User.DoesNotExist:
            response = {
                "status": "error",
                "message": "User does not exist",
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
    
    def patch(self, request, id):
        try:
            user = User.objects.get(pk=id)
            if request.user.is_staff:
                data = request.data
                serializer = UserUpdateSerializer(user, data=data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    response = {
                        "status": "success",
                        "message": "User updated successfully",
                        "data": serializer.data
                    }
                    return Response(response, status=status.HTTP_200_OK)
            if user == request.user:
                data = request.data
                serializer = UserUpdateSerializer(user, data=data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    response = {
                        "status": "success",
                        "message": "User updated successfully",
                        "data": serializer.data
                    }
                    return Response(response, status=status.HTTP_200_OK)
            else:
                response = {
                        "status": "error",
                        "message": "You are not authorized to update this user"
                        }
                return Response(response, status=status.HTTP_403_FORBIDDEN)    
        except User.DoesNotExist:
            response = {
                "status": "error",
                "message": "User does not exist",
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)

class UserProfileUpdateView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserProfilePictureUpdateView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfilePictureSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserAddBankAccountView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_summary="Add bank account details",
        request_body=UserAddBankAccountSerializer,
        responses={
            201: "successfully created bank account",
            400: 'Bad Request'},
    )

    def patch(self, request: Request, id):
       
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
            bad_response = {
                "status": "error",
                "message": "Bad request",
                "data": serializer.errors,
            }
            return Response(bad_response, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            response = {
                "status": "error",
                "message": "User does not exist",
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)





        
    # def get_user_by_pk(self, pk):
    #     try:
    #         return User.objects.get(pk=id)
    #     except:
    #         return Response({
    #             'error': 'User does not exist.'
    #         }, status=status.HTTP_404_NOT_FOUND)

    # def delete_user(self, request, pk):
    #     user = self.get_user_by_pk(pk=id)
    #     user.delete()
    #     return Response({'Message': 'User Deleted'}, status=status.HTTP_204_NO_CONTENT)


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

