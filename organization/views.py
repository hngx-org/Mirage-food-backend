from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import OrganizationSerializer
from users.permissions import IsAdmin
from . import workers

# Create your views here.


class OrganizationView(APIView):
    permission_classes = [
        IsAdmin,
    ]

    def post(self, request):
        request.data["lunch_price"] = request.data.get("lunch_price", 1000)
        serializer = OrganizationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        workers.Organization.create_organization(**serializer.validated_data)
        return Response(serializer.validated_data, status=status.HTTP_201_CREATED)
