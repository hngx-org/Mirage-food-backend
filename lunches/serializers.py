from rest_framework.serializers import ModelSerializer
from .models import Lunch

class LunchSerializer(ModelSerializer):
    class Meta:
        model = Lunch
        fields = "__all__"