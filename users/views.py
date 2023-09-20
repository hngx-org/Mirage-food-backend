from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from .serializers import LoginSerializer, CustomUserSerializer
from .models import User
from rest_framework.authtoken.models import Token

class LoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):

        email = request.data.get("email")
        password = request.data.get("password")
 
        if not self.request.data.get("email") or not self.request.data.get("password"):
            raise ValidationError({"message": "Email and Password must be provided"})
        
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
        response_data["user"] = CustomUserSerializer(user).data

        return Response(response_data)