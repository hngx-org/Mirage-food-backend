from rest_framework import serializers


from .models import (
        OrganizationLunchWallet,
        Organization,
        OrganizationInvites,
        OrganizationLunchPrice
        )


class OrganizationLunchWalletSerializer(serializers.ModelSerializer):
    """
    Serializer for organization lunch model
    """
    class Meta:
        model = OrganizationLunchWallet
        fields = ['balance', 'org_id']


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


class OrganizationLunchPriceSerializer(serializers.ModelSerializer):
    """
    Serializer for updating lunch price
    """
    class Meta:
        model = OrganizationLunchPrice
        fields = ['lunch_price']
