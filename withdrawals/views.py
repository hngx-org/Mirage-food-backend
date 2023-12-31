from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from .models import Withdrawal
from .serializers import WithdrawalSerializer, WithdrawalRequestSerializer


class WithdrawalCreateView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        serializer = WithdrawalRequestSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            
            withdrawal = Withdrawal.objects.create(
                amount=serializer.validated_data["amount"],
                user_id=request.user)
            withdrawal.status = "redeemed"
            withdrawal.save()


            response_data = {
                "id": withdrawal.id,
                "user_id": withdrawal.user_id.id,
                "status": "success",
                "amount": withdrawal.amount,
                "created_at": withdrawal.created_at.isoformat(),
            }

            return Response(
                {
                    "message": "Withdrawal request created successfully",
                    "statusCode": status.HTTP_201_CREATED,
                    "data": response_data,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class WithdrawalUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Withdrawal.objects.all()
    serializer_class = WithdrawalSerializer
    lookup_field = "pk"
