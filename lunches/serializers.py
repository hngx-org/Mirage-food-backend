from rest_framework import serializers
from .models import Lunch
from organization.models import OrganizationLunchWallet

class LunchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lunch
        fields = '__all__'

class OrganizationLunchWalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizationLunchWallet
        fields = '__all__'
