from .models import User
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password


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
        fields = ('email', 'password', 'first_name', 'last_name', 'phone', 'org_id', 'refresh_token')
        extra_kwargs = {
            'password': {'write_only': True},
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
    

class UserAddBankAccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["id", "bank_code", "bank_name", "bank_number"]
