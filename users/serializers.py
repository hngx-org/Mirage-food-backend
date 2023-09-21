from .models import User
from rest_framework import serializers

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'first_name', 'last_name', )
        extra_kwargs = {'password': {'write_only': True, 'min_length': 8}}
        
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    
class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'org_id', 'first_name', 'last_name', 'profile_pic', 'email', 'phone', 'created_at', 'updated_at', 'lunch_credit_balance']
       
