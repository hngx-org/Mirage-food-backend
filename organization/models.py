from django.db import models
from django.core.validators import MinValueValidator

# Create your models here.
class OrganizationLunchWallet(models.Model):
  """Model for Organization Lunch Wallet"""
  balance = models.DecimalField(max_digits=10,decimal_places=2,validators=[MinValueValidator(0)])
  org_id = models.ForeignKey(Organization, on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
