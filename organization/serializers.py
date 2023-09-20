from rest_framework import serializers

from .models import Organization, OrganizationLunchWallet


class OrganizationSerializer(serializers.ModelSerializer):
    """
    Serializer for organization model
    """

    class Meta:
        model = Organization
        fields = "__all__"


class OrganizationLunchWalletSerializer(serializers.ModelSerializer):
    """
    Serializer for organization lunch model
    """

    class Meta:
        model = OrganizationLunchWallet
        fields = ["balance", "orgnization"]
