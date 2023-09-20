from django.shortcuts import render

# Create your views here.

from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Organization, OrganizationLunchWallet 

def organization_balance(request, organization_id):
    # Get_object_or_404 to retrieve the organization or return a 404 response if it doesn't exist
    organization = get_object_or_404(Organization, id=organization_id)
    balance = OrganizationLunchWallet.balance
    return JsonResponse({'organization_balance': balance})
