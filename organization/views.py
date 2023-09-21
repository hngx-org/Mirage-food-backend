from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Organization
from users.permissions import IsAdmin
# Create your views here.

class DeleteOrganizationView(APIView):
    permission_classes = [IsAdmin]
    def delete(request, org_id):
        organization = Organization.object.get(pk=org_id)
        if request.user in organization.user_set.all():
            organization.delete()
            return Response({'message':'Organization deleted'},status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'error':'Organization not found'}, status=status.HTTP_404_NOT_FOUND)