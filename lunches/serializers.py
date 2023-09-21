from rest_framework import serializers
from .models import Lunch

class lunchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lunch
        fields = ['receiverID', 'senderID', 'quantity', 'redeemed', 'note', 'created_at', 'id']