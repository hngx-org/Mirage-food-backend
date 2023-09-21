from rest_framework import serializers
from .models import User as CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'password', 'first_name', 'last_name', )
        extra_kwargs = {'password': {'write_only': True, 'min_length': 8}}
        
    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user


class SearchedUserSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='pk')
    profile_picture = serializers.ImageField(source='profile_pic')
    class Meta:
        model = CustomUser 
        fields = ['user_id', 'first_name', 'last_name', 'email', 'profile_picture']