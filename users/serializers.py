from .models import User
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password


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

class UserBankDetailsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='pk')
    email = serializers.EmailField()
    bank_number = serializers.CharField()
    bank_code = serializers.CharField()
    bank_name = serializers.CharField()
    class Meta:
        model = User
        fields = ('id', 'email', 'bank_number', 'bank_code', 'bank_name')