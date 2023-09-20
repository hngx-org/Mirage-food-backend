from .models import User
from rest_framework import serializers
from django.contrib.auth import get_user_model

# UserModel = get_user_model()

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'first_name', 'last_name', )
        extra_kwargs = {'password': {'write_only': True, 'min_length': 8}}
        
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class SearchedUserSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='pk')
    profile_picture = serializers.ImageField(source='profile_pic')
    class Meta:
        model = User
        fields = ['user_id', 'first_name', 'last_name', 'email', 'profile_picture']