from rest_framework import serializers

from .models import OrganizationLunchWallet, Organization, OrganizationInvites


class OrganizationLunchWalletSerializer(serializers.ModelSerializer):
    """
    Serializer for organization lunch model
    """
    class Meta:
        model = OrganizationLunchWallet
        fields = ['balance', 'orgnization']


class ListInvitesSerializer(serializers.ModelSerializer):
    """
    Serialiser for listing all the invites of an Organisation
    """

    class Meta:
        model = OrganizationInvites
        fields = '__all__'


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ["name", "lunch_price", "currency"]
