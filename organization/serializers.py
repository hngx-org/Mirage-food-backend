from .models import OrganizationLunchWallet, Invitation
from rest_framework import serializers

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
        fields = ['balance', 'organization']  # Corrected the field name
