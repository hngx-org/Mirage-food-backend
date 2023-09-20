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
    class Meta:
        model = Organization
        fields = ["name", "lunch_price", "currency"]

#Serializer for Organization Invite
class OrganizationInviteSerializer(serializers.Serializer):
    email = serializers.EmailField()