from rest_framework import serializers
from .models import Lunch

class LunchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lunch
        fields = '__all__'
        fields = ['receiverID', 'senderID', 'quantity', 'redeemed', 'note', 'created_at', 'id']
