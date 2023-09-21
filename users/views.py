from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from .serializers import LoginSerializer, CustomUserSerializer
from .models import User
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login


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
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)