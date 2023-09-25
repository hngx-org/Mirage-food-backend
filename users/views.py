from rest_framework.response import Response
from django.http import Http404
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate, login
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.generics import RetrieveUpdateAPIView


from .models import User
from .serializers import (
    UserRegistrationSerializer,
    UserListSerializer,
    SearchedUserSerializer,
    UserDetailsSerializer,
    RedeemLunchSerializer,
    UserUpdateSerializer,

)
from . import workers


from django.urls import reverse
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import os
import ssl

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


# This logout view only blacklists the refresh token, and has no
# effect on the access token. In the future, the access token's
# lifespan would be reduced to restrict acess to both tokens
# within a reasonable timeframe.
class LogoutView(APIView):
    """View that accepts a refresh token and blacklists it as a form of logout mechanism"""

    # So authentication credentials are not required to blacklist a token
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        refresh_token = request.data.get(
            'refresh_token') or request.data.get('refresh')
        if not refresh_token:
            return Response({'error': 'Request token not provided'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'message': 'User Successfully logged out'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

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
                "status": "error", "message": "User does not exist",
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


class RequestPasswordResetView(generics.GenericAPIView):
    """
    View that sends the user an email providing them with the reset token
    associated with their user account.
    """

    from_email = 'rorobitega.hng.mirage@gmail.com'
    from_passwd = 'wptjcdiycgwagnsu'
    queryset = User.objects.all()
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    lookup_field = 'email'

    def send_email(self, to_email, reset_token):
        em = MIMEMultipart()
        em['From'] = "Mirage Lunch App"
        em['Subject'] = "Password reset link"
        em.attach(MIMEText(f"""
Hello User, You requested for a password reset. <br/> 
Here is your reset token: <b>{reset_token}</b> 
<br/><br/>
If this was not you, kindly ignore this email.
<br/>
Stay Kind :)""", 'html'))

        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=ssl.create_default_context()) as smtp:
            smtp.login(self.from_email, self.from_passwd)
            smtp.sendmail(self.from_email, to_email, em.as_string())

        return True

    # this view sends an email to a user providing them with the reset token
    # associated with their
    def get(self, request, *args, **kwargs):
        user = self.get_object()
        new_token = User.generate_reset_token(5)
        user.password_reset_token = new_token
        user.save()
        self.send_email(kwargs['email'], new_token)
        return Response({'message': 'Email successfully sent!'}, status=status.HTTP_200_OK)


class ConfirmResetTokenView(generics.GenericAPIView):
    "View that confirms the token the user provides is the one associated with their account."

    queryset = User.objects.all()
    lookup_field = 'email'
    queryset = User.objects.all()
    permission_classes = [AllowAny]

    def get(self, request, token, *args, **kwargs):
        user = self.get_object()
        if user.password_reset_token == token:
            return Response({'message': 'Token Authorized'}, status=status.HTTP_200_OK)
        return Response({'message': 'Invalid token!'}, status=status.HTTP_401_UNAUTHORIZED)


class PasswordResetView(generics.GenericAPIView):
    "View that resets the user's password"

    queryset = User.objects.all()
    lookup_field = 'password_reset_token'
    lookup_url_kwarg = 'token'
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        user = self.get_object()
        passwd1, passwd2 = request.data.get(
            'password1'), request.data.get('password2')
        if passwd1 != passwd2:
            return Response({'message': "Passwords do not match!"}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(passwd1)
        # generate a fresh token for the user
        user.password_reset_token = User.generate_reset_token(5)
        user.save()
        return Response({'message': 'Password reset successfully :)'}, status=status.HTTP_200_OK)


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


class RedeemLunchView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = RedeemLunchSerializer(data=request.data)
        if serializer.is_valid():
            # Get the list of user IDs from the serializer
            user_ids = serializer.validated_data.get('ids')

            # Assuming you have a function to handle lunch credit redemption in your User model
            for user_id in user_ids:
                user = User.objects.get(pk=user_id)
                user.redeem_lunch_credit()  # Implement this method in your User model

            return Response(
                {
                    "message": "success",
                    "statusCode": status.HTTP_200_OK,
                    "data": None
                },
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )


class UserUpdateView(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
