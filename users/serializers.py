from .models import User
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password
import cloudinary
from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_decode


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'org_id', 'first_name', 'last_name', 'profile_pic', 'email', 'phone', 'created_at', 'updated_at', 'lunch_credit_balance']

   
    

class SearchedUserSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='pk')
    profile_picture = serializers.ImageField(source='profile_pic')
    class Meta:
        model = User 
        fields = ['user_id', 'first_name', 'last_name', 'email', 'profile_picture']

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name', 'phone', 'org_id', 'refresh_token', 'lunch_credit_balance')
        extra_kwargs = {
            'password': {'write_only': True},
            'lunch_credit_balance': {'default': 1000}
        }

    def validate_password(self, value):
        # Use Django's password validation to ensure a strong password
        validate_password(value)
        return value

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    
  
    
    def update(self, instance, validated_data):
        # Hash the new password and update the user's password field
        new_password = validated_data.get('password')
        if new_password:
            hashed_password = make_password(new_password)
            instance.password = hashed_password
        # Call save to persist the changes to the database
        instance.save()
        return instance
    
class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone', 'bank_number', 'bank_code', 'bank_name', 'lunch_credit_balance']


# class UserProfilePictureSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['profile_pic']


class UserAddBankAccountSerializer(serializers.ModelSerializer):
    bank_name = serializers.CharField(max_length=50)
    bank_code = serializers.CharField(max_length=50)
    bank_number = serializers.CharField(max_length=50)
    
    class Meta:
        model = User
        fields = ["id", "bank_code", "bank_name", "bank_number"]




class EmailSerializer(serializers.Serializer):
    """
    Reset Password Email Request Serializer.
    """

    email = serializers.EmailField()

    class Meta:
        fields = ("email",)



class ResetPasswordSerializer(serializers.Serializer):
    """
    Reset Password Serializer.
    """

    password = serializers.CharField(
        write_only=True,
        min_length=1,
    )

    class Meta:
        field = ("password")

    def validate(self, data):
        """
        Verify token and encoded_pk and then set new password.
        """
        password = data.get("password")
        token = self.context.get("kwargs").get("token")
        encoded_pk = self.context.get("kwargs").get("encoded_pk")

        if token is None or encoded_pk is None:
            raise serializers.ValidationError("Missing data.")

        pk = urlsafe_base64_decode(encoded_pk).decode()
        user = User.objects.get(pk=pk)
        if not PasswordResetTokenGenerator().check_token(user, token):
            raise serializers.ValidationError("The reset token is invalid")

        user.set_password(password)
        user.save()
        return data

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
