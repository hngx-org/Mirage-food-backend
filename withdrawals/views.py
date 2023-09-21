from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from lunches.models import Lunch

from .models import Withdrawal
from .serializers import WithdrawalSerializer


class LunchWithdrawalCreateView(APIView):
    def post(self, request, *args, **kwargs):
        # I assummed the lunch_id is provided in the body
        lunch_id = request.data.get("lunch_id")
        try:
            lunch = Lunch.objects.get(pk=lunch_id)
        except Lunch.DoesNotExist:
            return Response({"message": "Lunch not found"}, status.HTTP_404_NOT_FOUND)

        if lunch.redeemed:
            return Response(
                {"message": "This lunch has already been redeemed"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        # The code below withdraws the lunch. Payment provider wasn't integrated.

        serializer = WithdrawalSerializer(data=request.data)
        if serializer.is_valid():
            withdrawal = serializer.save()
            withdrawal.status = "redeemed"
            lunch.redeemed = True
            withdrawal.save()

            response_data = {
                "id": withdrawal.id,
                "user_id": withdrawal.user_id.id,
                "status": withdrawal.status,
                "amount": withdrawal.amount,
                "created_at": withdrawal.created_at,
            }

            return Response(
                {
                    "message": "Withdrawal request created successfully",
                    "statusCode": 201,
                    "data": response_data,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WithdrawalUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Withdrawal.objects.all()
    serializer_class = WithdrawalSerializer
    lookup_field = "pk"
