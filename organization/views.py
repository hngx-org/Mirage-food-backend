from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Organization, OrganizationLunchWallet

def organization_balance(request, organization_id):
    # Retrieve the organization or return a 404 response if it doesn't exist
    organization = get_object_or_404(Organization, id=organization_id)

    # Query the OrganizationLunchWallet model to get the balance for this organization
    lunch_wallet = OrganizationLunchWallet.objects.filter(org_id=organization_id).first()

    if lunch_wallet:
        balance = lunch_wallet.balance
    else:
        balance = 0.00  # default balance if no lunch wallet record exists

    return JsonResponse({'organization_balance': balance})
