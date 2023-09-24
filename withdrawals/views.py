
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from users.models import User

from .models import Withdrawal
from .serializers import WithdrawalRequestSerializer

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class LunchWithdrawalCreateView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_summary="Request a withdrawal",
        request_body=WithdrawalRequestSerializer,
        responses={201: 'Created', 400: 'Bad Request'},
    )
    def post(self, request, *args, **kwargs):
        data = request.data
        bank_name = data.get("bank_name")
        bank_number = data.get("bank_number")
        serializer = WithdrawalRequestSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
             user = request.user
             withdrawal = Withdrawal.objects.create(
                amount=serializer.validated_data["amount"],
                user_id=user
            )
             if int(user.lunch_credit_balance) < int(withdrawal.amount):
                error_response = {
                    "message": "Your lunch credit balance is below your withdrawal amount"
                }
                return Response(error_response, status=status.HTTP_400_BAD_REQUEST)
             if user.bank_name != bank_name or user.bank_number != bank_number:
                print(bank_name, bank_number)
                response = {
                    "message": "User bank account or bank name not correct"
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
             withdrawal.status = "redeemed"
             withdrawal.save()
             user.lunch_credit_balance = float(user.lunch_credit_balance) - float(withdrawal.amount)
             user.lunch_credit_balance = int(user.lunch_credit_balance)
             user.save()
             response_data = {
                "id": withdrawal.id,
                "user_id": withdrawal.user_id.id,
                "status": "success",
                "amount": withdrawal.amount,
                "created_at": withdrawal.created_at
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
