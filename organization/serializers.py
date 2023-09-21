from rest_framework import serializers
from .models import OrganizationLunchWallet


from .models import OrganizationLunchWallet, Organization

class OrganizationLunchWalletSerializer(serializers.ModelSerializer):
    """
    Serializer for organization lunch model
    """

    class Meta:
        model = OrganizationLunchWallet
        fields = ['balance', 'org_id']
class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ["name", "lunch_price", "currency"]
