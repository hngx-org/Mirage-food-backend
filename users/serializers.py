from .models import User
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'first_name', 'last_name', )
        extra_kwargs = {'password': {'write_only': True, 'min_length': 8}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user
        user = User.objects.create_user(**validated_data)
        return user


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'org_id', 'first_name', 'last_name', 'profile_pic', 'email', 'phone', 'created_at', 'updated_at', 'lunch_credit_balance']
User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name', 'phone')
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
