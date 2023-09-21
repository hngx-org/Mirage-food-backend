from rest_framework import generics
from .models import Withdrawal
from .serializers import WithdrawalSerializer

class WithdrawalUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Withdrawal.objects.all()
    serializer_class = WithdrawalSerializer
    lookup_field = 'pk'
