from rest_framework import serializers
from .models import Lunch

class LunchSerializer(serializers.ModelSerializer):
<<<<<<< HEAD
    class Meta:
        model = Lunch
        fields = '__all__'
=======
 class Meta:
  model=Lunch
  fields="__all__"
>>>>>>> 5dec6a69ca57e6779e69eb9872c9c3600e6fc30f
