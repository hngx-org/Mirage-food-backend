from rest_framework import serializers
from .models import Lunch


class LunchSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lunch
        fields = '__all__'
        extra_kwargs = {
            "quantity": {"default": 1},
            "note": {"default": "This is your free lunch!"}
        }
