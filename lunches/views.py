from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Lunch
from .serializers import LunchSerializers


class WithdrawLunchView(APIView):
    def post(self, request, pk, *args, **kwargs):
        try:
            lunch = Lunch.objects.get(id=pk)
        except Lunch.DoesNotExist:
            return Response(
                {"message": "Lunch is not found"}, status.HTTP_404_NOT_FOUND
            )

        if request.user == lunch.receiver:
            if not lunch.redeemed:
                lunch.redeemed = True
                lunch.save()

                serializer = LunchSerializers(lunch)
                return Response(
                    serializer.data,
                    {"message": "Lunch redeemed successfully"},
                    status.HTTP_201_CREATED,
                )

            else:
                return Response(
                    {"message": "Lunch has already been redeemed"},
                    status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(
                {"message": "You're not authorized to withdraw this lunch"},
                status.HTTP_403_FORBIDDEN,
            )
