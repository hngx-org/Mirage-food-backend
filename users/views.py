from django.shortcuts import render
#uncomment when serializer class and model class is created
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
#from .models import User
#from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework import status, authentication

@csrf_exempt
@api_view(['GET'])
@permissionClasses([IsAuthenticated])
def get_user(request, *args, **kwargs):
    """
    Get a particular user from user_id or email
    """
    id = request.GET.get("id")
    user = get_object_or_404(User, pk=id)
    serializer = UserSerializer(user)
    return Response({
        "message": "User found",
        "data": serializer.data
    }, status=status.HTTP_200_OK)
