from django.shortcuts import render
#uncomment when serializer class and model class is created
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404, get_list_or_404
from .models import User
#from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework import status, authentication
from rest_framework.permissions import IsAuthenticated

@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user(request, pk, *args, **kwargs):
    """
    Get a particular user from user_id, name or email
    """
    try:
        user = get_list_or_404(User, name=pk)
        serializer = UserSerializer(user, many=True)
    except:
        user = get_object_or_404(User, email=pk)
        serializer = UserSerializer(user)
    return Response({
        "message": "User found",
        "data": serializer.data
    }, status=status.HTTP_200_OK)
