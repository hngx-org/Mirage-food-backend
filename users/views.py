from rest_framework.response import Response
from .serializers import (
    UserRegistrationSerializer,
    UserListSerializer,
    UserAddBankAccountSerializer,
    UserUpdateSerializer)
from .models import User
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from django.contrib.auth import authenticate, login
from drf_yasg.utils import swagger_auto_schema
from .serializers import SearchedUserSerializer, ChangePasswordSerializer
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import update_session_auth_hash
from rest_framework.decorators import api_view, permission_classes
from rest_framework import generics, status, viewsets, response
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.core.mail import send_mail
from . import serializers
from django.http import Http404
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)


class ApiStatusView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        return Response("API is Live", status=status.HTTP_200_OK)
    

class UserRegistrationView(APIView):
    permission_classes = [
        AllowAny
    ]

    def post(self, request):
        data = request.data

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
            try:
                user = User.objects.get(email=request.data.get('email'))
                user_profile_data = {
                    "id": user.id if user.id is not None else 0,
                    "first_name": user.first_name if user.first_name else "",
                    "last_name": user.last_name if user.last_name else "",
                    "email": user.email if user.email else "",
                    "phone": user.phone if user.phone else "",
                    "organization_id": user.org_id.id if user.org_id else "",
                    "lunch_credit_balance": user.lunch_credit_balance if user.lunch_credit_balance is not None else 0,
                    }
                response.data["data"] = user_profile_data
            except User.DoesNotExist:
                response.data["data"] = {}
        return response


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


class PasswordReset(generics.GenericAPIView):
    permission_classes = [AllowAny]
    """
    Request for Password Reset Link.
    """

    serializer_class = serializers.EmailSerializer

    def post(self, request):
        """
        Create token.
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data["email"]
        user = User.objects.filter(email=email).first()
        if user:
            encoded_pk = urlsafe_base64_encode(force_bytes(user.pk))
            token = PasswordResetTokenGenerator().make_token(user)
            reset_url = reverse(
                "reset-password",
                kwargs={"encoded_pk": encoded_pk, "token": token},
            )
            reset_link = f"https://mirage-backend.onrender.com{reset_url}"

            # Send the reset link as an email to the user
            subject = "Password Reset Link"
            message = f"Click the following link to reset your password: {reset_link}"
            from_email = 'abiolaadedayo1993@gmail.com'  # Change to your email
            recipient_list = [email]

            send_mail(subject, message, from_email, recipient_list, fail_silently=False)

            return response.Response(
                {"message": "Password reset link sent to your email"},
                status=status.HTTP_200_OK,
            )
        else:
            return response.Response(
                {"message": "User doesn't exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class ResetPasswordAPI(generics.GenericAPIView):
    permission_classes = [AllowAny]
    """
    Verify and Reset Password Token View.
    """

    serializer_class = serializers.ResetPasswordSerializer

    def patch(self, request, *args, **kwargs):
        """
        Verify token & encoded_pk and then reset the password.
        """
        serializer = self.serializer_class(
            data=request.data, context={"kwargs": kwargs}
        )
        serializer.is_valid(raise_exception=True)
        return response.Response(
            {"message": "Password reset complete"},
            status=status.HTTP_200_OK,
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    if request.method == 'POST':
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if user.check_password(serializer.data.get('old_password')):
                user.set_password(serializer.data.get('new_password'))
                user.save()
                update_session_auth_hash(request, user)  # To update session after password change
                return Response({'message': 'Password changed successfully.'}, status=status.HTTP_200_OK)
            return Response({'error': 'Incorrect old password.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
