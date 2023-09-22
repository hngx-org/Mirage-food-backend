from rest_framework import serializers
from .models import Lunch

class LunchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lunch
        fields = ['receiver', 'sender_id', 'quantity', 'redeemed', 'note', 'created_at', 'id']
