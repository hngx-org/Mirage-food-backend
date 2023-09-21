from rest_framework import serializers
from .models import Withdrawal

class WithdrawalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Withdrawal
        fields = '__all__'

<<<<<<< HEAD
=======

class WithdrawalRequestSerializer(serializers.Serializer):
    bank_name = serializers.CharField(max_length=100)
    bank_number = serializers.CharField(max_length=20)
    bank_code = serializers.CharField(max_length=20)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
>>>>>>> 61f328dee497fbcbfd352ac01075f5d666a17e4b
