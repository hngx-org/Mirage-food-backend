# views.py (in the main app)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from organization.models import Organization, OrganizationLunchWallet
from .models import Lunch
from .serializers import LunchSerializer

class SendFreeLunch(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, sender_id, organization_id):
        try:
            sender = request.user
            receiver_id = request.data.get('receiver_id')
            quantity = request.data.get('quantity')

            # Retrieve the organization
            organization = Organization.objects.get(id=organization_id)

            # Check if the sender belongs to the organization
            if sender not in organization.members.all():
                return Response({'detail': 'You do not belong to this organization.'}, status=status.HTTP_403_FORBIDDEN)

            # Check if the sender has enough balance in the organization's lunch wallet
            lunch_wallet = OrganizationLunchWallet.objects.get(organization=organization)
            if lunch_wallet.balance < quantity:
                return Response({'detail': 'Insufficient balance in the organization lunch wallet.'}, status=status.HTTP_400_BAD_REQUEST)

            # Create the Lunch record
            lunch = Lunch(sender=sender, receiver_id=receiver_id, quantity=quantity, organization=organization)
            lunch.save()

            # Update the lunch wallet balance
            lunch_wallet.balance -= quantity
            lunch_wallet.save()

            # Serialize the lunch object and return it as a response
            serializer = LunchSerializer(lunch)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Organization.DoesNotExist:
            return Response({'detail': 'Organization not found.'}, status=status.HTTP_404_NOT_FOUND)
