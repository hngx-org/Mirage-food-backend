from rest_framework import generics
<<<<<<< HEAD
from .models import Withdrawal
from .serializers import WithdrawalSerializer
=======
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from .models import Withdrawal
from .serializers import WithdrawalSerializer, WithdrawalRequestSerializer


class LunchWithdrawalCreateView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        serializer = WithdrawalRequestSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):

            
            withdrawal = Withdrawal.objects.create(
                bank_name=serializer.validated_data["bank_name"],
                bank_number=serializer.validated_data["bank_number"],
                bank_code=serializer.validated_data["bank_code"],
                amount=serializer.validated_data["amount"],
                user_id=request.user
            )
            withdrawal.status = "redeemed"
            withdrawal.save()


            response_data = {
                "id": withdrawal.id,
                "user_id": withdrawal.user_id.id,
                "status": withdrawal.status,
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

>>>>>>> 61f328dee497fbcbfd352ac01075f5d666a17e4b

class WithdrawalUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Withdrawal.objects.all()
    serializer_class = WithdrawalSerializer
<<<<<<< HEAD
    lookup_field = 'pk'
=======
    lookup_field = "pk"
>>>>>>> 61f328dee497fbcbfd352ac01075f5d666a17e4b
