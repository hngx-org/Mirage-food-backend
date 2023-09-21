from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import OrganizationLunchWalletSerializer
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST

class OrganizationLunchWalletView(APIView):
    def post(self, request):
        serializer = OrganizationLunchWalletSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

