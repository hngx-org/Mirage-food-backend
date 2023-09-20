from .models import User
from .models import User
from rest_framework import serializers
from django.core import validators
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator


class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(
        read_only=True,
    )
    email = serializers.EmailField(
        validators=[
            UniqueValidator(queryset=User.objects.all()),
            validators.validate_email,
        ]
    )
    password = serializers.CharField(
        write_only=True,
        min_length=8,
    )
    first_name = serializers.CharField(
        validators=[
            validators.RegexValidator(r'^[a-zA-Z ]+$', 'Name must be letters only')
        ]
    )

    last_name = serializers.CharField(
        validators=[
            validators.RegexValidator(r'^[a-zA-Z ]+$', 'Name must be letters only')
        ]
    )

    profile_pic = serializers.ImageField(
        required=False,
        allow_null=True,
        allow_empty_file=True,
    )
    phone = serializers.CharField(
        validators=[
            validators.RegexValidator(r'^\+?234[789][01]\d{8}$', 'Invalid Nigerian phone number'), # I found it useful to validate numbers but not sure how to cover a wide range of numbers. This is tentative, kindly review
            UniqueTogetherValidator(queryset=User.objects.all(), fields=['phone', 'email'], message='Phone number already exists for another user',)
        ]
    )
    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'first_name', 'last_name', 'profile_pic')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 8}}
        