from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Lunch
from .serializer import LunchSerializer

class LunchDetailView(APIView):
    def get(self, request, user_id, lunch_id):
        lunch = get_object_or_404(Lunch, sender_id=user_id, id=lunch_id)
        serializer = LunchSerializer(lunch)
        return Response(serializer.data)
