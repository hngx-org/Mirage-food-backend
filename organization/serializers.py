from .models import  Invitation
from rest_framework import serializers


from .models import (
        OrganizationLunchWallet,
        Organization,
        OrganizationInvites,
        OrganizationLunchPrice
        )


from .models import OrganizationLunchWallet, Organization, OrganizationInvites


class InvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invitation
        fields = '__all__'

class OrganizationLunchWalletSerializer(serializers.ModelSerializer):
    """
    Serializer for organization lunch wallet model
    """
    class Meta:
        model = OrganizationLunchWallet
        fields = ['balance', 'organization']


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



#Serializer for Organization Invite
class OrganizationInviteSerializer(serializers.Serializer):
    email = serializers.EmailField()

class OrganizationLunchPriceSerializer(serializers.ModelSerializer):
    """
    Serializer for updating lunch price
    """
    class Meta:
        model = OrganizationLunchPrice
        fields = ['lunch_price']


#organizationwalletupdate changes
class OrganizationLunchWalletUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for organization lunch wallet model
    """
    class Meta:
        model = OrganizationLunchWallet
        fields = ['balance']

