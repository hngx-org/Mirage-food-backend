from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Withdrawal
class WithdrawalSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Withdrawal
        fields = "__all__"
