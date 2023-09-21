<<<<<<< HEAD
from rest_framework.serializers import ModelSerializer
from .models import Lunch

class LunchSerializer(ModelSerializer):
    class Meta:
        model = Lunch
        fields = "__all__"
=======
from rest_framework import serializers
from .models import Lunch

class LunchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lunch
        fields = ['receiverID', 'senderID', 'quantity', 'redeemed', 'note', 'created_at', 'id']
>>>>>>> 5dec6a69ca57e6779e69eb9872c9c3600e6fc30f
