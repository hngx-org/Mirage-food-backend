from .models import User
from rest_framework import serializers



class UserRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'phone', ' profile_pic ',
                  'bank_name', 'bank_number', 'bank_code', 'bank_region', 'currency', 'currency_code',
                    'created_at', 'updated_at', 'lunch_credit_balance'
                  ]


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'