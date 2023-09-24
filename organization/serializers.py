from .models import  Invitation
from rest_framework import serializers
from .models import OrganizationLunchWallet




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


 # Corrected the field name

        fields = ['balance', 'orgnization']

   

        fields = ['org_id','balance']




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


#organizationwalletupdate changes
class OrganizationLunchWalletUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for organization lunch wallet model
    """
    class Meta:
        model = OrganizationLunchWallet
        fields = ['balance']

