from .models import User
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password
import cloudinary
from django.conf import settings


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


class UserProfilePictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['profile_pic']


class UserAddBankAccountSerializer(serializers.ModelSerializer):
    bank_name = serializers.CharField(max_length=50)
    bank_code = serializers.CharField(max_length=50)
    bank_number = serializers.CharField(max_length=50)
    
    class Meta:
        model = User
        fields = ["id", "bank_code", "bank_name", "bank_number"]
