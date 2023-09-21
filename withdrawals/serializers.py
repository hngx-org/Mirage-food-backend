from rest_framework import serializers
from .models import Withdrawal

class WithdrawalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Withdrawal
        fields = '__all__'


class WithdrawalRequestSerializer(serializers.Serializer):
    bank_name = serializers.CharField(max_length=100)
    bank_number = serializers.CharField(max_length=20)
    bank_code = serializers.CharField(max_length=10)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)