from rest_framework import serializers
from models import OrganizationLunchWallet


class OrganizationLunchWalletSerializer(serializers.ModelSerializer):
    """
    Serializer for organization lunch model
    """
    class Meta:
        model = OrganizationLunchWallet
        fields = ['balance', 'orgnization']

class OrganizationSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    lunch_price = serializers.DecimalField()
    currency = serializers.CharField(max_length=10)

    def validate_lunch_price(self, value):
        if value:
            if value < 0:
                raise serializers.ValidationError("Lunch price cannot be negative")
        else:
            value = 1000

        return value
