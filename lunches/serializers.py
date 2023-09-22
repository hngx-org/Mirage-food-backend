from rest_framework import serializers
from .models import Lunch

class LunchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lunch
        fields = ['id', 'receiver_id', 'sender_id', 'quantity', 'redeemed', 'note', 'created_at']
