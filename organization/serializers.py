from rest_framework import serializers

from .models import OrganizationLunchWallet, Organization


class OrganizationLunchWalletSerializer(serializers.ModelSerializer):
    """
    Serializer for organization lunch model
    """

    class Meta:
        model = OrganizationLunchWallet
        fields = ["balance", "orgnization"]


class OrganizationSerializer(serializers.ModelSerializer):
    lunch_price = serializers.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = Organization
        fields = ["name", "lunch_price", "currency"]

    def validate_lunch_price(self, value):
        if value:
            if value < 0:
                raise serializers.ValidationError("Lunch price cannot be negative")
        else:
            value = 1000

        return value
