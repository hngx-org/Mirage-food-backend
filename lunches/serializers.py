from .models import Lunch
from rest_framework import serializers


class LunchSerializers(serializers.ModelSerializer):
    class Meta:
        model = Lunch
        fields = [
            "id",
            "quantity",
            "redeemed",
            "note",
            "created_at",
            "sender",
            "receiver",
        ]
